Cross-post a facebook album to imgur

Developed on Windows 7 using Python 3, no guarantees for other platforms

Uses:

* Python Facebook SDK: https://github.com/mobolic/facebook-sdk
* Imgur Python client: https://github.com/Imgur/imgurpython

See constants_blank.py for the example constants file, replace with your values for facebook and imgur apps, and rename to constants.py.

You will need to add http://localhost:8000/ the list of valid OAuth redirect URIs on Facebook.

Credential tokens will be saved in .credentials

App name is "album-crosspost" on both Facebook and Imgur (of course, both are currently in dev mode)
