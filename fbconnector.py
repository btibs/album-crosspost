# Facebook-related code

from fboauth import FbOauth

from urllib.request import urlopen
import json
import facebook
import os
import requests
import shutil

CREDENTIALS_FILE = ".fbcredentials"

class FacebookConnector:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.client = None

    def authenticate(self):
        """Connect and authenticate user with Facebook"""
        if self.client is not None:
            return

        graph = None
        token = None
        try:
            auth_file = open(CREDENTIALS_FILE, "r")
            token = auth_file.readline()
            auth_file.close()
            graph = facebook.GraphAPI(access_token=token)
            print("Facebook: Authenticated with saved credentials")
        except:
            print("Facebook: Could not read authorization credentials, opening browser to authenticate...")
            auth = FbOauth(self.app_id, self.app_secret)
            token = auth.get_access_token()
            graph = facebook.GraphAPI(access_token=token)
            auth_file = open(CREDENTIALS_FILE, "w")
            auth_file.write(token)
            auth_file.close()
            print("Facebook: Successfully authenticated and saved to file!")

        self.client = graph

    def get_albums(self):
        """Return a listing of all albums"""
        response = self.client.request("me?fields=albums&limit=100")
        return response['albums']['data']

    def get_photo(self, photo_id):
        """Get a single photo. This will return the object with max size"""
        photos = self.client.get_object(photo_id, fields='id,name,images')
        caption = None
        if 'name' in photos:
            caption = photos['name']
        return (max(photos['images'], key=lambda x: x['width']), caption)

    def download_album(self, album_id):
        """
        Download album with given ID. Pictures and relevant info will be saved in
        a directory labeled with the album's ID
        """
        album = self.client.get_object(album_id, fields='name,description,count')
        album_description = ""
        if "description" in album:
            album_description = album["description"]

        album_photos = self.client.request(album_id+"/photos")
        
        # TODO if already exists...?
        if not os.path.exists(album_id):
           os.makedirs(album_id)
        
        # TODO this just does first 25, need to do pagination
        info = {"title": album["name"], "description":album_description, "photos":[]}
        i = 1
        for album_photo in album_photos['data']:
            print("Downloading image {0} of {1}".format(i,album['count']))
            photo, caption = self.get_photo(album_photo['id'])
            filename = album_photo['id'] + ".jpg"
            info["photos"].append({'id':album_photo['id'], 'file':filename, 'caption':caption})
            image = requests.get(photo["source"], stream=True)
            image_file = open(os.path.join(album_id, filename), "wb")
            shutil.copyfileobj(image.raw, image_file)
            image_file.close()
            i += 1

        info_file = open(os.path.join(album_id, "info.json"), "w")
        json.dump(info, info_file)
        info_file.close()
        print("Download complete! Album is located in: " + album_id)
