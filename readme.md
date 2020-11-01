# Głosowania w Sejmie
Dane zawarte w plikach [`vote_results.csv`](../master/vote_results.csv), [`vote_results.json`](../master/vote_results.json), [`vote_results_2.json`](../master/vote_results_2.json) zawierają dane uwzględniające wszystkie posiedzenia Sejmu 9. kandencji do dnia **31.10.2020** włączając w to **20. posiedzenie Sejmu** w dniach 27.10.2020 i 28.10.2020. Skrypt pozwala jednak pobrać nowsze dane w razie potrzeby (konieczne jednak będzie pobranie danych ze wszystkich posiedzeń).
## Metodologia
Do obliczenia korelacji wyników głosowań między ugrupowaniami użyłem wzoru `(liczba głosów za - liczba głosów przeciw)/(liczba wszystkich oddanych głosów, w tym głosów "wstrzymał się")` dzięki czemu otrzymałem wynik z zakresu **[-1, 1]** gdzie 1 oznacza pełne poparcie w głosowaniu, 0 całkowitą obojętność (lub nieobecność posłów) a -1 całkowity brak poparcia.
## Uwagi do plików
* W pliku [`vote_results.json`](../master/vote_results.json) liczba **-2** oznacza nieobecność posłów na głosowaniu.