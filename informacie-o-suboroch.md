# Informácie o súboroch

Prehľad súborov v projekte KECY-Znacenie a ich význam.

## Súbory `.md`

| Súbor | Význam |
|---|---|
| `ke.cy znacenie-facebook message.md` | Pripnuté správy a komunikácia k značeniu: postup prieskumu zóny, návrh miest pre tabuľky, kódy tabuliek na mape (MC, MZ1, TL, SĽ, SP, SR, !, KP) a zoznam podkladov (mapa celku, mapy zón, smerovníky, začiatok/koniec trailu). Obsahuje aj komunikáciu Zorana z 22. 10. 2025 (termín pripomienok, odkaz na Drive, princíp zón a farieb). |
| `Upravy mapy.md` | Zber pripomienok a nedostatkov na mape od jednotlivých členov (chýbajúce popisy, preklepy, zaniknuté podniky, nadmorské výšky, šípky smeru, ikony). Podklad pre grafika. |
| `KECY znacky\start trailu\nazvy-trailov.md` | Tabuľka názvov trailov (dĺžka, obtiažnosť, názov PDF súboru) prevzatá z PDF značiek štartu trailu, vrátane upozornení na chyby v podkladoch (Kamenný 0 m, rovnaká dĺžka Bedle a Jahody, nejednotná obtiažnosť). |
| `KECY mapy\ke.cy-mapy.md` | Popis máp (`kecy celok.pdf`, `zona 1–4.pdf`): ako čítať mapu (obtiažnosť, ikony), farby a poloha zón 1–4 a priradenie trailov k zónam podľa legendy. |
| `mesenger-vystupy\Upravy mapy.md` | Pôvodný zber pripomienok k mape od členov (podpisy: DK, Gabi M., Peťo D., Veronika, PaloG, Rišo, Tomáš). |
| `mesenger-vystupy\prehlad-pripomienok-po-osobach.md` | Pripomienky z `Upravy mapy.md` zoradené po osobách, s tabuľkou opakujúcich sa tém. |
| `gps\nortysp-ke.cy-zona-2-sumar.md` | Súhrn úpravy súboru `nortysp-ke.cy-zona-2.kml`: postup, význam kódov (MC, MZ, T, SĽ, SP, SR/SV, K, KP, !) a tabuľky všetkých 99 bodov zoradené podľa zón (kategória, obsah, poznámka, ⚠, GPS). |
| `informacie-o-suboroch.md` | Tento súbor: prehľad súborov a ich významu. |

## Prehľad v HTML

| Súbor | Význam |
|---|---|
| `prehlad.html` | Prepojený prehľad celého projektu na otvorenie v prehliadači: stav projektu, zoznam úloh na odškrtnutie, traily s obrázkami tabúľ (štart, vľavo, vpravo, vpred), počty tabúľ po zónach, mapy, všetky značky, tabuľka 99 GPS bodov, dokumenty `.md` a zoznam všetkých súborov. Sekcie sa dajú skryť, filtrovať podľa zóny a prehľadávať. |
| `prehlad-img\` | Náhľady (PNG) všetkých PDF značiek a máp, ktoré používa `prehlad.html`. Bez tohto priečinka sa v prehľade obrázky nezobrazia. |
| `skripty\build_html.py` | Generátor `prehlad.html` (údaje o trailoch, úlohy, pripomienky). Spúšťa sa z koreňa projektu: `python skripty\build_html.py`. |
| `skripty\tpl.html` | HTML šablóna (vzhľad, filtre, vyhľadávanie), ktorú používa `build_html.py`. |
| `skripty\thumbs.py` | Vygeneruje náhľady PNG do `prehlad-img\` zo všetkých PDF značiek a máp (potrebuje `pymupdf`). Spúšťa sa z koreňa projektu: `python skripty\thumbs.py`. |

## Účastníci

| Meno | V súboroch ako | Pripomienky / správy |
|---|---|---|
| Daniel Kolibar | DK | áno (`Upravy mapy.md`) |
| Gabriel Malina | Gabi M. | áno |
| Peter Dvorcak | Peťo D. | áno |
| Veronika Urbanovicova | Veronika | áno |
| Pavol Godis | PaloG | áno |
| Riso Tomecko | Rišo | áno |
| Tomas Dratva | Tomáš (zóna 4) | áno |
| Zoran Bosak | Zoran | správy z 22. 10. 2025 (`ke.cy znacenie-facebook message.md`) |
| Jan Bodnar | – | v súboroch nič |
| Martin Kandrac | – | v súboroch nič |
| Matthew Cruppi | – | v súboroch nič |
| Pater Peter | – | v súboroch nič |
| Samo Sas | – | v súboroch nič |
| Sigy Moravsky | – | v súboroch nič |

Priradenie podpisov k menám je odhad podľa krstných mien a prezývok.

## Súbory v priečinku `gps`

| Súbor | Význam |
|---|---|
| `gps\nortysp-ke.cy-zona-2.kml` | Hlavný súbor s 99 bodmi značenia pre zóny 1–4 (napriek názvu "zona-2"). Body sú zoradené do priečinkov Zóna (1 zelená, 2 žltá, 3 červená, 4 modrá) → kategória (mapy, prechody medzi zónami, začiatky trailov, smerovníky, križovania, konce trailov a protismer, výstrahy). Každý bod má popis (zóna, typ, obsah, poznámka, GPS, pôvodný názov) a farbu podľa kategórie. Body s ⚠ treba overiť. |
