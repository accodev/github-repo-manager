import logging
import logging.config
import argparse
import asyncio
from github import Github, Auth

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()


async def main():
    parser = argparse.ArgumentParser(prog='github-manager')
    parser.add_argument('-t', '--token',
                        help='GitHub Personal Access Token with the required scopes.',
                        required=True)
    parser.add_argument('-u', '--url',
                        help='The url of the enterprise instance of GitHub',
                        required=False)
    parser.add_argument('-r', '--repos',
                        help='The repositories on which to apply the action(s)',
                        nargs='+',
                        required=True)
    parser.add_argument('-a', '--actions',
                        help='The actions to apply',
                        nargs='+',
                        required=True)
    args = parser.parse_args()

    auth = Auth.Token(args.token)

    if args.url:
        gh = Github(base_url=args.url, auth=auth)
    else:
        gh = Github(auth=auth)

    actions = []
    for repo in args.repos:
        logging.info(f'Preparing actions for: {repo}')
        for action in args.actions:
            logging.info(f'Adding {action}')
            actions.append(lambda: action)

    logging.info(f'Execute {len(actions)} actions')
    #await asyncio.gather(*actions, return_exceptions=True)

    logging.debug('Close GitHub connection')
    gh.close()


if __name__ == '__main__':
    try:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(main())
    except:
        logger.exception('Exception')
