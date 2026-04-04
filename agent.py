from tavily import TavilyClient
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

branza = input("Podaj branżę: ")

wyniki = tavily.search("sklepy {branza} Polska")

konkurenci = "\n".join([f"{w['title']} - {w['url']}" for w in wyniki["results"]])

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1000,
    messages=[{
        "role": "user",
        "content": f"""Przeanalizuj tę konkurencję dla sklepu w branży {branza}:

{konkurenci}

Powiedz:
1. Kto jest głównym konkurentem
2. Jakie mają przewagi
3. Gdzie jest luka rynkowa"""
    }]
)

print(message.content[0].text)