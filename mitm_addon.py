import logging

class ShowToken:
    """def requestheaders(self, flow):
        headers = flow.request.headers
        for header in headers:
            if header == "__RequestVerificationToken":
                logging.info("VerifToken: "+headers[header])"""
    def response(self, flow):
        content = flow.response.content
        if b"__RequestVerificationToken" in content:
            if "js" not in flow.request.path:
                content = content.decode()
                token = content.split("__RequestVerificationToken")[1].split("value=")[1].split(" ")[0].strip('"')
                logging.info("VerifToken: "+token)
                with open("verif_token.txt", "w") as file:
                    file.write(token)

class AlwaysEN:
    def requestheaders(self, flow):
        flow.request.headers["Accept-Language"] = "en-US,en;q=0.9"

addons = [ShowToken(), AlwaysEN()]
