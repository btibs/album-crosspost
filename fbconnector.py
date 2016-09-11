# Facebook-related code
from fboauth import FbOauth
import facebook

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
        pass

    def download_album(self, album_id, directory):
        """Download the album with given ID into a given directory"""
        pass
