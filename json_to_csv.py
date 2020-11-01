import json

with open('vote_results.json', 'r') as f:
    results = json.load(f)

with open('vote_results.csv', 'w') as f:
    f.write(','.join(results.keys()))
    f.write('\n')

    for i in range(len(results['PiS'])):
        string = ''
        for key in results.keys():
            value = results[key][i]
            value = value if value != -2 else 0
            string = '{}{},'.format(string, value)
        string = string[:-1]
        f.write(string)
        f.write('\n')

for key in results.keys():
    results[key] = list(map(lambda x: x if x != -2 else 0, results[key]))

with open('vote_results_2.json', 'w') as f:
    json.dump(results, f)