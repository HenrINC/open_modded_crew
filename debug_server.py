from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional, Type

class DebugServer(BaseHTTPRequestHandler):

    #TODO use a factory

    last_screenshot:Optional[bytes] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def do_GET(self, request):
        if self.last_screenshot is None:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("""
<html>
    <head>
        <title>No screenshot</title>
    </head>
    <body>
        <h1>ERROR : No screenshot</h1>
    </body>
</html>
            """.encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(self.last_screenshot)


def start_debug_server(host="0.0.0.0", port=80) -> Type[DebugServer]:
    webServer = HTTPServer((host, port), DebugServer)
    print("Server started http://%s:%s" % (host, port))
    webServer.serve_forever()
    return DebugServer

