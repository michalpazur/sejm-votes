import requests
from bs4 import BeautifulSoup as bs
from backend.models import Deputy, split_name

letters = ["A", "B"]

for page_letter in letters:
  res = requests.get("http://sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type={}".format(page_letter))
  soup = bs(res.content, 'html.parser')

  all_letters = soup.findAll("ul", "deputies")
  new_deputies = []
  deputies = []
  for letter in all_letters:
    letter_mps = letter.findAll("li")
    for mp in letter_mps:
      name = mp.find("div", "deputyName").text
      party = mp.find("div", "deputy-box-details").find("strong").text

      first_name, last_name = split_name(name)
      try:
        deputy = Deputy.select().where((Deputy.first_name==first_name) & (Deputy.last_name==last_name)).get()
        if (deputy.party != party):
          print("Updating information about {} {}".format(first_name, last_name))
          deputy.party = party
          deputies.append(deputy)
      except:
        print("Creating deputy {} {}".format(first_name, last_name))
        deputy = Deputy(first_name=first_name, last_name=last_name, party=party)
        new_deputies.append(deputy)

  Deputy.bulk_update(deputies, fields=[Deputy.party], batch_size=50)
  Deputy.bulk_create(new_deputies, batch_size=100)
