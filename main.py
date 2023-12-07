import logging
import logging.config
import argparse
import asyncio
import action_factory
from result import Result
from github import Github, Auth


logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


def validate_args(args):
    if not isinstance(args.token, str):
        raise TypeError(f'args.token ({args.token}) not of type str')

    if args.url:
        if not isinstance(args.url, str):
            raise TypeError(f'args.url ({args.url}) not of type str')

    if not isinstance(args.owner, str):
        raise TypeError(f'args.owner ({args.owner}) not of type str')

    if not isinstance(args.repos, list):
        raise TypeError(f'args.repos ({args.repos}) not of type list')

    if not isinstance(args.actions, list):
        raise TypeError(f'args.actions ({args.actions}) not of type list')


async def main(args):
    auth = Auth.Token(args.token)
    if args.url:
        gh = Github(base_url=args.url, auth=auth)
    else:
        gh = Github(auth=auth)

    actions = []
    for repo in args.repos:
        logging.info(f'Preparing actions for: {repo}')
        repo = gh.get_repo(f'{args.owner}/{repo}')
        for action in args.actions:
            logging.info(f'Adding {action}')
            actions.append(action_factory.build(action, repo).run())

    logging.info(f'Execute {len(actions)} actions')
    results: list[Result] = await asyncio.gather(*actions, return_exceptions=True)

    good_results = [result for result in results if result.code == 0]
    logging.info(f'{len(good_results)} out of {len(actions)} actions executed succesfully')

    bad_results = (result for result in results if result.code != 0)
    for bad_result in bad_results:
        logging.error(f'Action: {bad_result.action_name}, Message: {bad_result.message}, Code {bad_result.code}')

    logging.debug('Close GitHub connection')
    gh.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='github-manager')
    parser.add_argument('-t', '--token',
                        help='GitHub Personal Access Token with the required scopes.',
                        required=True)
    parser.add_argument('-u', '--url',
                        help='The url of the enterprise instance of GitHub',
                        required=False)
    parser.add_argument('-o', '--owner',
                        help='The owner of the repositories',
                        required=True)
    parser.add_argument('-r', '--repos',
                        help='The repositories on which to apply the action(s)',
                        nargs='+',
                        required=True)
    parser.add_argument('-a', '--actions',
                        help='The actions to apply',
                        nargs='+',
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args_ = parse_args()
    validate_args(args_)
    try:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(main(args_))
    except:
        logger.exception('Exception')
