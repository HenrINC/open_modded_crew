from services.abstract_service import AbstractService
import time
import random

class Service(AbstractService):
    """
    Builtin service that executes the commands
    """

    def on_style(self, style):
        self.crew.update_style()
    
    def _loop(self):
        if "style_service_delay" in self.crew.service_config:
            delay = self.crew.service_config["style_service_delay"]
        else:
            delay = 300
        if "style_service_config" in self.crew.service_config:
            style = self.style_config_to_style(self.crew.service_config["style_service_config"])
            self.crew.set_style(style)
        time.sleep(delay)
    
    def style_config_to_style(self, style_config:dict[str, list[str]]):
        style = style_config.copy()
        for key in style.keys():
            style[key] = random.choice(style[key])
        return style