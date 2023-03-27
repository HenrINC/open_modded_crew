from services.abstract_service import AbstractService
import logging
import time

class Service(AbstractService):
    """
    Builtin service on which other services can hook
    so multiple services can only request data once 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hooks = {
            "posts": {
                "last_call": 0,
                "frequency": 5,
                "callback": self.crew.get_wall_posts
            },
            "style": {
                "last_call": 0,
                "frequency": 300,
                "callback": self.crew.get_style()
            }
        }
    def _loop(self):
        for hook, hook_cfg in self.hooks.items():
            if time.time() - hook_cfg["last_call"] > hook_cfg["frequency"]:
                try:
                    hook_data = hook_cfg["callback"]()
                except Exception as e:
                    logging.error(f"Could not get info for hook [{hook}] because of {e}")
                    continue
                for service in self.crew.services:
                    if service.running and hasattr(service, f"on_{hook}"):
                        try:
                            getattr(service, f"on_{hook}")(hook_data)
                        except Exception as e:
                            logging.error(f"Could not call [{service}]'s on_{hook} because of {e}")
                            continue


