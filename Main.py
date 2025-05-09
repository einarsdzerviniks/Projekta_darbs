import requests
from bs4 import BeautifulSoup


class Node:
    def __init__(self, id, title, year, engine, mileage, price, link, image):
        self.id = id
        self.title = title
        self.year = year
        self.engine = engine    
        self.mileage = mileage
        self.price = price
        self.link = link
        self.image = image
        self.next = None
class CarDatabase:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        new_node = Node(**data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    def __len__(self):
        return self.size
    def print(self):
        current = self.head
        while current:
            print("=== Car Listing ===")
            print(f"ID: {current.id}")
            print(f"Title: {current.title}")
            print(f"Year: {current.year}")
            print(f"Engine: {current.engine}")
            print(f"Mileage: {current.mileage}")
            print(f"Price: {current.price}")
            print(f"Link: {current.link}")
            print(f"Image: {current.image}")
            print("==================\n")
            current = current.next
    def to_txt(self):
        with open("car_database.txt", "w", encoding="utf-8") as file:
            current = self.head
            while current:
                file.write("=== Car Listing ===\n")
                file.write(f"ID: {current.id}\n")
                file.write(f"Title: {current.title}\n")
                file.write(f"Year: {current.year}\n")
                file.write(f"Engine: {current.engine}\n")
                file.write(f"Mileage: {current.mileage}\n")
                file.write(f"Price: {current.price}\n")
                file.write(f"Link: {current.link}\n")
                file.write(f"Image: {current.image}\n")
                file.write("==================\n\n")
                current = current.next
        print("Dati saglabāti car_database.txt failā.")

database = CarDatabase()

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

            database.append({
                "id": ad_id,
                "title": title,
                "year": year,
                "engine": engine,
                "mileage": mileage,
                "price": price,
                "link": link,
                "image": img_url
            })

        except Exception as e:
            print(f" Kļūda apstrādājot sludinājumu: {e}")

    page += 1  
database.print()
database.to_txt()