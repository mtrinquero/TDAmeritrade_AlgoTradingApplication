## Mark Trinquero
## TD Ameritrade Python Trading Bot
## ----------------------------------------
## Authentication Code
## Reference: https://developer.tdameritrade.com/content/authentication-sample-python-3

## In Browser Testing
## https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=Redirect URI&client_id=OAuth User ID

## ----------------------------------------
## Setup Notes

## Generating a self-signed certificate
## The openssl command below will generate key and certificate files you will need later. Put them in a location accessible to the Node app.

## openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
## Note: this is specific to apps running on the local machine, a response is sent to the browser only to show it's working.

## Setting up the Python environment
## Create a directory for this app and run the commands below
## python -m pip install requests

## ----------------------------------------



from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import ssl

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #Get the Auth Code
        path, _, query_string = self.path.partition('?')
        code = parse_qs(query_string)['code'][0]

        #Post Access Token Request
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'authorization_code', 'access_type': 'offline', 'code': code, 'client_id': 'OAuth User ID', 'redirect_uri': 'Redirect URI'}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        
        #returned just to test that it's working
        self.wfile.write(authReply.text.encode())

httpd = HTTPServer((Host for Server to Listen On, Port of Redirect URI), Handler)

#SSL cert
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile='path/to/key.pem', 
        certfile='path/to/certificate.pem', server_side=True)

httpd.serve_forever()