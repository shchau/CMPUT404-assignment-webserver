#  coding: utf-8 
import socketserver
import os

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

		if (request):
			print ("Got a request of: %s\n" % request)
			requestDetails = request.split(" ")

			#self.request.sendall(bytearray("OK",'utf-8'))

			status = "HTTP/1.1 200 OK\n"
			contentType = "Content-Type: text/html\n\n"		

			if '.css' in request:
				contentType = "Content-Type: text/css\n\n"


			FilePath = requestDetails[1]
			if ("etc" not in FilePath):
				if FilePath[-1] == "/" :
					FilePath = requestDetails[1] + "index.html"

				try:
					File = open('./www/' + FilePath, "r").read()
				except:
					status = 'HTTP/1.1 404 Not Found\r\n'
					contentType = ''
					File = "404 - Not Found"
			else:
				status = 'HTTP/1.1 404 Not Found\r\n'
				contentType = ''
				File = "404 - Not Found"
			Response = status + contentType + File			
			if "GET" not in request:
				Response = "HTTP/1.1 405 Method Not Allowed\n"

			print("Response == %s\n", Response)
			self.request.sendall(bytearray(Response,'utf-8'))	


if __name__ == "__main__":
	HOST, PORT = "localhost", 8080

	socketserver.TCPServer.allow_reuse_address = True
	# Create the server, binding to localhost on port 8080
	server = socketserver.TCPServer((HOST, PORT), MyWebServer)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
