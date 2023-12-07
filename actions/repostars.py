import logging

from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger(__name__)


class RepoStars(Action):
    async def run(self) -> [Result, None]:
        try:
            logging.debug(self.repo.stargazers_count)
            return Result(self.name, 'Ok', 0)
        except GithubException:
            logger.exception('GithubException')
            return Result(self.name, 'Exception', 1)


def build(name: str, repo):
    return RepoStars(name, repo)
