# simple server to serve video and get around cors.
# copied from: https://stackoverflow.com/a/21957017
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import json
import sys
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os
import re

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):

        now = datetime.now()
        stamp = mktime(now.timetuple())
        format_date_time(stamp)

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Expires', format_date_time(stamp)) # prevent caching
        SimpleHTTPRequestHandler.end_headers(self)
    def do_GET(self):
        # list endpoint, get all video files available
        if self.path == '/list':
            files = os.listdir('./')
            vid_files = list(filter(lambda s: re.match(r'clip.*\.mp4',s) != None, files))
            res = json.dumps(vid_files)
            self.send_response(200)
            self.send_header("Content-length", len(res))
            self.end_headers()
            self.wfile.write(str.encode(res))
            print("helloo")
        

        SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)