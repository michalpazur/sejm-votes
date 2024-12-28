from backend.models import Term, Sitting
from util.fetch import get
from config.url import term_url
from datetime import datetime

def parse_date(date: str):
  return datetime.strptime(date, "%Y-%m-%d")

def update_sittings(db_term: Term):
  updated_sittings = []
  new_sittings = []
  sittings_to_delete = []
  term = db_term.id
  
  sittings = get(f"{term_url(term)}/proceedings")
  term_sittings = Sitting.select().where(Sitting.term == db_term)
  for sitting in sittings:
    try:
      db_sitting = term_sittings.select().where(Sitting.number == sitting["number"]).get()
      if (db_sitting.number == 0):
        sittings_to_delete.append(db_sitting)
      elif (len(db_sitting.days) != len(sitting["dates"])):
        db_sitting.days = [parse_date(x) for x in sitting["dates"]]
        updated_sittings.append(db_sitting)
    except Sitting.DoesNotExist:
      new_sitting = Sitting(
        number=sitting["number"],
        days=[parse_date(x) for x in sitting["dates"]],
        term=db_term
      )
      new_sittings.append(new_sitting)

  if (len(updated_sittings) > 0):
    Sitting.bulk_update(updated_sittings, fields=[Sitting.days])
  Sitting.bulk_create(new_sittings)
  if (len(sittings_to_delete) > 0):
    Sitting.delete().where(Sitting.number == 0).execute()
  print(f"Updated {len(updated_sittings)} sittings, created {len(new_sittings)}. Deleted {len(sittings_to_delete)} sittings.")

if (__name__ == "__main__"):
  terms = Term.select()
  for term in terms:
    print(f"Updating sittings for term {term.id}...")
    update_sittings(term)
