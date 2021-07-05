import re
from backend.models import Vote
stop_words = []

with open("stop.txt", "r", encoding="utf-8") as f:
    for line in f:
        stop_words.append(line.strip())

frequency = {}

all_votes = Vote.select()
for vote in all_votes:
    line = vote.title.strip()
    line = re.sub(r"^Pkt \d+\. porz\. dzien\. ", "", line)
    for word in line.split(" "):
        word = word.lower()
        word = word.replace(",", "")
        word = word.replace(".", "")
        
        if (word in stop_words or word == "" or re.match(r"^\d+", word)):
            continue
        frequency[word] = frequency.setdefault(word, 0) + 1

sorted_freq = {}
with open("freqs.csv", "w", encoding="utf-8") as f:
    for key in list(sorted(list(frequency.keys()), key=lambda x: frequency[x])):
        f.write("{},{}\n".format(key, frequency[key]))