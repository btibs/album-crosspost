from constants import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET
from fboauth import FbOauth

import facebook
from imgurpython import ImgurClient

FB_CREDENTIALS_FILE = ".fbcredentials"
IMGUR_CREDENTIALS_FILE = ".imgcredentials"

## FACEBOOK CODE

def fb_auth():
    graph = None
    token = None
    # TODO saving token doesn't work, but getting the token seems ok
    try:
        auth_file = open(FB_CREDENTIALS_FILE, "r")
        auth_file.close()
        token = auth_file.readline()
        graph = facebook.GraphAPI(access_token=token)
        print("Facebook: Authenticated with saved credentials")
    except:
        print("Facebook: Could not read authorization credentials, opening browser to authenticate...")
        auth = FbOauth(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        token = auth.get_access_token()
        graph = facebook.GraphAPI(access_token=token)
        auth_file = open(FB_CREDENTIALS_FILE, "w")
        auth_file.write(token)
        auth_file.close()
        print("Facebook: Successfully authenticated and saved to file!")
    return graph

def get_fb_album(fb_client):
    """
    fb_client = fb_auth()
    album = fb_client.download_photo_album_with_ordering_and_titles()
    return downloaded_album_location
    """
    pass

## IMGUR CODE

# Get authorized client for Imgur API
def imgur_auth():
    imgur_client = None
    access_token = None # lasts for one month, access to user's account
    refresh_token = None # request new access token without more authorization process, does not expire
    try:
        auth_file = open(IMGUR_CREDENTIALS_FILE, "r")
        lines = auth_file.read().split("\n")
        auth_file.close()
        if (len(lines) < 2):
            raise Exception("Imgur: Missing tokens in file")
        access_token = lines[0]
        refresh_token = lines[1]
        if access_token is None or refresh_token is None:
            raise Exception("Imgur: Empty tokens in file")
        imgur_client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, access_token, refresh_token)
        print("Imgur: Authenticated with saved credentials")
    except:
        print("Imgur: Could not read authorization credentials, opening browser to authenticate...")
        imgur_client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
        auth_url = imgur_client.get_auth_url('pin')
        webbrowser.open_new_tab(auth_url)
        pin = input("Enter PIN: ")
        # TODO what if not authorize
        credentials = imgur_client.authorize(pin, 'pin')
        imgur_client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
        auth_file = open(IMGUR_CREDENTIALS_FILE, "w")
        auth_file.write(credentials['access_token'] + "\n")
        auth_file.write(credentials['refresh_token'])
        auth_file.close()
        print("Imgur: Successfully authenticated and saved to file!")
    return imgur_client

def make_imgur_album(imgur_client, album):
    """
    imgur_client = imgur_auth()
    create_imgur_album(imgur_client, title, album_files)
    """
    pass

if __name__ == "__main__":
    graph = fb_auth()
    #album = get_fb_album(graph)
    imgur_client = imgur_auth()
    #make_imgur_album(imgur_client, album)
