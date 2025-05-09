# Projekta darbs Auto Sludinājumu Web Scraper no ss.lv

Šī Python programma automātiski savāc sludinājumus no [ss.lv](https://www.ss.lv), pamatojoties uz lietotāja ievadīto automašīnas marku un modeli. Iegūtie dati tiek strukturēti ar saistītā saraksta datu struktūru un saglabāti teksta failā.

## Projekta uzdevums

Programmas mērķis ir:
- Ļaut lietotājam ievadīt auto marku un modeli.
- Automātiski izgūt attiecīgos sludinājumus no ss.lv vairākās lapās.
- Saglabāt svarīgāko informāciju par katru sludinājumu.
- Attēlot datus konsolē un saglabāt tos failā `car_database.txt`.

##  Izmantotās Python bibliotēkas

| Bibliotēka | Apraksts |
|------------|----------|
| [`requests`](https://docs.python-requests.org/) | HTTP pieprasījumu nosūtīšana, lai iegūtu ss.lv lapas saturu. |
| [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) (`bs4`) | HTML dokumentu parsēšana un datu izvilkšana no DOM. |

Instalēšana:
```bash
pip install requests beautifulsoup4
