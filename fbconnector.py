# Facebook-related code

from fboauth import FbOauth
from fbalbum import FacebookAlbumIterator, FacebookPhotoIterator

from urllib.request import urlopen
import json
import facebook
import os
import requests
import shutil
from dateutil import parser, tz
import time

CREDENTIALS_FILE = ".fbcredentials"
INFO_FILE = "info.json"
ALBUM_FIELDS = ["name","created_time","updated_time","description","location"] # not exactly sure how users set album location but it does return things sometimes...
PHOTO_FIELDS = ["name","created_time","backdated_time","updated_time","tags","place"] #"name_tags" is in the API docs but doesn't actually return things...

def get_local_time(time_str):
    """Convert time string into a local timestamp"""
    t = parser.parse(time_str)
    t_local = t.astimezone(tz.tzlocal())
    return time.mktime(t_local.timetuple())

class FacebookConnector:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.graph = None

    def authenticate(self):
        """Connect and authenticate user with Facebook"""
        if self.graph is not None:
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

        self.graph = graph

    def get_album_iterator(self):
        """Return an iterator to list all albums"""
        return FacebookAlbumIterator(self.graph)

    def get_photo(self, photo_id):
        """Get a single photo. This will return the object with max size"""
        photos = self.graph.get_object(photo_id, fields=','.join(PHOTO_FIELDS + ['id','images']))

        # Get largest image
        img_max = max(photos['images'], key=lambda x: x['width'])
        del(photos['images'])

        # Simplify tags
        photo_tags = []
        if "tags" in photos:
            for tag in photos['tags']['data']:
                photo_tags.append(tag['name'])
        photos['tags'] = photo_tags

        # Simplify locations
        place = None
        if "place" in photos:
            place = photos['place']['name']
        photos['place'] = place

        return (img_max, photos)

    def download_album(self, album_id):
        """
        Download album with given ID. Pictures and relevant info will be saved in
        a directory labeled with the album's ID

        Returns the directory where the album was downloaded
        """
        album = self.graph.get_object(album_id, fields=','.join(ALBUM_FIELDS + ['count']))

        # Create folder for album
        folder_name = album_id

        if not os.path.exists(folder_name):
           os.makedirs(folder_name)
        
        # Metadata for all photos
        info = {"photos":[]}
        for field in ALBUM_FIELDS:
            if field in album:
                info[field] = album[field]
            else:
                info[field] = None
        
        i = 1 # for the normal people who count 1-indexed :P
        for album_photo in FacebookPhotoIterator(self.graph, album_id):
            print("Downloading image {0} of {1}".format(i,album['count']))
            
            img_max, photo = self.get_photo(album_photo['id'])
            filename = album_photo['id'] + ".jpg"
            photo_info = {'filename':filename}
            for field in PHOTO_FIELDS:
                if field in photo:
                    photo_info[field] = photo[field]
                else:
                    photo_info[field] = None
            
            info["photos"].append(photo_info)
            
            # Save image
            image = requests.get(img_max["source"], stream=True)
            image_file = open(os.path.join(folder_name, filename), "wb")
            shutil.copyfileobj(image.raw, image_file)
            image_file.close()

            # Set image file time
            ct = get_local_time(photo["created_time"])
            ut = get_local_time(photo["updated_time"])
            os.utime(image_file.name, (ct, ut))

            i += 1

        info_file = open(os.path.join(folder_name, INFO_FILE), "w")
        json.dump(info, info_file)
        info_file.close()
        print("Download complete! Album is located in: " + folder_name)

        return folder_name
