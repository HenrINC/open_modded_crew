import json
import time
from services.abstract_service import AbstractService

class Service(AbstractService):
    """
Builtin service that archives the commands sent to the bot in an file
This keeps the crew chat clean  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed: list[str]
        self.archive_path = f"services/{self.crew.name}-archive.json"
        try:
            with open(self.archive_path, 'r') as file:
                self.archive = json.load(file)
        except:
            self.archive = []
        
        self.processed_since_last_save = 0

    def on_post(self, post):
        
        if post["type"] == "wrote_crew_wall_message"\
        and post["content"].startswith("/")\
        and post["time"] + 600 < time.time():
            for comment in post["comments"]:
                if int(comment["actor"]["id"]) == self.connector.get_self_player().id:
                    self.connector.delete_post(post_id=post["id"])
                    self.archive.append(post)
                    self.processed_since_last_save += 1
                    break
        if self.processed_since_last_save > 10:
            self.processed_since_last_save = 0
            with open(self.archive_path, "w") as file:
                json.dump(self.archive, file)

    def start(self):
        self.running = True
