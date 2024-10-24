#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import argparse
from urllib.parse import urlparse, parse_qs
import base64
import os


def extract_b64_data(querystring):
    parsed_query = parse_qs(querystring)
    if 'b64' in parsed_query:
        b64_value = parsed_query['b64'][0]
        # Find the first equals sign in the remaining part after 'b64='
        #second_equals_pos = b64_value.find('=')
        #if second_equals_pos != -1:
            # Extract the desired part between the second equals sign and the end
            #extracted_data = b64_value[second_equals_pos + 1:]
            #return extracted_data
        #else:
        #    return b64_value
        return b64_value
    return None


def try_b64_decode(s):
    decoded = None
    for i in range(3):  # try with no padding, one padding character, or two padding characters
        try:
            decoded = base64.b64decode(s + '=' * i).decode('utf-8')
            break
        except Exception:
            continue
    return decoded


def decode_base64(b64_data):
    # If there are no periods in the data (ex. a jwt), just decode it
    if '.' not in b64_data:
        return try_b64_decode(b64_data)
    # Otherwise, split on the periods and decode the chunks
    parts = b64_data.split('.')
    decoded_parts = []
    for part in parts:
        decoded_part = try_b64_decode(part)
        if decoded_part is not None:
            decoded_parts.append(decoded_part)
    return decoded_parts


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
        qstring_start = self.path.find('?')
        if qstring_start != -1:
            resource = self.path[:qstring_start]
        else:
            resource = self.path
        if resource == '' or resource == '/':
            resource = '/index.html'
        filepath = os.path.join(os.getcwd(), resource[1:])
        try:
            file_to_open = open(filepath, 'rb').read()
            self.send_response(200)
        except FileNotFoundError:
            self.send_response(404)
        except Exception as e:
            self.send_response(500)
            print(f'An exception occurred while processing a GET request:\n{e}')
        self.end_headers()
        try:
            self.wfile.write(bytes(file_to_open))
        except TypeError:
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        except Exception as e:
            self._send_response(500, b'Failed to parse requested resource.\r\n')
        self.verbose_output()
        b64_data = extract_b64_data(urlparse(self.path).query)
        if b64_data is not None:
            decoded = decode_base64(b64_data)
            if decoded is not None and decoded != []:
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
                self._send_response(200, b'File uploaded successfully.\r\n')
                self.verbose_output()
                print(('\n' if args.verbose else '') + f'\tFile uploaded: {filename}')
            except Exception as e:
                self._send_response(500, b'Server error occurred while uploading file.\r\n')
                self.verbose_output()
                print(f'\tFile failed to upload.')                    
        else:
            self._send_response(200, b'POST data received.\r\n')
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
