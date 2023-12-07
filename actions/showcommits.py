import logging

from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger(__name__)


class ShowCommits(Action):
    async def run(self) -> [Result, None]:
        try:
            repo = self.gh.get_repo(self.repo)
            commits = repo.get_commits()
            for commit in commits:
                logging.debug(commit)
            return Result(self.name, 'Ok', 0)
        except:
            logger.exception('Exception')
            return Result(self.name, 'Exception', 1)


def build(name: str, repo, gh, args):
    return ShowCommits(name, repo, gh, args)
