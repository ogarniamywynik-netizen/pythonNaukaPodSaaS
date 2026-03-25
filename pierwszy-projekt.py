import dotenv
import os
import anthropic
import requests
from bs4 import BeautifulSoup

dotenv.load_dotenv()

url = input("Podaj URL: ")
try:
    response = requests.get(url)
except requests.exceptions.RequestException as e:
    print(f'Błąd podczas pobierania strony: {e}')
    exit(1)
soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find('title').text
meta = soup.find('meta', {'name': 'description'})
meta_description = meta['content'] if meta else 'Brak opisu'
h2 = soup.findAll('h2')

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=600,
    messages=[{
        'role': 'user',
        'content': f'Stórz schemat idealnego klienta dla strony:\nTytuł: {title}\nOpis: {meta_description}\nNagłówki H2:' + 
        '\n'.join([h.get_text() for h in h2])
    }],
)

with open ('idealny_klient.txt', 'w', encoding='utf-8') as plik:
    plik.write(message.content[0].text)
print("Schemat idealnego klienta został zapisany w pliku 'idealny_klient.txt'")