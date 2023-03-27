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
    
    def _run(self, namespace, member:CrewMember):
        if namespace.list:
            return ", ".join([repr(service) for service in self.crew.service])
        
        elif namespace.status:
            service_name = namespace.status
            for service in self.crew.services:
                if service_name == service.name:
                    return service.get_status()
            return f"Found no service with name {service_name}"
        
        elif namespace.add:
            service_name = namespace.add
            self.crew.add_service_to_cfg(service_name)
        
        elif namespace.remove:
            self.crew.remove_service_from_cfg(service_name)
        
        elif namespace.start:
            service = self.crew.get_service_from_name(service_name)
            service.start()

        elif namespace.stop:
            service = self.crew.get_service_from_name(service_name)
            service.stop()
        
        elif namespace.reload:
            self.crew.reload_services()

