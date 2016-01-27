#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class myParseUrl(object):
    def __init__(self, url):
        p = '(?:http://)?(?P<host>[^:/ ]+):?(?P<port>[0-9]*)(?P<path>.*)'
        m = re.search(p,url)
        self.hostname = m.group('host') 
        self.port = m.group('port')
        self.path = m.group('path')
        self.netloc = self.hostname+":"+self.port
        if not self.port:
            self.port = 80
        if not self.path:
            self.path = "/"


class HTTPClient(object):
    def connect(self, host, port):
        conn = socket.create_connection((host,port))
        return conn

    def get_code(self, data):
        return data.split()[1]

    def get_headers(self, method, url_data, args=None):
        request = "%s %s HTTP/1.1\r\n" %(method, url_data.path)
        request += "Host: %s\r\n" %(url_data.hostname)
        request += "Connection: Close\r\n" 
        if args is not None:
            params = urllib.urlencode(args)
            request += "Content-Type: "
            request += "application/x-www-form-urlencoded\r\n"
            request += "Content-Length: %d\r\n" %(len(params))
            request += "\r\n%s\r\n" %(params)
        request += "\r\n"
        return request

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        url_data = myParseUrl(url)
        connection = self.connect(url_data.hostname, url_data.port)
        header = self.get_headers("GET", url_data)
        connection.sendall(header)
        response = self.recvall(connection)
        code = self.get_code(response)
        body = self.get_body(response)
        connection.close()
        return HTTPResponse(int(code), body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        url_data = myParseUrl(url)
        connection = self.connect(url_data.hostname, url_data.port)
        header = self.get_headers("POST", url_data, args)
        connection.sendall(header)
        response = self.recvall(connection)
        code = self.get_code(response)
        body = self.get_body(response)
        connection.close()
        return HTTPResponse(int(code), body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1], command) 
