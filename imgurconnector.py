# Imgur-related code

from imgurpython import ImgurClient

from fbconnector import INFO_FILE

import json
import webbrowser
import sys
from dateutil import parser

from base64 import b64encode

CREDENTIALS_FILE = ".imgcredentials"
IMGUR_API_BASE = "https://api.imgur.com/"
IMGUR_ALBUM_BASE = "https://imgur.com/a/"

def make_caption(data):
    s = "Originally uploaded: %s\nLast updated: %s" % (parser.parse(data['created_time']), parser.parse(data['created_time']))
    if data['backdated_time'] is not None:
        s += "\n\nBackdated to: %s" % parser.parse(data['backdated_time'])
    if data['tags'] is not None and len(data['tags']) > 0:
        s += "\n\nTagged: " + ','.join(data['tags'])
    if data['place'] is not None:
        s += "\n\nLocation: " + data['place']
    return s

class ImgurConnector:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.client = None

    def authenticate(self):
        """Connect and authenticate user with Imgur"""
        if self.client is not None:
            return

        # lasts for one month, access to user's account
        access_token = None
        # request new access token without more authorization process, does not expire
        refresh_token = None
        try:
            auth_file = open(CREDENTIALS_FILE, "r")
            lines = auth_file.read().split("\n")
            auth_file.close()
            if (len(lines) < 2):
                raise Exception("Imgur: Missing tokens in file")
            access_token = lines[0]
            refresh_token = lines[1]
            if access_token is None or refresh_token is None:
                raise Exception("Imgur: Empty tokens in file")
            client = ImgurClient(self.app_id, self.app_secret, access_token, refresh_token)
            print("Imgur: Authenticated with saved credentials")
        except:
            print("Imgur: Could not read authorization credentials, opening browser to authenticate...")
            imgur_client = ImgurClient(self.app_id, self.app_secret)
            auth_url = imgur_client.get_auth_url('pin')
            webbrowser.open_new_tab(auth_url)
            pin = input("Enter PIN: ")
            try:
                credentials = imgur_client.authorize(pin, 'pin')
                client = ImgurClient(self.app_id, self.app_secret, credentials['access_token'], credentials['refresh_token'])
            except:
                print("Error authenticating PIN:", sys.exc_info()[1])
                sys.exit()

            auth_file = open(CREDENTIALS_FILE, "w")
            auth_file.write(credentials['access_token'] + "\n")
            auth_file.write(credentials['refresh_token'])
            auth_file.close()
            print("Imgur: Successfully authenticated and saved to file!")
        
        self.client = client

    def upload_album(self, album_folder):
        """Upload the given album to imgur"""
        
        # Read in the album information
        metadata = json.load(open(album_folder + "/" + INFO_FILE, 'r'))

        # Create the album
        album_description = metadata['description']
        if metadata['location'] is not None:
            album_description += "\n\nLocation: " + metadata['location']
        album_fields = {'title':metadata['name'], 'description':album_description, 'privacy':'hidden'}
        album_response = self.client.create_album(album_fields)
        album_id = album_response['id']

        # Upload all the images
        for img in metadata['photos']:
            img_path = album_folder + "/" + img['filename']
            description = make_caption(img)
            config = {'album':album_id, 'title':img['name'], 'description':description}
            print("Uploading " + img_path)
            img_response = self.client.upload_from_path(img_path, config=config, anon=False)

        print("Album online at " + IMGUR_ALBUM_BASE + album_id)
