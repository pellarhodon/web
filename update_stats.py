import requests
from bs4 import BeautifulSoup # Musíme přidat tuhle knihovnu
import re

USERNAME = "Pellarhodon"
# URL tvého profilu na Trackeru
URL = f"https://r6.tracker.network/profile/pc/{USERNAME}"

def scrape_r6():
    try:
        print(f"Scraping data from Tracker.gg for {USERNAME}...")
        
        # Maskujeme se jako Chrome prohlížeč, aby nás nezablokovali
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(URL, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Cannot access Tracker.gg. Status: {response.status_code}")
            return

        # Použijeme BeautifulSoup na vytáhnutí dat z HTML kódu stránky
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tady bot hledá konkrétní texty na stránce
        # POZOR: Názvy tříd se mohou na webu měnit, tohle je aktuální verze
        rank = soup.find("div", {"class": "common-stats"}).find("div", {"class": "rank-name"}).text.strip().upper()
        mmr = soup.find("div", {"class": "common-stats"}).find("div", {"class": "mmr"}).text.strip().replace(",", "")
        
        # Najdeme ostatní staty (Killy, Čas...)
        # Tohle je jen příklad, Tracker.gg má data v různých kontejnerech
        stats_map = {
            "r6-lvl": "373", # Level necháme fixní nebo ho taky vytáhneme
            "r6-rank": rank,
            "r6-mmr": mmr,
            "r6-kills": "FETCHING...", # Zde by se dopsala logika pro zbytek
            "r6-aces": "142",
            "r6-time": "1840H",
            "r6-op": "ASH"
        }

        # Zápis do tvého index.html
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        for eid, val in stats_map.items():
            pattern = rf'(id="{eid}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{val}\2', content)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"SUCCESS! New Rank: {rank} | MMR: {mmr}")

    except Exception as e:
        print(f"Scrape failed: {e}")

if __name__ == "__main__":
    scrape_r6()
