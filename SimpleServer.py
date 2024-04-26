#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import argparse

class CustomRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
        self.verbose_output()

    def verbose_output(self):
        if not args.verbose:
            return
        for header, value in self.headers.items():
            print(f'\t{header}: {value}')

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        file_to_open = ''
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except FileNotFoundError:
            self.send_response(404)
        except:
            self.send_response(500)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self._send_response("Received POST request with data:\n{}".format(post_data))
        if post_data and post_data != '':
            print(f'\t{post_data}')
       

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Server is running on port {port}")
    httpd.serve_forever()
    
parser = argparse.ArgumentParser(
    prog='SimpleServer.py',
    description="A simple extension of Python's http.server module. Serves files in the local directory, but also prints request data to the host.",
    epilog='Author: 4wayhandshake 🤝🤝🤝🤝')
    
parser.add_argument('port', nargs='?', default=8000, help='The port to listen on.', type=int)
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Output extra information. Use this to see all incoming request headers.')
args = parser.parse_args()

if __name__ == '__main__':
    run_server(args.port)
