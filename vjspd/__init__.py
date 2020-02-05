from pprint import pprint
import json

from lxml import etree


def login(sess, username, passwd):
    url = "https://vjudge.net/user/login"
    data = {
        "username": username,
        "password": passwd
    }
    resp = sess.post(url, data=data)
    assert(resp.status_code == 200)


def get_contest_data(sess, contest_id):
    url = f"https://vjudge.net/contest/{contest_id}"
    resp = sess.get(url)
    assert(resp.status_code == 200)
    tree = etree.HTML(resp.text)
    data_xpath = "/html/body/textarea/text()"
    data_raw = tree.xpath(data_xpath)[0]
    return json.loads(data_raw)


def parse_cf_problems(problems):
    results = []
    for problem in problems:
        assert(problem['oj'] == 'CodeForces')
        title = f"{problem['oj']} - {problem['probNum']}"
        source = problem['properties']['Source']
        score = int(problem['properties']['Tags'].split('*')[1])
        results.append({
            'title': title,
            'source': source,
            'score': score
        })
    return results


def get_contest_rank(sess, contest_id):
    url = f"https://vjudge.net/contest/rank/single/{contest_id}"
    resp = sess.get(url)
    assert(resp.status_code == 200)
    return resp.json()


def parse_rank(rank):
    participants = rank['participants']
    submissions = rank['submissions']

    results = {}
    for uid, name in participants.items():
        results[uid] = {
            'username': name[0],
            'realname': name[1],
            'submissions': []
        }

    for submission in submissions:
        [uid, problem_index, ac, time] = submission
        results[str(uid)]['submissions'].append({
            'problem_index': problem_index,
            'AC': bool(ac),
            'time_seconds': time
        })

    results = [dict(user_id=k, **v) for k, v in results.items()]
    return results
