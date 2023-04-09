
import json
from services.abstract_service import AbstractService
from common import CrewMember
from datetime import datetime

class Service(AbstractService):
    """
Builtin service that archives the commands sent to the bot in an file
This keeps the crew chat clean  
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = f"services/{self.crew.name}-tracking.json"
        try:
            with open(self.data_path, 'r') as file:
                self.tracking_data = json.load(file)
        except:
            self.tracking_data = {}
        
        self.processed_since_last_save = 0

    def on_crew_notification(self, notification):
        actor = notification["actor"]
        if actor["id"] not in self.tracking_data:
            self.tracking_data[actor["id"]] = {
                "id": actor["id"],
                "name": actor["name"],
                "invite_sent": [],
                "invite_accepted": [],
                "last_performance": 0,
                "joined_at": 0,
                "left": False
            }
        actor_data = self.tracking_data[actor["id"]]

        if notification["type"] == "crew_joined_notif_agg":
            actor_data["joined_at"] = datetime.strptime(
                notification["notif"]["time"],
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ).timestamp()
            for member_id, member_data in self.tracking_data.items():
                if actor["id"] in member_data["invite_sent"]:
                    member_data["invite_accepted"].append(actor["id"])
        
        elif notification["type"] == "crew_invite_notif_agg":
            for invitee in notification["notif"]["participants"]:
                if invitee not in actor_data["invite_sent"]:
                    actor_data["invite_sent"].append(invitee["id"])
        
        elif notification["type"] == "crew_left_notif_agg":
            actor_data["left"] = True



        if self.processed_since_last_save > 10:
            self.processed_since_last_save = 0  
            with open(self.data_path, "w") as file:
                json.dump(self.tracking_data, file, indent=2)

    def start(self):
        self.running = True