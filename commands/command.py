from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser

class Command(LazyCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = ArgumentParser()
        self.parser.add_argument("-add")
        self.parser.add_argument("--min_rank", default=0, type=int)
        self.parser.add_argument("-reload", action="store_true")
        self.parser.add_argument("-list", action="store_true")
        self.parser.add_argument("-change_rank")
    
    def _run(self, namespace, member:CrewMember):
        ranks = ["Leader", "Commissioner", "Lieutenant", "Representative", "Muscle"]
        if namespace.add:
            self.crew.add_command_to_cfg(namespace.add, namespace.min_rank)
            return f"Command [{namespace.add}] added succesfully for rank [{ranks[namespace.min_rank]}] and higher"
        elif namespace.change_rank:
            self.crew.command_config[namespace.change_rank]["min_rank"] = namespace.min_rank
            return f"Command [{namespace.change_rank}] changed succesfully for rank [{ranks[namespace.min_rank]}] and higher"
        elif namespace.list:
            return ",".join(["/"+command.name for command in self.crew.commands])
        elif namespace.reload:
            self.crew.reload_commands()
