import logging
from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger(__name__)


class RepoStars(Action):
    async def run(self) -> Result:
        try:
            repo = self.gh.get_repo(self.repo)
            logging.debug(repo.stargazers_count)
            return Result(self.name, 'Ok', 0)
        except:
            logger.exception('Exception')
            return Result(self.name, 'Exception', 1)


def build(name: str, repo, gh, args):
    return RepoStars(name, repo, gh, args)
