import requests
import re

# KONFIGURACE - Zkusíme tohle API, je teď stabilnější
USERNAME = "Pellarhodon"
URL = f"https://r6.apitab.com/search/uplay/{USERNAME}"

def update_html():
    try:
        print(f"Checking database for: {USERNAME}...")
        response = requests.get(URL, timeout=15)
        data = response.json()
        
        if not data or "players" not in data or not data["players"]:
            print("CRITICAL: Player not found in R6Tab database!")
            return

        # Vytáhneme první shodu
        pid = list(data["players"].keys())[0]
        player = data["players"][pid]
        
        # NAČTENÍ REÁLNÝCH DAT
        # Pokud jsi Unranked nebo API blbne, dáme tam aspoň real Level
        real_lvl = str(player.get("stats", {}).get("level", "373"))
        real_rank = player.get("metadata", {}).get("rankname", "FETCHING...").upper()
        real_mmr = str(player.get("stats", {}).get("score", "0"))
        real_kills = str(player.get("stats", {}).get("kills", "0"))
        real_aces = str(player.get("stats", {}).get("penta", "0"))
        
        # Čas (přepočet na hodiny)
        seconds = player.get("stats", {}).get("timeplayed", 0)
        real_time = f"{int(seconds // 3600)}H"
        
        # Operátor
        real_op = player.get("metadata", {}).get("fav_op", "UNKNOWN").upper()

        print(f"DATA FOUND: {real_rank} | MMR: {real_mmr} | LVL: {real_lvl}")

        # ZÁPIS DO SOUBORU
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        stats_map = {
            "r6-lvl": real_lvl,
            "r6-rank": real_rank,
            "r6-mmr": real_mmr,
            "r6-kills": real_kills,
            "r6-aces": real_aces,
            "r6-time": real_time,
            "r6-op": real_op
        }

        for eid, val in stats_map.items():
            pattern = rf'(id="{eid}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{val}\2', content)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("HTML UPDATE: SUCCESSFUL")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    update_html()
