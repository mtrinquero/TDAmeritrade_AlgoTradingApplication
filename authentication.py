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