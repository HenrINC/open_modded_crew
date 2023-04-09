from commands.lazy_command import LazyCommand
from common import CrewMember
from argparse import ArgumentParser
import random

class Command(LazyCommand):
    
    name = "coinflip"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _run(self, namespace, member:CrewMember):
        return random.choice(["heads", "tails"])