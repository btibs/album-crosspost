# Imgur-related code

from imgurpython import ImgurClient
import webbrowser
import sys

CREDENTIALS_FILE = ".imgcredentials"

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

    def make_album(self, album):
        """Create a new imgur album"""
        pass