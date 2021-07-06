![Logo Sejmu RP](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Sejm_RP_logo_and_wordmark.svg/320px-Sejm_RP_logo_and_wordmark.svg.png "Logo Sejmu RP")
# Głosowania w Sejmie
Dane aktualnie pobrane w repozytorium zwierają wyniki glosowań ze wszystkich posiedzeń przeprowadzonych przed dniem **6.07.2021**, w tym głosowania z 33. posiedzenia Sejmu w dniach 23.06.2021 i 24.06.2021.

Dane przechowywane są w bazie SQL, której backup znajduje się w pliku [`backup.sql`](../backup/backend/backup.sql). Aby uzyskać do nich dostęp wystarczy uruchomić skrypt w serwerze PostgreSQL.

Tak samo by móc korzystać ze skryptu konieczne jest uruchomienie serwera PostgreSQL. Możliwe jest skorzystanie z innego serwera, wymaga to jednak ingerenncji w kod.

Dane dla poszczególnych ugrupowań pobierane są z całej kadencji pobierane są na podstawie przynależności posłów w dniu pobrania danych przy użyciu skryptu [`mps.py`](../master/mps.py), który należy uruchomić przed obliczeniem korelacji i wygenerowaniem wykresu.
## Metodologia
Do obliczenia korelacji wyników głosowań między ugrupowaniami użyłem wzoru `(Z - P)/(W - N)`, gdzie:
* `Z` - głosy za
* `P` - głosy przeciw
* `W - N` - liczba wszystkich **oddanych** głosów, w tym głosów "wstrzymał się"

Dzięki temu otrzymałem wynik z zakresu **[-1, 1]** gdzie 1 oznacza pełne poparcie w głosowaniu, 0 całkowitą obojętność (lub nieobecność posłów) a -1 całkowity brak poparcia. Do obliczenia korelacji między ugrupowaniami wykorzystałem [współczynnik korelacji Pearsona](https://pl.wikipedia.org/wiki/Wsp%C3%B3%C5%82czynnik_korelacji_Pearsona).
## Uwagi do plików
* Wartość **-1** oznacza głosowanie *przeciw*, **0** oznacza *wstrzymanie się* od głosu a **1** oznacza głos *za*.
* W bazie danych nieobecność posła a głosowaiu zapisywana jest jako wartość -2.

<img src="https://i.imgur.com/zIZg8x9.png" width="500" alt="Gotowy wykres" />