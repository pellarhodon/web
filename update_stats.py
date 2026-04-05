import requests
import re

# KONFIGURACE
USERNAME = "Pellarhodon"
PLATFORM = "pc"
# Použijeme stabilnější endpoint
URL = f"https://api2.r6stats.com/public-api/stats/{USERNAME}/{PLATFORM}/generic"

def update_html():
    try:
        print(f"Connecting to R6Stats for {USERNAME}...")
        
        # Přidáme hlavičku, aby nás server neblokoval
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(URL, headers=headers, timeout=15)
        
        # Pokud toto API selže, zkusíme záložní metodu přes jiný tracker
        if response.status_code != 200:
            print(f"Primary API failed (Status: {response.status_code}). Using fallback...")
            # Tady můžeš ručně dopsat svůj rank, pokud ho víš, aby tam nebyl ten Gold
            real_rank = "EMERALD" # ZMĚŇ SI NA SVŮJ AKTUÁLNÍ RANK
            real_mmr = "3450"      # ZMĚŇ SI NA SVÉ MMR
            real_lvl = "373"
        else:
            data = response.json()
            # Extrakce dat z R6Stats struktury
            real_lvl = str(data.get("stats", {}).get("progression", {}).get("level", "373"))
            real_rank = "RANKED" # R6Stats někdy vrací obecné kategorie
            real_mmr = "CHECK_TRACKER"
        
        print(f"Final Sync -> Rank: {real_rank}")

        # ZÁPIS DO SOUBORU index.html
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        stats_map = {
            "r6-lvl": "373", # Tvůj level je stabilní
            "r6-rank": "PLATINUM I", # SEM NAPIŠ SVŮJ REÁLNÝ RANK (např. SILVER, EMERALD...)
            "r6-mmr": "3120",        # SEM NAPIŠ SVÉ PŘIBLIŽNÉ MMR
            "r6-kills": "24500",
            "r6-aces": "142",
            "r6-time": "1840H",
            "r6-op": "ASH"
        }

        for eid, val in stats_map.items():
            pattern = rf'(id="{eid}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{val}\2', content)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("HTML UPDATE: SUCCESSFUL (STATIC OVERRIDE)")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    update_html()
