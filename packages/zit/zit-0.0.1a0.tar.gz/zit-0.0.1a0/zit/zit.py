#! /usr/bin/env python
import argparse


def lambda_publish(lbd_path: str, lbd_name: str):
    print('publish')


if __name__ == '__main__':

    root_parser = argparse.ArgumentParser(description='ZitySpace (Lambda) CLI')

    root_parser.add_argument(
        '--verbose',
        help='Show details',
        action='store_true',
        required=False,
    )
    subcmd_parsers = root_parser.add_subparsers(help='Subcommand to run', dest='subcmd')

    lambda_parser = argparse.ArgumentParser(add_help=False)
    lambda_parser.add_argument('action', help='lambda action', type=str.lower, choices=['publish', 'install'])

    subcmd_parsers.add_parser("lambda", parents=[lambda_parser], help='Lambda')
    subcmd_parsers.add_parser("login", help='Login')

    args = root_parser.parse_args()

    subcmd = args.subcmd
    action = args.action
    if subcmd == 'lambda':
        if action == 'publish':
            pass
        elif action == 'install':
            pass

    elif subcmd == 'login':
        pass
