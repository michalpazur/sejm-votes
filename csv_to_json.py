import json

vote_results = {}
vote_results_2 = {}

with open("vote_results.csv", "r") as f:
  parties = f.readline().strip().split(",")
  vote_results = { k : [] for k in parties }
  vote_results_2 = { k: [] for k in parties }
  for l in f:
    results = l.strip().split(",")
    i = 0
    for name in parties:
      arr = vote_results[name]
      arr_2 = vote_results_2[name]
      result = results[i]
      arr.append(float(result))
      arr_2.append(float(result) if result != -2 else 0)
      vote_results[name] = arr
      vote_results_2[name] = arr_2
      i += 1

with open("vote_results.json", "w") as f:
  json.dump(vote_results, f, ensure_ascii=False)

with open("vote_results_2.json", "w") as f:
  json.dump(vote_results_2, f, ensure_ascii=False)