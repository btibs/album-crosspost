from constants import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET

from imgurconnector import ImgurConnector
from fbconnector import FacebookConnector

import sys

DOWNLOAD_DIR = "temp"

def main():
    fb = FacebookConnector(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
    fb.authenticate()
    imgur = ImgurConnector(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    imgur.authenticate()
    
    albums = fb.get_albums()
    for a in albums:
        print(a['id'] + ": " + a['name'])
    aid = input("Enter ID of album to download, or 0 to quit: ")
    if aid is 0:
        print("Bye")
        sys.exit(0)
    fb.get_album(aid, DOWNLOAD_DIR)

    imgur.make_album(DOWNLOAD_DIR)

if __name__ == "__main__":
    main()
