import sys
import json
from pprint import pprint
import argparse
import csv

penalty_per_error = 50


def main(data_file):
    data = json.load(open(data_file))

    problems = data['problems']

    results = []

    for participant in data['participants']:
        submissions = participant['submissions']

        score = [0 for _ in range(len(problems))]
        ac = [False for _ in range(len(problems))]
        error = [0 for _ in range(len(problems))]

        for sm in submissions:
            i = sm['problem_index']
            if ac[i]:
                continue
            if sm['AC']:
                score[i] += problems[i]['score']
                ac[i] = True
            else:
                score[i] -= penalty_per_error
                error[i] += 1

        results.append({
            'name': participant['realname'],
            'score': sum(x for x in score if x > 0),
            'solved': sum(int(b) for b in ac),
            'problems': [{
                'no': chr(i+ord('A')),
                'AC': ac[i],
                'error':error[i]
            } for i in range(len(problems))]
        })

    results.sort(key=lambda x: x['name'])

    ans = {
        'contest_id': data['contest_id'],
        'rank': results,
        'problems': data['problems']
    }

    return ans


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='analyze')
    parser.add_argument('data_json')
    parser.add_argument(
        '-j', '--json', help="output as json", action='store_true')
    parser.add_argument('-c', '--csv', help="output as csv",
                        action='store_true')
    parser.add_argument('-o', '--output', help="output to file")
    args = parser.parse_args()

    if not args.json and not args.csv:
        raise "provide output method"

    if args.json and args.csv:
        raise "conflice argument"

    ans = main(args.data_json)

    output = open(args.output, 'w') if args.output else sys.stdout

    if args.json:
        json.dump(ans, output, indent=4, ensure_ascii=False)
        print(file=output)

    if args.csv:
        writer = csv.writer(output)

        headers = ['name', f'contest/{ans["contest_id"]}/score']
        writer.writerow(headers)
        for r in ans['rank']:
            writer.writerow([r['name'], r['score']])

        headers = ['name', f'contest/{ans["contest_id"]}/problems']
        headers.extend(chr(i+ord('A')) for i in range(len(ans['problems'])))
        writer.writerow(headers)

        for r in ans['rank']:
            row = [r['name'], r['solved']]
            row.extend(f"{int(p['AC'])}/{-p['error']}" for p in r['problems'])
            writer.writerow(row)
