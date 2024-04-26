#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import argparse
from urllib.parse import urlparse, parse_qs
import base64

class CustomRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, message):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message)

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
        except Exception as e:
            self.send_response(500)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
        self.verbose_output()
        # make a dict from the query string
        query_params = parse_qs(urlparse(self.path).query)
        if 'b64' in query_params:
            b64data = query_params['b64'][0]
            decoded = None
            for i in range(2):
                try:
                    decoded = base64.b64decode(b64data + ('='*i)).decode('utf-8')
                    break
                except:
                    continue
            if decoded is not None:
                print(('\n' if args.verbose else '') + f'\tDecoded base-64 data from query string:\n\n{decoded}')
        print("")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        content_type = self.headers.get('Content-Type')
        if content_type and content_type.startswith('multipart/form-data'):
            try:
                boundary = content_type.split('; boundary=')[1]
                parts = post_data.split(boundary.encode())[1:-1]
                filename = ''
                for part in parts:
                    # Extract filename and content from each part
                    filename = part.split(b'\r\n')[1].split(b';')[-1].split(b'=')[-1].decode().strip('"')
                    file_content = part.split(b'\r\n\r\n')[1]
                    # Write file content to a file
                    with open(filename, 'wb') as f:
                        f.write(file_content)
                self._send_response(200, b'File uploaded successfully.')
                self.verbose_output()
                print(('\n' if args.verbose else '') + f'\tFile uploaded: {filename}')
            except Exception as e:
                self._send_response(500, b'Server error occurred while uploading file.')
                self.verbose_output()
                print(f'\tFile failed to upload.')                    
        else:
            self._send_response(200, b'POST data received.')
            self.verbose_output()
            if post_data and post_data != '':
                print(('\n' if args.verbose else '') + f'\t{post_data.decode("utf-8")}')
        print("")
        
       

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Server is running on port {port}\n")
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
