from github import Github
from result import Result
from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self, name: str, repo: str, gh: Github, args):
        self._name = name
        self.repo = repo
        self.gh = gh
        self.args = args

    @abstractmethod
    async def run(self) -> Result:
        pass

    @property
    def name(self) -> str:
        return self._name
