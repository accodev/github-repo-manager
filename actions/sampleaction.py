import logging

from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger()


class SampleAction(Action):
    async def run(self) -> [Result, None]:
        try:
            commits = self.repo.get_commits()
            for commit in commits:
                logging.debug(commit)
        except GithubException:
            logger.exception('GithubException')


def build(name: str, repo):
    return SampleAction(name, repo)