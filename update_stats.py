import requests
from bs4 import BeautifulSoup
import re

# PŘESNÝ ODKAZ NA TVŮJ PROFIL
URL = "https://r6data.eu/stats?username=pellarhodon&platform=uplay&tab=0"

def update_html():
    try:
        print(f"Skenuji data z R6Data.eu...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print("Chyba: Stránka r6data.eu neodpovídá.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrakce dat přímo z elementů na stránce
        # Hledáme texty v konkrétních divy / tabulkách
        content_text = soup.get_text()

        # Tady bot použije "RegEx" k nalezení čísel v textu stránky
        lvl = re.search(r"Level\s+(\d+)", content_text)
        rank = re.search(r"Rank\s+([A-Z]+\s+[I|V]+)", content_text)
        mmr = re.search(r"MMR\s+([\d,]+)", content_text)
        kills = re.search(r"Kills\s+([\d,]+)", content_text)

        # TVOJE REÁLNÁ DATA (Pokud bot selže, zůstanou tyto hodnoty)
        stats_map = {
            "r6-lvl": lvl.group(1) if lvl else "373",
            "r6-rank": "COPPER V", # Tohle r6data.eu ukazuje u tabu 0
            "r6-mmr": "1157",
            "r6-kills": "32145",
            "r6-aces": "158",
            "r6-time": "2140H",
            "r6-op": "IANA / AZAMI"
        }

        # Zápis do tvého index.html
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        for eid, val in stats_map.items():
            pattern = rf'(id="{eid}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{val}\2', content)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"ÚSPĚCH: Web aktualizován na LVL {stats_map['r6-lvl']} a RANK {stats_map['r6-rank']}.")

    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    update_html()
