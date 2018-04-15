Cross-post a facebook album to imgur

Developed on Windows 7 using Python 3, no guarantees for other platforms

**Current status**

- Facebook OAuth does not work. Facebook has started requiring all apps to use HTTPS and this was using a local HTTP server. Workaround: manually generate a token at https://developers.facebook.com/tools/explorer/145634995501895/ (select the `user_photos` permission) and paste into a file named `.fbcredentials`.
- Facebook album download only
- Imgur authentication works once you have a token, but currently has issues with getting it... stay tuned.

Libraries used:

* Python Facebook SDK: https://github.com/mobolic/facebook-sdk
* Imgur Python client: https://github.com/Imgur/imgurpython

See `constants_blank.py` for the example constants file, replace with your values for facebook and imgur apps, and rename to `constants.py`.

You will need to add http://localhost:8000/ the list of valid OAuth redirect URIs on Facebook.

Credential tokens will be saved in files named `.fbcredentials` and `.imgcredentials`

App name is "album-crosspost" on both Facebook and Imgur (of course, both are currently in dev mode)
