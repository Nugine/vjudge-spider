from vjspd import *

from pprint import pprint
import json

import requests

with open("task.txt") as f:
    username = f.readline().strip()
    password = f.readline().strip()
    contest_id = int(f.readline().strip())

sess = requests.session()

print(f"login: username = {username}")
login(sess, username, password)

print(f'request contest data: id = {contest_id}')
data = get_contest_data(sess, contest_id)
problems = parse_cf_problems(data['problems'])

print(f'request contest rank: id = {contest_id}')
rank = get_contest_rank(sess, contest_id)

participants = parse_rank(rank)

print('write to participants.json')
with open('participants.json', 'w') as f:
    json.dump(participants, f, indent=4, ensure_ascii=False)

print('write to problems.json')
with open('problems.json', 'w') as f:
    json.dump(problems, f, indent=4, ensure_ascii=False)

print('finished')
