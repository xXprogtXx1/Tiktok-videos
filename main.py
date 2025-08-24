import os
import requests
from gtts import gTTS
from moviepy.editor import *
import textwrap

# ========================
# Config
# ========================
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
STORY_TEXT = os.getenv("STORY_TEXT", "Era una notte buia e tempestosa...")

VIDEO_FILE = "output_tiktok.mp4"
AUDIO_FILE = "story_audio.mp3"
IMAGE_FILE = "background.jpg"

# ========================
# 1. Scarica immagine da Pexels
# ========================
headers = {"Authorization": PEXELS_API_KEY}
query = "dark night storm"
url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

print("📸 Scarico immagine da Pexels...")
response = requests.get(url, headers=headers)
data = response.json()

if "photos" not in data or len(data["photos"]) == 0:
    raise Exception("❌ Nessuna immagine trovata su Pexels.")

image_url = data["photos"][0]["src"]["large"]
img_data = requests.get(image_url).content

with open(IMAGE_FILE, "wb") as f:
    f.write(img_data)

print("✅ Immagine scaricata")

# ========================
# 2. Genera audio con gTTS
# ========================
print("🎤 Genero audio...")
tts = gTTS(STORY_TEXT, lang="it")
tts.save(AUDIO_FILE)

audio_clip = AudioFileClip(AUDIO_FILE)

# ========================
# 3. Crea video con MoviePy
# ========================
print("🎬 Creo il video...")

# Clip immagine di sfondo
background = ImageClip(IMAGE_FILE).set_duration(audio_clip.duration)

# Spezza il testo in più righe (per evitare overflow)
wrapped_text = "\n".join(textwrap.wrap(STORY_TEXT, width=40))

# Usa TextClip con metodo PIL invece di ImageMagick
txt_clip = TextClip(
    wrapped_text,
    fontsize=40,
    color="white",
    font="DejaVu-Sans",   # font standard in Linux
    method="caption",     # usa PIL invece di ImageMagick
    size=background.size
).set_duration(audio_clip.duration).set_position("center")

# Composizione video
final = CompositeVideoClip([background, txt_clip])
final = final.set_audio(audio_clip)

# ========================
# 4. Esporta
# ========================
print("💾 Esporto video finale...")
final.write_videofile(VIDEO_FILE, fps=24)

print("✅ Video creato:", VIDEO_FILE)
