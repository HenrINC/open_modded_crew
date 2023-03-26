from abc import ABC, abstractmethod
from common import CrewMember, Crew, Connector

class AbstractCommand(ABC):
    """
    A command is an abject that can interct with a crew and it's sender
    """

    def __init__(self, crew:Crew, connector:Connector, name:str, min_rank:int=0):
        self.crew = crew
        self.name = name
        self.min_rank = min_rank
        self.connector = connector

    @abstractmethod
    def run(self, args:list[str], actor:CrewMember):
        """
        Args is the result of a shlex.split
        it's a good idea to parse it with arparse
        """
        raise NotImplementedError()

    def __repr__(self):
        return f"<Command {self.name}>"