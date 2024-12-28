from backend.models import Deputy, Term, Result, Sitting, Vote
from util.fetch import get
from config.url import term_url
from typing import List
import re

vote_values = {
  "YES": 1,
  "NO": -1,
  "ABSTAIN": 0,
  "ABSENT": -2,
}

def is_in_list(_str: str, _list: List[str]):
  contains = False
  for fragment in _list:
    if (fragment in _str):
      contains = True
      break

  return contains

def update_votes(db_sitting: Sitting):
  banned_phrases = []

  with open("banned_phrases.txt", "r", encoding="utf-8") as _file:
    for line in _file:
      banned_phrases.append(line.strip())

  new_votes = 0
  votes_to_delete = 0
  votes_list = get(f"{term_url(term)}/votings/{db_sitting.number}")
  sitting_votes = Vote.select().where(Vote.sitting == db_sitting)
  for vote in votes_list:
    db_vote = None
    try:
      db_vote = sitting_votes.select().where(Vote.number == vote["votingNumber"]).get()
      if (is_in_list(db_vote.topic, banned_phrases) or vote["kind"] == "ON_LIST"):
        db_vote.delete_instance()
        votes_to_delete += 1
        continue
    except Vote.DoesNotExist:
      if (not is_in_list(vote["topic"], banned_phrases) and vote["kind"] != "ON_LIST"):   
        db_vote = Vote(
          number=vote["votingNumber"],
          total_votes=vote["totalVoted"],
          time=vote["date"],
          title=re.sub("Pkt \d+\. porz\. dzien\. ", "", vote["title"]),
          topic="Głosowanie nad " + vote["topic"],
          sitting=db_sitting
        )
        db_vote.save()
        new_votes += 1
      else:
        continue

    if (vote["totalVoted"] + vote["notParticipating"] == len(db_vote.results)):
      # All votes were counted
      continue

    new_results = []
    results = get(f"{term_url(term)}/votings/{db_sitting.number}/{db_vote.number}")["votes"]
    db_results = Result.select().where(Result.vote == db_vote)
    for result in results:
      db_mp = None
      try:
        db_mp = Deputy.select().where(Deputy.sejm_id == result["MP"]).get()
      except Deputy.DoesNotExist:
        raise IndexError(f"MP with id {db_mp.sejm_id} not found! Perhaps you forgot to run mps.py first?")

      result_value = vote_values[result["vote"]]
      try:
        db_results.select().where(Result.deputy == db_mp).get()
      except Result.DoesNotExist:
        new_result = Result(
          result=result_value,
          deputy=db_mp,
          vote=db_vote
        )
        new_results.append(new_result)
    Result.bulk_create(new_results)
    print(f"Created {len(new_results)} results for vote {db_vote.number} in sitting {db_sitting.number}.")

  print(f"Created {new_votes} votes, deleted {votes_to_delete} votes.")

if (__name__ == "__main__"):
  terms = Term.select()
  for term in terms:
    sittings = Sitting.select().where(Sitting.term == term)
    for sitting in sittings:
      print(f"Updating votes for sitting {sitting.number} (term {term.id})...")
      update_votes(sitting)
