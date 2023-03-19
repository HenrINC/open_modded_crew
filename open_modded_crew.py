from common import Crew, Connector
from _thread import start_new_thread as new_thread
#from services.hook_service import Service as HookService
from services.abstract_service import AbstractService
import time
from services.hook_service import Service as HookService
import json

print("#"*100)
print("#"+f"{'Open Modded Crew Server': ^20}"+"#")
print("#"*100)

with open("config.json", "r") as file:
    config = json.load(file)

connector = Connector()
connector.login(config["email"], config["password"])

crews = []

for crew_name in config["crews"]:
    crew = Crew(name=crew_name, connector=connector)
    crew.load_config()
    crew.relaod_services()
    crew.reload_commands()
    crews.append(crew)

while True:
    time.sleep(1)




