Cross-post a facebook album to imgur

Developed on Windows 7 using Python 3, no guarantees for other platforms

**I have since stopped using Facebook, so I am abandoning this project. Feel free to fix up for your own purposes and submit a pull request!** Currently, authentication to both services are working and it can download the album photos of Facebook, but I didn't finish the upload to Imgur half of it.

Libraries used:

* Python Facebook SDK: https://github.com/mobolic/facebook-sdk
* Imgur Python client: https://github.com/Imgur/imgurpython

See constants_blank.py for the example constants file, replace with your values for facebook and imgur apps, and rename to constants.py.

You will need to add http://localhost:8000/ the list of valid OAuth redirect URIs on Facebook.

Credential tokens will be saved in .credentials

App name is "album-crosspost" on both Facebook and Imgur (of course, both are currently in dev mode)
