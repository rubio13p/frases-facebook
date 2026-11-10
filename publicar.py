import os, random, base64, requests

OPENAI_KEY = os.environ["OPENAI_API_KEY"]
PAGE_ID = os.environ["FB_PAGE_ID"]
PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]

temas = [
    # Motivación
    "perseverance", "self-love", "never giving up", "gratitude", "discipline",
    "overcoming fear", "new beginnings", "inner strength", "patience", "courage",
    "believing in yourself", "hard times", "dreams",
    # Educación financiera
    "saving money", "investing early", "financial freedom", "avoiding debt",
    "building wealth slowly", "multiple income streams", "budgeting",
    "the power of compound interest", "spending less than you earn",
    "money mindset", "paying yourself first", "emergency fund",
]
tema = random.choice(temas)
headers = {"Authorization": f"Bearer {OPENAI_KEY}"}

# 1. Crear la frase
r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
    "model": "gpt-5-mini",
    "messages": [{"role": "user", "content":
        f"Write one original, short, powerful quote in English about {tema}. "
        "It can be motivational or practical financial wisdom. "
        "Maximum 20 words. Make it emotional and highly shareable. "
        "Reply with only the quote, no quotation marks, no author."}]
})
r.raise_for_status()
frase = r.json()["choices"][0]["message"]["content"].strip()
print("Tema:", tema)
print("Frase:", frase)

# 2. Crear la imagen
r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json={
    "model": "gpt-image-2",
    "size": "1024x1024",
    "quality": "medium",
    "prompt": f"A beautiful, inspiring background photo (sunrise, mountains, ocean, city skyline or nature). "
              f"In the center, large, elegant, perfectly spelled white text with a soft shadow: \"{frase}\". "
              "Clean, modern, easy to read on a phone."
})
r.raise_for_status()
imagen = base64.b64decode(r.json()["data"][0]["b64_json"])

# 3. Publicar en Facebook
texto = (f"{frase}\n\n💬 Tag someone who needs to read this today.\n\n"
         "#motivation #inspiration #mindset #financialfreedom #money")
r = requests.post(f"https://graph.facebook.com/v27.0/{PAGE_ID}/photos",
    data={"message": texto, "access_token": PAGE_TOKEN},
    files={"source": ("frase.png", imagen, "image/png")})
print(r.json())
r.raise_for_status()
print("¡Publicado!")
