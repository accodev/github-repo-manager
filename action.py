from github import Repository
from result import Result
from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self, name: str, repo: Repository):
        self._name = name
        self.repo = repo

    @abstractmethod
    async def run(self) -> [Result, None]:
        pass

    @property
    def name(self) -> str:
        return self._name
