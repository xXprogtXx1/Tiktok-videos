import os
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"

STORY_TEXT = "L’uomo non smette mai di imparare, anche quando pensa di sapere tutto."
IMAGE_QUERY = "nature landscape"

# 🔧 Funzione per normalizzare il testo (rimuove caratteri non ASCII problematici)
def normalize_text(text: str) -> str:
    return (text.replace("’", "'")
                .replace("‘", "'")
                .replace("“", '"')
                .replace("”", '"'))

# 🔧 Scarica immagine da Pexels
def download_image(query, filename="image.jpg"):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    response = requests.get(PEXELS_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    image_url = data["photos"][0]["src"]["large"]
    img_data = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(img_data)
    return filename

# 🔧 Genera audio con gTTS
def generate_audio(text, filename="audio.mp3"):
    tts = gTTS(text=text, lang="it")
    tts.save(filename)
    return filename

# 🔧 Crea immagine con testo
def create_text_image(text, filename="text.png"):
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 40)  # supporta Unicode
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text(((W - w) / 2, H - h - 100), text, font=font, fill="white")
    img.save(filename)
    return filename

# 🔧 Crea video finale
def create_video(image_file, audio_file, text, output="final_video.mp4"):
    text = normalize_text(text)  # 👈 fix qui
    text_img = create_text_image(text)

    audio = AudioFileClip(audio_file)
    img_clip = ImageClip(image_file).set_duration(audio.duration).resize(height=1920)
    text_clip = ImageClip(text_img).set_duration(audio.duration)

    final = CompositeVideoClip([img_clip, text_clip.set_position("center")])
    final = final.set_audio(audio)
    final.write_videofile(output, fps=24)

# MAIN
if __name__ == "__main__":
    print("📸 Scarico immagine da Pexels...")
    image_file = download_image(IMAGE_QUERY)
    print("✅ Immagine scaricata")

    print("🎤 Genero audio...")
    audio_file = generate_audio(STORY_TEXT)
    print("✅ Audio generato")

    print("🎬 Creo il video...")
    create_video(image_file, audio_file, STORY_TEXT)
    print("✅ Video creato con successo!")
