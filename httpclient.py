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

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        #TODO error handle?
        return socket.create_connection((host,port))

    def get_code(self, data):
        return data.split()[1]

    def get_headers(self, method, url_data):
        #request line ex. GET / HTTP/1.1
        request = method
        if url_data.path == None:
            request += " / "
        else:
            request += " " + url_data.path
        request += " HTTP/1.1\r\n"
        ##host
        host = "Host: " + url_data.netloc + "\r\n"
        ### connection  maybe????
        connect_message = "Connection: Close\r\n"
        ###Accept
        accept = "*/*\r\n"
        ####
        header = request + host + connect_message + accept + "\r\n"

        return header

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
        url_data = urlparse.urlparse(url)
        connection = self.connect(url_data.hostname, url_data.port)
        header = self.get_headers("GET", url_data)
        ####TODO add try
        connection.sendall(header)
        response = self.recvall(connection)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

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
        print client.command( command, sys.argv[1] )    
