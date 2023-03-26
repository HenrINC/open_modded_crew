"""
Abstract class with more tools that works for most commands
"""
from commands.abstract_command import AbstractCommand
from common import CrewMember
from argparse import ArgumentParser
from abc import abstractmethod

class LazyCommand(AbstractCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = ArgumentParser()
        
    def run(self, args, member:CrewMember):
        try:
            if member.get_rank(self.crew) <= self.min_rank:
                namespace = self.parser.parse_args(args)
                return self._run(namespace, member)
            else:
                ranks = ["Leader", "Commissioner", "Lieutenant", "Representative", "Muscle"]
                return f"Command [{self.name}] is only avialable for rank {ranks[self.min_rank]} \
                    and higher but your rank is [{member.get_rank(self.crew)}]"
        except SystemExit as e:
            return "Error: parsing arguments failed"

    @abstractmethod
    def _run(namespace, member:CrewMember):
        raise NotImplementedError()
