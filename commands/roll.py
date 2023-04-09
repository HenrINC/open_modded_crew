from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser
import random

class Command(LazyCommand):
    
    name = "roll"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument("-max", type=int, default=6)
    
    def _run(self, namespace, member:CrewMember):
        return random.randint(1, namespace.max)