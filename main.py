import requests
from bs4 import BeautifulSoup as bs
import json
import backend.models as m
import datetime

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

vote_results_values = {
    "Za": 1,
    "Przeciw": -1,
    "Wstrzymał się": 0,
    "Nieobecny": -2,
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

    header = all_votes_soup.find("h1").text.split(" ")
    #Głosowania w dniu DD-MM-YYYY r. na XX. posiedzeniu Sejmu
    date = header[3].split("-")
    sitting_number = int(header[6][:-1])
    sitting = None
    try:
        sitting = m.Sitting.get(m.Sitting.number == sitting_number)
    except:
        print("Creating sitting with number {}".format(sitting_number))
        sitting = m.Sitting(number=sitting_number)
        sitting.save()
    
    day = None
    date_formatted = datetime.date(int(date[2]), int(date[1]), int(date[0]))
    try:
        day = m.Day.get(m.Day.date == date_formatted)
    except:
        print("Creating new day: {}".format(".".join(date)))
        day = m.Day(date=date_formatted, sitting=sitting)
        day.save()
    
    for row in all_votes_soup.find("tbody").findAll('tr'):
        vote_row = row.find("td", class_="left")
        vote_link = vote_row.find('a')
        if ('stwierdzenie kworum' in vote_link.text or 'przerwy w obradach' in vote_link.text or 'odroczeniem posiedzenia' in vote_link.text):
            continue

        title = vote_row.text
        short_title = vote_link.text

        vote = None
        vote_number = int(row.find("td", class_="bold").text)
        print(title)

        #If all the votes have been counted there's no need to count them again
        try:
            vote = m.Vote.get((m.Vote.day == day) & (m.Vote.number == vote_number))
            count = m.Result.select().where(m.Result.vote == vote).count()
            if (count == vote.total_votes):
                print("Skipping vote {}, all votes are counted.".format(vote_number))
                continue
            else:
                print("Counted {} votes, {} votes are missing.".format(count, vote.total_votes - count))
        except:
            pass

        #If not, download the page and count the votes
        vote_soup = bs(requests.get(base_link + vote_link['href']).content, 'html.parser')
        try:
            all_cells = vote_soup.find("tbody").findAll("td", "left")
        except:
            print("Encountered an error while parsing HTML.")
            continue

        with open("titles.txt", "a", encoding="utf-8") as f:
            f.write(title + "\n")

        #Getting total number of votes from the header
        bold_elements = vote_soup.find("div", class_="sub-title").findAll("strong")
        voted = int(bold_elements[0].text)
        not_voted = int(bold_elements[4].text)
        total = voted + not_voted
        print("Voted: {}, not voted: {}, total: {}".format(voted, not_voted, total))
        if (vote is None):
            print("Creating vote with number {}...".format(vote_number))
            vote = m.Vote(day=day, title=title, number=vote_number, total_votes=total)
            vote.save()

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
                res = all_results_cells[(i * 2) + 1].text
                result = vote_results_indicies[res]
                result_value = vote_results_values[res]
                party_name = mps[name]
                arr = tmp_party_results[party_name]
                arr[result] = arr[result] + 1
                tmp_party_results[party_name] = arr

                first_name, last_name = m.split_name(name)
                deputy = None
                try:
                    deputy = m.Deputy.get((m.Deputy.first_name == first_name) & (m.Deputy.last_name == last_name))
                except:
                    print("No deputy with name {} {} found.".format(first_name, last_name))
                    print("Perhaps you forgot to run mps.py first?")
                    quit(-1)

                vote_result = None
                try:
                    vote_result = m.Result.get((m.Result.deputy == deputy) & (m.Result.vote == vote))
                    vote_result.result = result_value
                    vote_result.save()
                except:
                    vote_result = m.Result(result=result_value, vote=vote, deputy=deputy)
                    vote_result.save()

        if (not should_pass):
            continue
        
        with open("vote_results.csv", "a") as f:
            line = ""
            for party_name in party_names:
                party_ratio = get_results(tmp_party_results[party_name])
                #print("{} - {}".format(party_name, party_ratio))
                line += str(party_ratio) + ","
            line = line[:-1] + "\n"
            f.write(line)
