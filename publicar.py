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

estilos = [
    "a person working on a laptop in a cozy cafe, warm natural light",
    "a glass jar full of coins on a wooden table, close-up photo",
    "a rising stock market chart on a dark screen, modern and sleek",
    "a traveler with a backpack looking at a foreign city street",
    "a minimalist solid color background with subtle paper texture",
    "an open notebook with handwritten goals and a pen, top-down view",
    "a person running up stairs in a city at dawn",
    "a modern home office with plants and a big window",
    "a stack of books about money and a cup of coffee",
    "a young entrepreneur smiling at a small shop counter",
    "a chess board with one king standing, dramatic lighting",
    "a piggy bank with a small plant growing out of it",
    "a person meditating on a rooftop above a city at night",
    "an empty open road in the desert, cinematic style",
    "a luxury watch and a planner on a dark marble desk",
    "a bold gradient background in purple and orange, abstract shapes",
    "a hand dropping a coin into a jar, soft focus",
    "a person on a boat in calm turquoise water, freedom feeling",
    "a vintage typewriter with paper, retro style",
    "a city skyline at night with glowing lights, aerial view",
]

colores = [
    "white", "golden yellow", "black", "bright yellow",
    "emerald green", "soft cream", "bold red", "sky blue",
]

tema = random.choice(temas)
estilo = random.choice(estilos)
color = random.choice(colores)
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
print("Estilo:", estilo)
print("Color:", color)
print("Frase:", frase)

# 2. Crear la imagen
r = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json={
    "model": "gpt-image-2",
    "size": "1024x1024",
    "quality": "medium",
    "prompt": f"Background scene: {estilo}. "
              f"Large, elegant, perfectly spelled {color} text: \"{frase}\". "
              "The text must have strong contrast with the background "
              "(add a subtle outline or shadow if needed) so it is easy to read on a phone. "
              "Clean, modern, professional design."
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
