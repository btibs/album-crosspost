from constants import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET

#from imgurconnector import ImgurConnector
from fbconnector import FacebookConnector

import sys

def main():
    fb = FacebookConnector(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
    fb.authenticate()
    #imgur = ImgurConnector(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    #imgur.authenticate()
    
    while True:
        print()
        for a in fb.get_album_iterator():
            print(a['id'] + ": " + a['name'])
        aid = input("\nEnter ID of album to download, or q to quit: ")
        print()
        if aid == 'q':
            print("Bye")
            sys.exit(0)

        fb.download_album(aid)
        #imgur.make_album(aid)

if __name__ == "__main__":
    main()
