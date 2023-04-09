from services.abstract_service import AbstractService
import logging
import time
import threading

class Service(AbstractService):
    """
    Builtin service on which other services can hook
    so multiple services can only request data once 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hooks = {
            "post": {
                "last_call": 0,
                "frequency": 5,
                "callback": self.crew.get_wall_posts,
                "iterable": True,
                "thread": None,
            },
            "crew_notification": {
              "last_call": 0,
              "frequency": 5,
              "callback": self.crew.get_notifications,
              "iterable": True,
              "thread": None,
            },
            "style": {
                "last_call": 0,
                "frequency": 300,
                "callback": self.crew.get_style,
                "iterable": False,
                "thread": None,
            }
        }
        
    def trigger_hooked_services(self, hook, hook_data):
        for i, hook_data_chunk in enumerate(hook_data):
            for service in self.crew.services:
                if hasattr(service, f"on_{hook}_max_size"):
                    if i > getattr(service, f"on_{hook}_max_size"):
                        continue
                if service.running and hasattr(service, f"on_{hook}"):
                    try:
                        getattr(service, f"on_{hook}")(hook_data_chunk)
                    except Exception as e:
                        logging.error(
                            f"Could not call [{service}]'s [on_{hook}]"
                            f"with [{hook_data_chunk}] because of [{type(e)}: {e}]"
                        )
        
    def _loop(self):
        for hook, hook_cfg in self.hooks.items():
            if time.time() - hook_cfg["last_call"] > hook_cfg["frequency"]:
                if hook_cfg["thread"] is None or not hook_cfg["thread"].is_alive():
                    hook_cfg["last_call"] = time.time()
                    try:
                        hook_data = hook_cfg["callback"]()
                    except Exception as e:
                        logging.error(f"Could not get info for hook [{hook}] because of [{type(e)}: {e}]")
                        continue
                
                    if not hook_cfg["iterable"]:
                        hook_data = [hook_data]
                    
                    thread = threading.Thread(
                        target=self.trigger_hooked_services,
                        args=(hook, hook_data),
                        name=f"Hook [{hook}]'s trigger service",
                    )

                    thread.start()
                    hook_cfg["thread"] = thread
