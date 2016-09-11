from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
import webbrowser
import json

class FbServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request, address, server, app_id, app_secret):
        super().__init__(request, address, server)
        self.app_id = app_id
        self.app_secret = app_secret

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if 'code' in self.path:
            self.server.fb_code = self.path.split("code=")[1].split("&")[0]
            self.wfile.write(bytes("""<html><head>
                <title>Login complete</title>
                <script type="text/javascript">setTimeout(window.close, 1000);</script></head>
                <body><h1>Thanks for logging in! You may now close this window.</h1></body></html>""",
                "utf-8"))
            # TODO else/failure/denied?

    def log_message(self, format, *args):
        '''Suppress log output'''
        return

class FbServer(HTTPServer):
    def __init__(self, server_address, handler):
        super().__init__(server_address, handler)
        self.fb_code = None

class FbOauth:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    def get_access_token(self):
        redirect_uri = "http://localhost:8000/"
        login_url = "https://www.facebook.com/dialog/oauth?client_id=" \
            + self.app_id + "&redirect_uri=" + redirect_uri \
            + "&scope=user_photos&response_type=code"

        webbrowser.open_new(login_url)
        server = FbServer(('localhost', 8000),
            lambda request, address, server: FbServerHandler(request, address,
                server, self.app_id, self.app_secret))
        server.handle_request()
        
        if server.fb_code is not None:
            # Exchange code for a token
            token_url = "https://graph.facebook.com/v2.3/oauth/access_token?client_id=" \
                + self.app_id + "&redirect_uri=" + redirect_uri \
                + "&client_secret=" + self.app_secret + "&code=" + server.fb_code
            result = urlopen(token_url).read().decode("utf-8")
            token = json.loads(result)['access_token']
        else:
            print("\nFacebook server did not get code :(")
            # TODO throw error?
            token = None

        return token
