Cross-post a facebook album to imgur

Developed on Windows 7 using Python 3, no guarantees for other platforms

Currently working! Downloads from Facebook to disk, then uploads to Imgur using the Facebook metadata.

**Important notes:**

- Facebook OAuth does not work. Facebook has started requiring all apps to use HTTPS and this was using a local HTTP server. Workaround: manually generate a token at https://developers.facebook.com/tools/explorer/145634995501895/ (select the `user_photos` permission) and paste into a file named `.fbcredentials`.

**Libraries used:**

* Python Facebook SDK: https://github.com/mobolic/facebook-sdk
* Imgur Python client: https://github.com/Imgur/imgurpython

**Setup**

You will have to set up your own Facebook and Imgur apps, I have not made publicly available (e.g. non-developer-mode) apps. Once you have done that:

1. Add https://localhost:8000/ the list of valid OAuth redirect URIs on Facebook.
2. See `constants_blank.py` for the example constants file, replace with your values for facebook and imgur apps, and rename to `constants.py`.
3. See note above: instead of authorizing via the app, generate a Facebook user token [here](https://developers.facebook.com/tools/explorer/145634995501895/) and save in a file named `.fbcredentials`.
3. Run `main.py`. On the first run, your web browser will open Imgur and you will be prompted to enter the PIN into the app to get a permanent token (saved to `.imgcredentials`).
4. Enter the album ID you would like to download/upload.
