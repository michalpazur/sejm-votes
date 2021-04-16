import requests
from bs4 import BeautifulSoup as bs
import json

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
        return -2

vote_results_indicies = {
    "Za": 0,
    "Przeciw": 1,
    "Wstrzymał się": 2,
    "Nieobecny": 3,
}

base_link = 'http://www.sejm.gov.pl/Sejm9.nsf/'
mps = {}
vote_results = {}
party_names = []

with open("mps.json", "r", encoding="utf-8") as f:
    mps = json.load(f)

for party_name in list(mps.values()):
    if (party_name not in party_names):
        party_names.append(party_name)

all_days_page = requests.get(base_link + 'agent.xsp?symbol=posglos&NrKadencji=9')
all_days_soup = bs(all_days_page.content, 'html.parser')

with open("titles.txt", "w") as f:
    f.write("") #make sure the file is empty

with open("vote_results.csv", "w") as f:
    line = ""
    for party_name in party_names:
        line += party_name + ","
    line = line[:-1] + "\n"
    f.write(line)

for all_votes_link in all_days_soup.find('tbody').findAll('a'):
    print(all_votes_link.text)
    all_votes_soup = bs(requests.get(base_link + all_votes_link['href']).content, 'html.parser')
    for vote_row in all_votes_soup.findAll('td', class_='left'):
        vote_link = vote_row.find('a')
        if ('stwierdzenie kworum' in vote_link.text or 'przerwy w obradach' in vote_link.text or 'odroczeniem posiedzenia' in vote_link.text):
            continue

        with open("titles.txt", "a", encoding="utf-8") as f:
            f.write(vote_row.text + "\n")
        
        print(vote_link.text)
        vote_soup = bs(requests.get(base_link + vote_link['href']).content, 'html.parser')
        
        try:
            all_cells = vote_soup.find("tbody").findAll("td", "left")
        except:
            print("!!!")
            continue
        
        tmp_party_results = {k: [0, 0, 0, 0] for k in party_names}
        should_pass = True

        for cell in list(all_cells):
            party_results_link = cell.find("a")
            party_results_page = bs(requests.get(base_link + party_results_link["href"]).content, 'html.parser')
            try:
                all_results_cells = list(party_results_page.find("tbody").findAll("td", "left"))
            except:
                should_pass = False
                break

            #one MP has two cells - one for their name and one for their vote
            #hence the division by two
            for i in range(int(len(all_results_cells)/2)): 
                name = all_results_cells[i * 2].text
                result = vote_results_indicies[all_results_cells[(i * 2) + 1].text]
                party_name = mps[name]
                arr = tmp_party_results[party_name]
                arr[result] = arr[result] + 1
                tmp_party_results[party_name] = arr

        if (not should_pass):
            continue
        
        with open("vote_results.csv", "a") as f:
            line = ""
            for party_name in party_names:
                party_ratio = get_results(tmp_party_results[party_name])
                print("{} - {}".format(party_name, party_ratio))
                line += str(party_ratio) + ","
            line = line[:-1] + "\n"
            f.write(line)
