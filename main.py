import os
import requests
from bs4 import BeautifulSoup

MAX_PRIS = 15000
BLOCKET_URL = f"https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cg=1020&st=s&ps=0&pe={MAX_PRIS}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def hitta_annons_urler():
    response = requests.get(BLOCKET_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    # Hitta alla annonser - här plockar vi länkar till bilarna
    annonser = soup.find_all("a", href=True)

    url_lista = []
    for annons in annonser:
        href = annons["href"]
        if "/annons/" in href:  # Säkra att det är en annons-länk
            url = "https://www.blocket.se" + href
            if url not in url_lista:
                url_lista.append(url)

    return url_lista

def skicka_discord_meddelande(meddelande):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ Webhook-URL saknas!")
        return

    data = {"content": meddelande}
    requests.post(webhook_url, json=data)

if __name__ == "__main__":
    annonser = hitta_annons_urler()
    if annonser:
        for url in annonser:
            skicka_discord_meddelande(f"🚗 Bil under 15 000 kr:\n{url}")
    else:
        print("Inga annonser hittades.")
