from abc import ABC, abstractmethod
from common import Crew, Connector
from threading import Thread

class AbstractService(ABC):
    """
    A service is an object that can interact with a crew object
    it mainly works by waiting for some time, reading/settign crew propreties,
    repeating the cycle
    """

    def __init__(self, crew:Crew, connector:Connector, name:str):
        self.crew:Crew = crew
        self.connector:Connector = connector
        self.name = name
        self.running = False
        self.thread = None
    
    def __repr__(self):
        return f"<{self.name}>"

    def get_status(self):
        return f"[Loop :{'' if self.running else ' not'} running]"
    
    def _loop(self):
        self.stop()
    
    def loop(self):
        while self.running:
            self._loop()
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            if self.thread is None:
                self.thread = Thread(target=self.loop, name = f"{self.crew.name}-{self.name}-loop")
                self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread is not None:
            try:
                self.thread.join()
                self.thread = None
            except:
                pass
