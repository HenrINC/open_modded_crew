from services.abstract_service import AbstractService

import time

class Service(AbstractService):
    """
    Builtin service on which other services can hook
    so multiple services can only request data once 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_hook_call = {
            "posts": 0,
            "style": 0
        }
        self.hook_call_cfg = {
            "posts": 5,
            "style": 300
        }
    def can_call_hook(self, hook):
        return \
            hook in self.crew.services["hooked"] and \
            hook in self.hook_call_cfg and \
            hook in self.last_hook_call and \
            time.time() - self.hook_call_cfg[hook] > self.last_hook_call[hook]
    def _loop(self):
        if "hooked" in self.crew.services:
            
            if self.can_call_hook("posts"):
                hooked_services = self.crew.services["hooked"]["posts"]
                try:
                    posts = self.crew.get_wall_posts()
                    for service in hooked_services:
                        if service.running:
                            service.on_post(posts)
                except:
                    print("Could not get wall posts")
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



