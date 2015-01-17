import SocketServer
import os.path
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/ 



class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        # parse incoming request
        self.data = self.request.recv(1024).strip()
        Splitdata =  self.data.splitlines()
        Firstword = Splitdata[0].split()
      	
        #variables used / premade HTTP 
    	style = ""
    	respmes = ""
        HTTP200 = "HTTP/1.1 200 OK\n" + "Content-type: text/"
        reHTTP200 = "HTTP/1.1 200 OK\r\n"+ "Location: http://127.0.0.1:8080/\r\n\r\n"
        HTTP301 = "HTTP/1.1 301 Moved Permanently\r\n"+ "Location: http://127.0.0.1:8080/deep/\r\n\r\n"
        HTTP404 = "HTTP/1.1 404 Not Found\n"+"Content-Type: text/html\n\n"+"<!DOCTYPE html>\n"+"<html><body>HTTP/1.1 404 Not Found\n"+"Not found on server directory</body></html>"
        
        #get pathway requested
        pathway = os.getcwd() + "/www"+ Firstword[1]
	
        #see if what is being requested is a css or html
        style = pathway.split(".")[-1].lower()
        
        #check if pathway is a file and check if the requested pathway is in what the file return as path /../
        if (os.path.isfile(pathway) and os.getcwd() in os.path.realpath(pathway)):
                #message to client opens html or css and open file requested
                respmes = (HTTP200+style+"\n\n" +open(pathway).read())

        #checks if file is a directory and handles a redirect according to what is inputted , checks path /../
        elif (os.path.isdir(pathway) and os.getcwd() in os.path.realpath(pathway)):
    
            #open index file with format html for first get request from http://127.0.0.1:8080
            if Firstword[1].endswith("/"):
            	pathway = pathway+"index.html"
            	respmes = (reHTTP200+ open(pathway).read())
            else:
                #opens index.html file in deep, redirects http://127.0.0.1:8080/deep to http://127.0.0.1:8080/deep/
                pathway = pathway+"/index.html"
                respmes = (HTTP301+open(pathway).read())

        #doesnt exist! not in deep or was not www index or was not get request
        else:
            respmes = (HTTP404)

        #send response to the client
        self.request.sendall(respmes)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
