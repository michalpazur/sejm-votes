import requests
from bs4 import BeautifulSoup as bs
import json

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

with open('mps.json', 'w', encoding='utf-8') as f:
  json.dump(all_mps, f, ensure_ascii=False, sort_keys=True, indent=2)