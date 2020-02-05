import sys
import json
from pprint import pprint

data_file = sys.argv[1]
data = json.load(open(data_file))

problems = data['problems']

for participant in data['participants']:
    submissions = participant['submissions']
    score = [0 for _ in range(len(problems))]

    for sm in submissions:
        i = sm['problem_index']
        if sm['AC']:
            if score[i] <= 0:
                score[i] += problems[i]['score']
        else:
            score[i] -= 50
    participant['score'] = sum(x for x in score if x > 0)

results = [{'name': p['realname'], 'score':p['score']}
           for p in data['participants']]
results.sort(key=lambda x: x['name'])
results.sort(key=lambda x: x['score'], reverse=True)

ans = {
    'contest_id': data['contest_id'],
    'rank': results,
}

json.dump(ans, sys.stdout, ensure_ascii=False, indent=4)
print()
