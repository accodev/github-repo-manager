import logging

from action import Action
from result import Result
from github.GithubException import *


logger = logging.getLogger(__name__)


class CreatePrivateRepo(Action):
    def get_owner(self):
        try:
            return self.gh.get_user(self.args.owner)
        except GithubException:
            try:
                return self.gh.get_organization(self.args.owner)
            except GithubException:
                return None

    async def run(self) -> Result:
        try:
            owner = self.get_owner()
            repo = owner.create_repo(self.repo, private=True)
            logging.debug(repo)
            return Result(self.name, 'Ok', 0)
        except:
            logger.exception('Exception')
            return Result(self.name, 'Exception', 1)


def build(name: str, repo, gh, args):
    return CreatePrivateRepo(name, repo, gh, args)
