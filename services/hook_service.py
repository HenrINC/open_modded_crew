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
                hook_data = hook_cfg["callback"]()
                for service in self.crew.services:
                    


        if "hooked" in self.crew.services:
            
            if self.can_call_hook("posts"):
                hooked_services = self.crew.services["hooked"]["posts"]
                try:
                    posts = self.crew.get_wall_posts()
                    for service in hooked_services:
                        if service.running:
                            service.on_post(posts)
                except:
                    logging.error("Could not get wall posts")
                finally:
                    self.last_hook_call["posts"] = time.time()
                
            if self.can_call_hook("style"):
                hooked_services = self.crew.services["hooked"]["style"]
                try:
                    style = self.crew.get_style()
                    for service in hooked_services:
                        if service.running:
                            service.on_style(style)
                except:
                    print("Could not get style")
                
                finally:
                    self.last_hook_call["style"] = time.time()



