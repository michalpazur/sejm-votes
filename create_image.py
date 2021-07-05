import json, math
from PIL import Image, ImageDraw
from matplotlib.pylab import get_cmap
import backend.models as m
from peewee import fn

def average(arr):
  return sum(arr)/len(arr)

def get_results(vote_results):
  all_votes = sum(vote_results)
  votes_for = vote_results[0]
  votes_against = vote_results[1]
  abstained = vote_results[2]
  no_vote = vote_results[3]

  if (all_votes - no_vote > 0):
    ratio = (votes_for - votes_against) / (all_votes - no_vote)
    return ratio
  else:
    return 0
        
def calculate_correlation(party_x, party_y, avgs, std_devs, corrs):
  corr = 0
  if (party_x == party_y):
    corr = 1
    corrs[party_x][party_y] = corr
    corrs[party_x][party_y] = corr
  elif (corrs[party_x][party_y] is None):
    all_votes = m.Vote.select()
    cov = 0
    for vote in all_votes:
      result_x = m.PartyResult.get((m.PartyResult.vote == vote) & (m.PartyResult.party == party_x))
      result_y = m.PartyResult.get((m.PartyResult.vote == vote) & (m.PartyResult.party == party_y))
      cov += (result_x.result - avgs[party_x]) * (result_y.result - avgs[party_y])
    corr = cov / (std_devs[key_x] * std_devs[key_y])
    corrs[party_x][party_y] = corr
    corrs[party_y][party_x] = corr
  else:
    corr = corrs[party_x][party_y]

  print(party_x, party_y, corr)
  return corr
  
party_list = m.Deputy.select(m.Deputy.party).distinct()
party_names = [party.party for party in party_list]

vote_list = m.Vote.select()
for vote in vote_list:
  sitting = m.Sitting.select().join(m.Day).join(m.Vote).where(m.Vote.id == vote.id).get()
  print("Sitting {}, vote {}".format(sitting.number, vote.number))
  for party_name in party_names:
    vote_result = None
    try:
        vote_result = m.PartyResult.get((m.PartyResult.vote == vote) & (m.PartyResult.party == party_name))
    except:
        pass
      
    all_results = m.Result.select().join(m.Deputy).where((m.Result.vote == vote) & (m.Deputy.party == party_name))
    votes_for = all_results.where(m.Result.result == 1).count()
    votes_against = all_results.where(m.Result.result == -1).count()
    abstained = all_results.where(m.Result.result == 0).count()
    no_vote = all_results.where(m.Result.result == -2).count()
    result = get_results([votes_for, votes_against, abstained, no_vote])

    if (vote_result is None):
      vote_result = m.PartyResult(party=party_name, vote=vote, result=result)
      vote_result.save()
    else:
      vote_result.result = result
      vote_result.save()

avgs = {}
std_devs = {}
corrs = {party_x : {party_y : None for party_y in party_names} for party_x in party_names}

print("Average results:")
avg_query = m.PartyResult.select(m.PartyResult.party, fn.avg(m.PartyResult.result).alias("avg")).group_by(m.PartyResult.party)
for row in avg_query:
  print(row.party, row.avg)
  avgs[row.party] = row.avg

print("Standard deviations:")
for party_name in party_names:
  variance = 0
  for result in m.PartyResult.select().where(m.PartyResult.party==party_name):
      variance += (result.result - avgs[party_name]) ** 2
  std_dev = math.sqrt(variance)
  print(party_name, std_dev)
  std_devs[party_name] = std_dev

for key_x in party_names:
  for key_y in party_names:
    calculate_correlation(key_x, key_y, avgs, std_devs, corrs)

sorted_party_names = sorted(party_names, key=lambda key: average([corrs[key][p] for p in corrs[key]]))

img = Image.new('RGBA', (len(party_names) * 500, len(party_names) * 500))
x = 0
for key_x in sorted_party_names:
  y = 0
  for key_y in sorted_party_names:
    corr = calculate_correlation(key_x, key_y, avgs, std_devs, corrs)
    d = ImageDraw.Draw(img)
    fill_color = tuple(int(x * 255) for x in get_cmap('RdYlGn')((corr + 1) / 2))
    d.rectangle([(x * 500, y * 500), ((x + 1) * 500, (y+ 1) * 500)], fill=fill_color)
    y += 1
  x += 1
img.save('chart.png')
