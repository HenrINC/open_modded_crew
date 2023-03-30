import json
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

    def on_post(self, posts):
        try:
            with open(self.archive_path, 'r') as file:
                archive = json.load(file)
        except:
            archive = []
        for post in posts[10:]:
            if post["type"] == "wrote_crew_wall_message" and post["content"].startswith("/"):
                for comment in post["comments"]:
                    if int(comment["actor"]["id"]) == self.connector.get_self_player().id:
                        self.connector.delete_post(post_id=post["id"])
                        archive.append(post)
                        break
        with open(self.archive_path, "w") as file:
            json.dump(archive, file)

    def start(self):
        self.running = True
