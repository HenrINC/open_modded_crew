from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser

class Command(LazyCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = ArgumentParser()
        self.parser.add_argument("-add")
        self.parser.add_argument("--rank", default=0, type=int)
        self.parser.add_argument("-reload", action="store_true")
        self.parser.add_argument("-list", action="store_true")
        self.parser.add_argument("-update")
    
    def _run(self, namespace, member:CrewMember):
        ranks = ["Leader", "Commissioner", "Lieutenant", "Representative", "Muscle"]
        if namespace.add:
            self.crew.add_command_to_cfg(namespace.add, namespace.rank)
            return f"Command [{namespace.add}] added successfully for rank [{ranks[namespace.rank]}] and higher"
        elif namespace.update:
            self.crew.command_config[namespace.update]["rank"] = namespace.rank
            return f"Command [{namespace.update}] updated successfully for rank [{ranks[namespace.rank]}] and higher"
        elif namespace.list:
            return ",".join(["/"+command.name for command in self.crew.commands])
        elif namespace.reload:
            self.crew.reload_commands()
