from vjspd import *

import sys
from pprint import pprint
import json
import argparse

import requests


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main(**options):
    username = options['username']
    password = options['password']
    contest_id = options['contest_id']

    sess = requests.session()

    eprint(f"login: username = {username}")
    login(sess, username, password)

    eprint(f'request contest data: id = {contest_id}')
    data = get_contest_data(sess, contest_id)
    problems = parse_cf_problems(data['problems'])

    eprint(f'request contest rank: id = {contest_id}')
    rank = get_contest_rank(sess, contest_id)
    participants = parse_rank(rank)

    eprint('finished')
    return {
        'contest_id': contest_id,
        'participants': participants,
        'problems': problems
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='vjspd')
    parser.add_argument('contest_id', type=int)
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('-a', '--account_file')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    options = {}
    if args.account_file:
        if args.username or args.password:
            raise "conflict arguments"
        with open(args.account_file) as f:
            options['username'] = f.readline().strip()
            options['password'] = f.readline().strip()
    elif args.username and args.password:
        options['username'] = args.username
        options['password'] = args.password
    else:
        raise 'provide user infomation to login'

    options['contest_id'] = str(args.contest_id)

    output = args.output if args.output else None

    ans = main(**options)

    if output is None:
        json.dump(ans, sys.stdout, indent=4, ensure_ascii=False)
        print()
    else:
        eprint(f'write to {output}')
        with open(output, 'w') as f:
            json.dump(ans, f, indent=4, ensure_ascii=False)
