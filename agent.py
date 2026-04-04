from tavily import TavilyClient
from dotenv import load_dotenv
import os
import anthropic
import requests
from bs4 import BeautifulSoup

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

branza = input("Podaj branżę: ")

wyniki = tavily.search(f"sklepy {branza} Polska")

urlsList = []

for wynik in wyniki["results"]:
    url = wynik['url']
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f'Wystąpił błąd: {e}')
        exit(1)
    urlTextParsed = BeautifulSoup(response.text, "html.parser")
    text = urlTextParsed.get_text(separator=" ", strip=True)[:2000]
    urlsList.append(text)

konkurenci_z_tekstem = "\n\n".join([
    f"URL: {wyniki['results'][i]['url']}\nTreść: {urlsList[i]}"
    for i in range(len(urlsList))
])

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": f"""Przeanalizuj tę konkurencję dla sklepu w branży {branza}:

{konkurenci_z_tekstem}

Powiedz:
1. Kto jest głównym konkurentem
2. Jakie mają przewagi
3. Gdzie jest luka rynkowa"""
    }]
)

print(message.content[0].text)