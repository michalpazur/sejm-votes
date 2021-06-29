import requests
from bs4 import BeautifulSoup as bs
import json
from backend.models import Deputy, database

letters = ["A", "B"]
all_mps = {}

for page_letter in letters:
  res = requests.get("http://sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type={}".format(page_letter))
  soup = bs(res.content, 'html.parser')

  all_letters = soup.findAll("ul", "deputies")
  for letter in all_letters:
    letter_mps = letter.findAll("li")
    for mp in letter_mps:
      name = mp.find("div", "deputyName").text
      party = mp.find("div", "deputy-box-details").find("strong").text
      print(name, party)
      all_mps[name] = party
      
      first_name = ""
      last_name = ""
      name = name.split(" ")
      if ("vel" in name):
        #👀 at you Szymon Szynkowski vel Sęk
        first_name = " ".join(name[-1:])
        last_name = " ".join(name[0:3])
      else:
        first_name = " ".join(name[1:])
        last_name = name[0]

      try:
        deputy = Deputy.select().where((Deputy.first_name==first_name) & (Deputy.last_name==last_name)).get()
        deputy.party = party
        deputy.save()
      except:
        print("Creating deputy {} {}".format(first_name, last_name))
        deputy = Deputy(first_name=first_name, last_name=last_name, party=party)
        deputy.save()

with open('mps.json', 'w', encoding='utf-8') as f:
  json.dump(all_mps, f, ensure_ascii=False, sort_keys=True, indent=2)