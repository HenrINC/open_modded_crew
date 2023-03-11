from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser

class Command(LazyCommand):
    
    name = "service"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument("-list", action="store_true")
        self.parser.add_argument("-status")
        self.parser.add_argument("-add")
        self.parser.add_argument("-remove")
        self.parser.add_argument("-start")
        self.parser.add_argument("-stop")
        self.parser.add_argument("-reload", action="store_true")
        self.parser.add_argument("--force", action="store_true")
        self.parser.add_argument("--hook")
    
    def _run(self, namespace, member:CrewMember):
        if namespace.list:
            ret = ["Unhooked : "+" , ".join([repr(service) for service in self.crew.services["free"]])]
            for hook, services in self.crew.services["hooked"].items():
                ret.append(f"Hooked on [{hook}] : "+" , ".join([repr(service) for service in services]))
            return " | ".join(ret)
        
        elif namespace.status:
            service_name = namespace.status
            for service in self.crew.get_services_list():
                if service_name == service.name:
                    return service.get_status()
            return f"Found no service with name {service_name}"
        
        elif namespace.add:
            service_name = namespace.add
            self.crew.add_service_to_cfg(service_name, namespace.hook)
        
        elif namespace.remove:
            self.crew.remove_service_from_cfg(service_name, namespace.hook)
        
        elif namespace.start:
            service = self.crew.get_service_from_name(service_name, namespace.hook)
            service.start()

        elif namespace.stop:
            service = self.crew.get_service_from_name(service_name, namespace.hook)
            service.stop()
        
        elif namespace.reload:
            self.crew.relaod_services()

