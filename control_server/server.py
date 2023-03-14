from http.server import BaseHTTPRequestHandler, HTTPServer
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from typing import Optional
import json


class BaseControlServer(BaseHTTPRequestHandler):
    last_screenshot:Optional[bytes] = None
    password:int = -1
    driver:Optional[webdriver.Chrome] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if str(self.password) in self.path:
            if "tab" in self.path:
                webdriver.ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                return None

            if "enter" in self.path:
                webdriver.ActionChains(self.driver).send_keys(Keys.ENTER).perform()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
                return None
            
            if "img" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.send_header("Cache-control", "max-age=0, must-revalidate")
                self.end_headers()
                self.wfile.write(self.driver.get_screenshot_as_png())
                return None
            
        with open("control_server/dashboard.html", "rb") as file:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(file.read())
        return None

def get_control_server(
        drvr:webdriver.Chrome,
        host="0.0.0.0",
        port=2555) -> HTTPServer:
    class ControlServer(BaseControlServer):
        password = id(host)+id(port)
        driver = drvr
    
    webServer = HTTPServer((host, port), ControlServer)
    print(f"Control server started http://{host}:{port}")
    webServer.debug_password = ControlServer.password
    return webServer

    
