from services.abstract_service import AbstractService
import time
import random

class Service(AbstractService):
    """
    Builtin service that executes the commands
    """
    last_update = 0

    def on_style(self, style):
        self.crew.update_style()
    
    def _loop(self):
        if "delay" in self.crew.service_config:
            delay = self.crew.service_config["delay"]
        else:
            delay = 300
        if self.last_update + delay < time.time(): 
            if "style" in self.crew.service_config["style"]:
                style = self.style_config_to_style(self.crew.service_config["style"]["style"])
                self.crew.set_style(style)
            self.last_update = time.time()
    
    def style_config_to_style(self, style_config:dict[str, list[str]]):
        style = style_config.copy()
        for key in style.keys():
            style[key] = random.choice(style[key])
        return style