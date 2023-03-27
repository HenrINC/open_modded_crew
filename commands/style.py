from commands.lazy_command import LazyCommand
from common import CrewMember, fix_style_property_value
from base64 import b32decode

class Command(LazyCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument("-get", action="store_true")
        self.parser.add_argument("-set", action="store_true")
        self.parser.add_argument("-add", action="store_true")
        self.parser.add_argument("-remove", action="store_true")
        self.parser.add_argument("-drop_duplicates", action="store_true")
        self.parser.add_argument("-set_delay", type=int)
        self.parser.add_argument("--property")
        self.parser.add_argument("--value")
        self.parser.add_argument("--base32", action="store_true")
    
    def _run(self, namespace, member:CrewMember):
        if namespace.value is not None:
            if namespace.base32:
                namespace.value = b32decode(value, casefold=True).decode()
            namespace.value = fix_style_property_value(namespace.value)
        if namespace.set or namespace.add or namespace.get:
            style = self.crew.get_style()
            if namespace.property is None:
                old_cfg = self.crew.service_config["style_service_config"].copy()
                if namespace.get:
                    return f"[SUCCESS] {old_cfg}"
                if namespace.set:
                    new_style_cfg = self.style_to_style_config(style)
                else:
                    if "style_service_config" not in self.crew.service_config:
                        raise ValueError("Style is not configured, please run \"/style -set\"")
                    new_style_cfg = self.add_style_to_style_config(self.crew.service_config["style_service_config"], style)
                self.crew.service_config["style_service_config"] = new_style_cfg
                return f"[SUCCESS] {old_cfg} => {new_style_cfg}"

            else:
                if "style_service_config" not in self.crew.service_config:
                    raise ValueError("Style is not configured, please run \"/style -set\"")
                if namespace.property not in style:
                    raise ValueError(f"The property \"{namespace.property}\" is not a style property,\
                                     available properties are : {list(self.crew.service_config['style_service_config'].keys())}")
                
                if namespace.value is None:
                    value = style[namespace.property]
                else:
                    value = namespace.value
                old_value = self.crew.service_config["style_service_config"][namespace.property].copy()
                if namespace.get:
                    return f"[SUCCESS]{namespace.property} : {old_value}"
                
                if namespace.set:
                    self.crew.service_config["style_service_config"][namespace.property] = [value]
                else:
                    self.crew.service_config["style_service_config"][namespace.property].append(value)
                return f"[SUCCESS]{namespace.property} : {old_value} => \
                    {self.crew.service_config['style_service_config'][namespace.property]}"                    
                

        elif namespace.remove:
            if namespace.property is None:
                raise ValueError("Argument \"property\" is required")
            if namespace.value is None:
                raise ValueError("Argument \"value\" is required")
        
        elif namespace.set_delay is not None:
            self.crew.service_config["style_service_delay"] = namespace.set_delay
    
        self.crew.save_config()

    def style_to_style_config(self, style):
        style = style.copy()
        for key in style.keys():
            style[key] = [style[key]]
        return style
    
    def add_style_to_style_config(self, style_config, style):
        style = style.copy()
        style_config = style_config.copy()
        for key in style.keys():
            style_config[key].append(style[key])
        return style

