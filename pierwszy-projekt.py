import dotenv
import os
import anthropic

dotenv.load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

industry = input("Podaj swoją branżę: ")

wiadomosc = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=600,
    messages=[{
    "role": "user",
    "content": f"Jesteś ekspertem w dziedzinie {industry}. Napisz mi 5 pomysłów na biznes w tej branży.",
    }],
)
print(wiadomosc.content[0].text)