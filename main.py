import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ---- Inställningar ----
KEYWORDS = ["rost", "obes", "felkod", "små fel", "småfel", "projekt", "besikt", "motorfel"]
MAX_PRIS = 15000
BLOCKET_URL = f"https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cg=1020&st=s&ps=0&pe={MAX_PRIS}"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def hitta_annons_urler():
    response = requests.get(BLOCKET_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    annonser = soup.find_all("a", href=True)

    matchningar = []
    for annons in annonser:
        text = annons.get_text().lower()
        url = "https://www.blocket.se" + annons["href"]
        if any(keyword in text for keyword in KEYWORDS):
            matchningar.append((text.strip(), url))

    return matchningar

def skicka_discord_meddelande(meddelande):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ Webhook-URL saknas!")
        return

    data = {
        "content": meddelande
    }
    requests.post(webhook_url, json=data)

if __name__ == "__main__":
    resultat = hitta_annons_urler()
    if resultat:
        for titel, url in resultat:
            meddelande = f"🚗 **Ny bil hittad!**\n{titel}\n🔗 {url}"
            skicka_discord_meddelande(meddelande)
    else:
        print("Inga matchande annonser hittades.")
if __name__ == "__main__":
    skicka_discord_meddelande("🤖 Bot körs! Testmeddelande.")
    resultat = hitta_annons_urler()
    if resultat:
        for titel, url in resultat:
            meddelande = f"🚗 **Ny bil hittad!**\n{titel}\n🔗 {url}"
            skicka_discord_meddelande(meddelande)
    else:
        print("Inga matchande annonser hittades.")
