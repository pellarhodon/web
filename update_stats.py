import re

# TVOJE REÁLNÁ DATA (ZDE JE UPRAVUJ)
stats_map = {
    "r6-lvl": "373",
    "r6-rank": "COPPER V",
    "r6-mmr": "1157",
    "r6-kills": "32145",
    "r6-aces": "158",
    "r6-time": "2140H",
    "r6-op": "IANA / AZAMI"
}

def update():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()

        for eid, val in stats_map.items():
            # Najde id="id-nazev">COKOLI</span> a nahradí to novou hodnotou
            pattern = rf'(id="{eid}">).*?(</span>)'
            content = re.sub(pattern, rf'\1{val}\2', content)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Synchronizace s index.html byla úspěšná.")
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    update()
