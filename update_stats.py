import requests
import re

# KONFIGURACE
USERNAME = "Pellarhodon"
URL = f"https://r6.apitab.com/search/uplay/{USERNAME}"

def update_html():
    try:
        # 1. Získání dat z R6Tab API
        print(f"Connecting to R6 database for {USERNAME}...")
        response = requests.get(URL, timeout=10)
        data = response.json()
        
        if not data or "players" not in data:
            print("Player not found in database.")
            return

        # Výběr prvního nalezeného hráče
        player_id = list(data["players"].keys())[0]
        player = data["players"][player_id]
        
        # 2. Extrakce konkrétních hodnot
        stats = {
            "r6-lvl": str(player["stats"].get("level", 0)),
            "r6-rank": player["metadata"].get("rankname", "UNRANKED").upper(),
            "r6-mmr": str(player["stats"].get("score", 0)),
            "r6-kills": str(player["stats"].get("kills", 0)),
            "r6-aces": str(player["stats"].get("penta", 0)), # Penta kills = Aces
            "r6-time": f"{int(player['stats'].get('timeplayed', 0) // 3600)}H",
            "r6-op": player["metadata"].get("fav_op", "UNKNOWN").upper()
        }

        # 3. Načtení index.html a přepsání hodnot
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        for element_id, value in stats.items():
            # Najde id="..." a přepíše obsah mezi > a </span>
            pattern = rf'(id="{element_id}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{value}\2', content)

        # 4. Uložení změn
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Successfully synced: " + ", ".join([f"{k}:{v}" for k, v in stats.items()]))

    except Exception as e:
        print(f"Error during update: {e}")

if __name__ == "__main__":
    update_html()
