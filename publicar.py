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
    "thick stacks of US hundred-dollar bills on a dark polished wooden table, a glass of whiskey, blurred night city skyline through a large window behind",
    "a shower of hundred-dollar bills falling into an old open wooden treasure chest, dark textured wall behind",
    "a hand holding a thick wad of dollar bills next to luxury car keys and a whiskey glass on a black marble table, city lights at night",
    "a glowing golden hundred-dollar bill surrounded by gold coins, lit candles and a fountain pen",
    "two rolls of dollar bills tied with braided leather on black leather surface with scattered gold coins",
    "an ancient stone portal with a waterfall of dollar bills pouring down, golden light from above, a golden lamp on the floor",
    "an open brown leather bag full of stacked dollar bills under a warm desk lamp, books and a pen on a wooden desk",
    "a wet city street at night with dollar bills and copper coins on the ground, steam and blurred lights",
    "an ornate vintage banknote engraving with gold details and a fountain pen on aged paper",
    "hundred-dollar bills flying in the air over a dark background, dramatic golden backlight",
    "a vintage safe open, filled with gold bars and cash, warm spotlight in a dark room",
    "a private jet interior with cash on a leather seat and champagne glass, golden sunset through window",
    "a mahogany executive desk with stacks of cash, a luxury watch and a cigar, dim golden lamp",
    "gold coins spilling from a velvet bag onto dark wood, candlelight glow",
    "a briefcase open full of hundred-dollar bills on a rooftop at night, skyscrapers behind",
    "a fan of hundred-dollar bills held by a hand in a suit, dark luxury lounge background",
    "a pile of gold bars and coins in a dark vault, shimmering golden reflections",
    "an antique compass, old map and a stack of dollar bills on a wooden table, warm lantern light",
    "a crystal glass of whiskey beside a tower of stacked cash, bokeh golden lights",
    "dollar bills raining down on a luxury penthouse balcony overlooking the city at night",
]

colores = ["white", "golden yellow", "soft cream", "bright gold"]

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
    "prompt": f"Ultra-realistic cinematic photo, luxury wealth and abundance theme. Scene: {estilo}. "
              "Dark moody atmosphere, warm golden lighting, deep shadows, rich textures, "
              "shallow depth of field, high detail, premium look. "
              f"Large, elegant, perfectly spelled {color} serif text: \"{frase}\". "
              "Place the text in a clean darker area of the image (top or bottom) "
              "with a subtle shadow so it is easy to read on a phone."
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
