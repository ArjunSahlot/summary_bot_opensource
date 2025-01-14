from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

class NoFileAccessHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_error(403, "Forbidden")
    
    def do_POST(self):
        self.send_error(403, "Forbidden")

server = TCPServer(("", 8000), NoFileAccessHTTPRequestHandler)
