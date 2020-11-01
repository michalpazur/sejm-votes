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

base_link = 'http://www.sejm.gov.pl/Sejm9.nsf/'
vote_results = {
    'PiS': [],
    'KO': [],
    'Lewica': [],
    'PSL-Kukiz15': [],
    'Konfederacja': [],
    'niez.': [],
}
party_names = {
    'PiS': 'PiS',
    'KO': 'KO',
    'Lewica': 'Lewica',
    'PSL-Kukiz15': 'PSL-Kukiz15',
    'Konfederacja': 'Konfederacja',
    'niez.': 'niez.',
    'SLD': 'Lewica',
    'PSL': 'PSL-Kukiz15',
}

all_days_page = requests.get(base_link + 'agent.xsp?symbol=posglos&NrKadencji=9')
all_days_soup = bs(all_days_page.content, 'html.parser')
for all_votes_link in all_days_soup.find('tbody').findAll('a'):
    print(all_votes_link.text)
    all_votes_soup = bs(requests.get(base_link + all_votes_link['href']).content, 'html.parser')
    for vote_row in all_votes_soup.findAll('td', class_='left'):
        vote_link = vote_row.find('a')
        if ('stwierdzenie kworum' in vote_link.text or 'przerwy w obradach' in vote_link.text):
            continue
        
        print(vote_link.text)
        vote_soup = bs(requests.get(base_link + vote_link['href']).content, 'html.parser')
        pis_results = [0, 0, 0, 0] #za, przeciw, wstrzymało się, nieobecni
        pis_ratio = 0
        row_index = 0

        for party_row in vote_soup.findAll('tr'):
            if (row_index == 0):
                row_index += 1
                continue
            cell_index = 0
            party_name = ''
            party_results = [0, 0, 0, 0]
            for cell in party_row.findAll('td'):
                if (cell_index == 0):
                    party_name = cell.text

                cell_text = cell.text
                if (cell_text == '-'):
                    cell_text = '0'

                if (cell_index > 2 and row_index == 1):
                    pis_results[cell_index - 3] = int(cell_text)
                elif (cell_index > 2):
                    party_results[cell_index - 3] = int(cell_text)
                cell_index += 1
            
            if (row_index == 1):
                pis_ratio = get_results(pis_results)
                print(party_name, pis_ratio)
                vote_results[party_names[party_name]].append(pis_ratio)
            else:
                party_ratio = get_results(party_results)
                if (party_ratio != -2):
                    print(party_name, 'niezgodnie z PiSem' if abs(party_ratio - pis_ratio) > 0.2 else 'zgodnie z PiSem', party_ratio)
                else:
                    print(party_name, 'nieobecni')
                vote_results[party_names[party_name]].append(party_ratio)
            row_index += 1

with open('vote_results.json', 'w', encoding='utf-8') as f:
    json.dump(vote_results, f)
