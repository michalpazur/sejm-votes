import requests
from backend.models import Club, Deputy, Term
from config.url import term_url
from util.fetch import get

def update_mps(db_term: Term):
  updated_mps = []
  new_mps = []
  term = db_term.id
  mps = get(f"{term_url(term)}/MP")
  term_mps = Deputy.select().where(Deputy.term == db_term)
  for mp in mps:
    club = None
    club_id = mp["club"]
    try:
      club = Club.get(Club.sejm_id == club_id)
    except Club.DoesNotExist:
      raise Club.DoesNotExist(f"Club {club_id} does not exist! Perhaps you forgot to run clubs.py first?")
    try:
      db_mp = term_mps.select().where(Deputy.sejm_id == mp["id"]).get()
      if (db_mp.club != club):
        db_mp.club = club
        updated_mps.append(db_mp)
    except Deputy.DoesNotExist:
      new_mp = Deputy(
        first_name=mp["firstName"],
        last_name=mp["lastName"],
        term=db_term,
        club=club,
        birthday=mp["birthDate"],
        district_num=mp["districtNum"],
        sejm_id=mp["id"]
      )
      new_mps.append(new_mp)

  if (len(updated_mps)):
    Deputy.bulk_update(updated_mps, fields=[Deputy.club])
  Deputy.bulk_create(new_mps)
  print(f"Updated {len(updated_mps)} MPs, created {len(new_mps)}.")

if (__name__ == "__main__"):
  terms = Term.select()
  for term in terms:
    print(f"Updating MPs for term {term.id}...")
    update_mps(term)
