#  coding: utf-8 
import socketserver

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
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		request = self.data.decode("utf-8").split("\r\n")[0]

		print ("Got a request of: %s\n" % request)
		#self.request.sendall(bytearray("OK",'utf-8'))

		status = "HTTP/1.1 200 OK\n"
		contentTypeHTML = "Content-Type: text/html\n\n"		
		indexPath = "./www/index.html" 
		if 'deep' in request:
			indexPath = "./www/deep/index.html"

		htmlFile = open(indexPath, "r").read()
		Response = status + contentTypeHTML + htmlFile

		if 'css' in request:
			cssPath = "./www/base.css"
			if 'deep' in request:
				cssPath = "./www/deep/deep.css"

			cssFile = open(cssPath, "r").read()
			contentTypeCSS = "Content-Type: text/css\n\n"
			Response = status + contentTypeCSS + cssFile	

		
		if "GET" not in request:
			Response = "HTTP/1.1 405 Method Not Allowed\n"


		self.request.sendall(bytearray(Response,'utf-8'))	
		#if '/deep/index.html' in str(self.data):
			#htmlFile = open(deeperPath, "r").read()
			#self.request.send((status + htmlFile).encode('utf-8'))


if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
