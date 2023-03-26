from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser
import requests

class Command(LazyCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument("--lang", default="en")
    
    def _run(self, namespace, member:CrewMember):
        url = f"https://v2.jokeapi.dev/joke/Miscellaneous,Pun?lang={namespace.lang}&blacklistFlags=nsfw,racist,sexist,explicit&type=single"
        response = requests.get(url).json()
        if "joke" in response:
            return response["joke"]
        else:
            return "ERROR:"+response["additionalInfo"]