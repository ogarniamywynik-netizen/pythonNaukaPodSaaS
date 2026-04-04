from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
import os
import anthropic
from dotenv import load_dotenv

tools = [
    {
        "name": "web_search",
        "description": "Przeszukuje internet w poszukiwaniu informacji o konkurencji",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Zapytanie do wyszukiwarki"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "scrape_url",
        "description": "pobiera tekst ze strony internetowej według url",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "url strony"
                }
            },
            "required": ["url"]
        }
    }
]

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def web_search(query: str) -> str:
    wyniki = tavily.search(query, max_results=5)
    return "\n".join([f"{w['title']} - {w['url']}" for w in wyniki["results"]])

def scrape_url(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)[:3000]

branza = input("Podaj branżę: ")

messages = [
    {
        "role": "user",
        "content": f"Przeanalizuj konkurencję dla sklepu w branży {branza}. Znajdź głównych konkurentów, ich przewagi i luki rynkowe."
    }
]
print("Start agenta...")
while True:
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        tools=tools,
        messages=messages
    )
    print(f"stop_reason: {response.stop_reason}")
    
    if response.stop_reason == "end_turn":
        print(response.content[0].text)
        break
    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})
        
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Używam narzędzia: {block.name}")
                if block.name == "web_search":
                    wynik = web_search(block.input["query"])
                elif block.name == "scrape_url":
                    wynik = scrape_url(block.input["url"])
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": wynik
                })
        
        messages.append({"role": "user", "content": tool_results})