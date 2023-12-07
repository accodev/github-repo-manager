import logging

from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger(__name__)


class ShowCommits(Action):
    async def run(self) -> [Result, None]:
        try:
            commits = self.repo.get_commits()
            for commit in commits:
                logging.debug(commit)
            return Result(self.name, 'Ok', 0)
        except GithubException:
            logger.exception('GithubException')
            return Result(self.name, 'Exception', 1)


def build(name: str, repo):
    return ShowCommits(name, repo)
