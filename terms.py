import requests
from config.url import base_url
from backend.models import Term

terms_to_include = [9, 10]

def update_terms():
  res = requests.get(f"{base_url}/term").json()
  for term in res:
    num = term["num"]
    if (num not in terms_to_include):
      continue

    db_term, created = Term.get_or_create(id=num, defaults={ "start": "9999-01-01" })
    created_str = "Creating" if created else "Updating"
    print(f"{created_str} term number {num}...")
    db_term.start = term["from"]
    db_term.end = term.get("to", None)
    db_term.save()

if (__name__ == "__main__"):
  update_terms()