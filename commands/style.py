from commands.lazy_command import LazyCommand
from common import CrewMember, fix_style_property_value
from base64 import b32decode
import json

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
        style = self.crew.get_style()
        
        if "style" not in self.crew.service_config["style"]: 
            self.crew.service_config["style"]["style"] = self.style_to_style_config(style)

        style_config = self.crew.service_config["style"]["style"]

        if namespace.value is not None:
            if namespace.base32:
                namespace.value = b32decode(value, casefold=True).decode()
            namespace.value = fix_style_property_value(namespace.value)
        if namespace.set or namespace.add or namespace.get:
            if namespace.property is None:
                old_cfg = style_config.copy()
                if namespace.get:
                    return f"[SUCCESS] {old_cfg}"
                elif namespace.set:
                    new_style_cfg = self.style_to_style_config(style)
                elif namespace.add:
                    new_style_cfg = self.add_style_to_style_config(style_config, style)
                else:
                    raise ValueError("Namespace asynchronously modified")
                style_config.update(new_style_cfg)
                self.crew.save_config()
                return f"[SUCCESS] {old_cfg} => {new_style_cfg}"

            else:
                if namespace.property not in style:
                    raise ValueError(
                        f"The property \"{namespace.property}\" is not a style property,"
                        f"available properties are : {list(style_config.keys())}")
                
                if namespace.value is None:
                    value = style[namespace.property]
                else:
                    value = namespace.value
                old_value = style_config[namespace.property].copy()
                if namespace.get:
                    return f"[SUCCESS]{namespace.property} : {old_value}"
                
                elif namespace.set:
                    style_config[namespace.property] = [value]
                elif namespace.add:
                    style_config[namespace.property].append(value)
                else:
                    raise ValueError("Namespace asynchronously modified")
                self.crew.save_config()
                return f"[SUCCESS]{namespace.property} : {old_value} => \
                    {style_config[namespace.property]}"                    
                

        elif namespace.remove:
            if namespace.property is None:
                raise ValueError("Argument \"property\" is required")
            if namespace.value is None:
                raise ValueError("Argument \"value\" is required")
        
        elif namespace.set_delay is not None:
            self.crew.service_config["style"]["delay"] = namespace.set_delay
    
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

