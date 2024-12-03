from backend.models import Club, Term
from util.fetch import get
from config.url import term_url

def update_clubs(db_term: Term):
  updated_clubs = []
  new_clubs = []
  term = db_term.id
  
  clubs = get(f"{term_url(term)}/clubs")
  term_clubs = Club.select().where(Club.term == db_term)
  for club in clubs:
    try:
      db_club = term_clubs.select().where(Club.sejm_id == club["id"]).get()
      if (db_club.full_name != club["name"]):
        db_club.full_name = club["name"]
        updated_clubs.append(db_club)
    except Club.DoesNotExist:
      new_club = Club(
        full_name=club["name"],
        sejm_id=club["id"],
        term=db_term
      )
      new_clubs.append(new_club)

  if (len(updated_clubs) > 0):
    Club.bulk_update(updated_clubs, fields=[Club.full_name])
  Club.bulk_create(new_clubs)
  print(f"Updated {len(updated_clubs)} clubs, created {len(new_clubs)}.")

if (__name__ == "__main__"):
  terms = Term.select()
  for term in terms:
    print(f"Updating clubs for term {term.id}...")
    update_clubs(term)
