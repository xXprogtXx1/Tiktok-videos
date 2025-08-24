import os
import requests
from gtts import gTTS
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
STORY_TEXT = os.getenv("STORY_TEXT", "Era una notte buia e tempestosa...")

# Scarica immagine da Pexels
def download_image(query="night sky", filename="background.jpg"):
    print("📸 Scarico immagine da Pexels...")
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    img_url = data["photos"][0]["src"]["large"]
    img_data = requests.get(img_url).content
    with open(filename, "wb") as f:
        f.write(img_data)
    print("✅ Immagine scaricata")
    return filename

# Genera audio dal testo
def text_to_speech(text, filename="audio.mp3"):
    print("🎤 Genero audio...")
    tts = gTTS(text=text, lang="it")
    tts.save(filename)
    return filename

# Crea immagine con testo
def create_text_image(text, filename="text.png"):
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Font di default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Ottieni bounding box del testo
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Posiziona al centro
    x = (1080 - text_w) // 2
    y = (1920 - text_h) // 2

    # Disegna testo bianco con ombra nera
    draw.text((x+4, y+4), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill="white")

    img.save(filename)
    return filename

# Crea video
def create_video(image_file, audio_file, text, output="output_tiktok.mp4"):
    print("🎬 Creo il video...")
    audio = AudioFileClip(audio_file)
    img_clip = ImageClip(image_file).set_duration(audio.duration).resize(height=1920)
    text_img = create_text_image(text)
    text_clip = ImageClip(text_img).set_duration(audio.duration)

    final = CompositeVideoClip([img_clip, text_clip.set_position("center")])
    final = final.set_audio(audio)
    final.write_videofile(output, fps=24)
    print("✅ Video creato:", output)

if __name__ == "__main__":
    image_file = download_image("story")
    audio_file = text_to_speech(STORY_TEXT)
    create_video(image_file, audio_file, STORY_TEXT)
