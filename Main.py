import request
from bs4 import BeautifulSoup
# jāizveido datu struktūra
marka = input("Ievadi auto marku: ").strip().lower()
modelis = input("Ievadi auto modeli: ").strip().lower()

base_url = f"https://www.ss.lv/lv/transport/cars/{marka}/{modelis}/sell/page{{}}.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

page = 1
processed_ids = set()

# Nosakām maksimālo lapu skaitu
response = requests.get(base_url.format(1), headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

last_page = 1
pagination = soup.find("div", class_="td2")
if pagination:
    page_links = pagination.find_all("a")
    page_numbers = [int(a.text) for a in page_links if a.text.isdigit()]
    last_page = max(page_numbers) if page_numbers else 1

print(f" Atrastas {last_page} lapas sludinājumu {marka.upper()} {modelis.upper()}!")


while page <= last_page:
    url = base_url.format(page)
    print(f" Apstrādājam lapu {page}/{last_page}: {url}")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(" Lapa nav pieejama!")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    ads = soup.find_all("tr", id=lambda x: x and x.startswith("tr_"))

    if not ads:  
        print(" Nav vairāk sludinājumu")
        break

    for ad in ads:
        try:
            ad_id = ad["id"].split("_")[-1]
            if ad_id in processed_ids:
                print(f" Sludinājums {ad_id} jau apstrādāts, izlaižam.")
                continue  
            
            processed_ids.add(ad_id)

            title_elem = ad.find("a", class_="am")
            title = title_elem.text.strip() if title_elem else "Nezināms"
            link = "https://www.ss.lv" + title_elem["href"] if title_elem else "Nav"

            td_elements = ad.find_all("td", class_=["msga2-o", "msga2-r"])
            year = td_elements[0].text.strip() if len(td_elements) > 0 else "Nav"
            engine = td_elements[1].text.strip() if len(td_elements) > 1 else "Nav"
            mileage = td_elements[2].text.strip() if len(td_elements) > 2 else "Nav"
            price = td_elements[3].text.strip() if len(td_elements) > 3 else "Nav"

            img_elem = ad.find("img", class_="isfoto")
            img_url = img_elem["src"] if img_elem else "Nav attēla"
            # 
            
            })

        except Exception as e:
            print(f" Kļūda apstrādājot sludinājumu: {e}")

    page += 1  
