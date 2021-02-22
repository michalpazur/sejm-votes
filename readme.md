# Głosowania w Sejmie
Dane zawarte w plikach [`vote_results.csv`](../master/vote_results.csv), [`vote_results.json`](../master/vote_results.json), [`vote_results_2.json`](../master/vote_results_2.json) zawierają dane uwzględniające wszystkie posiedzenia Sejmu 9. kandencji do dnia **21.02.2021** włączając w to **25. posiedzenie Sejmu** w dniach 20.01.2021 i 21.01.2021. Skrypt pozwala jednak pobrać nowsze dane w razie potrzeby (konieczne jednak będzie pobranie danych ze wszystkich posiedzeń).

Dane dla poszczególnych ugrupowań pobierane są z całej kadencji pobierane są na podstawie przynależności posłów w dniu 21.02.2021, nawet jeśli dane ugrupowanie nie istaniało od początku kadencji.
## Metodologia
Do obliczenia korelacji wyników głosowań między ugrupowaniami użyłem wzoru `(Z - P)/(W - N)`, gdzie:
* **Z** - głosy za
* **P** - głosy przeciw
* **W - N** - liczba wszystkich oddanych głosów, w tym głosów "wstrzymał się"

Dzięki temu otrzymałem wynik z zakresu **[-1, 1]** gdzie 1 oznacza pełne poparcie w głosowaniu, 0 całkowitą obojętność (lub nieobecność posłów) a -1 całkowity brak poparcia.
## Uwagi do plików
* W pliku [`vote_results.json`](../master/vote_results.json) liczba **-2** oznacza nieobecność posłów na głosowaniu.