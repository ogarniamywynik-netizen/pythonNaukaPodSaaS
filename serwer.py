from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"status": "Serwer działa poprawnie!"}

@app.get("/analiza")
def analiza(url: str):
    import dotenv
    import os
    import anthropic
    import requests
    from bs4 import BeautifulSoup

    dotenv.load_dotenv()

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return {"error": f'Błąd podczas pobierania strony: {e}'}

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

    return {"schemat_idealnego_klienta": message.content[0].text}