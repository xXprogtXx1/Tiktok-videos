import requests
import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_image(query="nature", filename="image.jpg"):
    print("📸 Scarico immagine da Pexels...")
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    r = requests.get(url, headers=headers)
    data = r.json()
    image_url = data["photos"][0]["src"]["large"]
    img = requests.get(image_url).content
    with open(filename, "wb") as f:
        f.write(img)
    print("✅ Immagine scaricata")
    return filename

def text_to_speech(text, filename="audio.mp3"):
    print("🎤 Genero audio...")
    tts = gTTS(text=text, lang="it")
    tts.save(filename)
    return filename

def create_text_image(text, output="text.png", size=(1080, 200), fontsize=40):
    """Crea immagine con testo usando Pillow"""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", fontsize)
    except:
        font = ImageFont.load_default()

    # Calcolo centratura testo
    w, h = draw.textsize(text, font=font)
    position = ((size[0] - w) // 2, (size[1] - h) // 2)
    draw.text(position, text, font=font, fill="white")
    img.save(output)
    return output

def create_video(image_file, audio_file, text, output="final_video.mp4"):
    print("🎬 Creo il video...")

    # Clip immagine
    audio_clip = AudioFileClip(audio_file)
    img_clip = ImageClip(image_file).set_duration(audio_clip.duration)

    # Clip testo come immagine
    text_img = create_text_image(text)
    text_clip = ImageClip(text_img).set_duration(audio_clip.duration).set_position(("center", "bottom"))

    # Composizione
    final = CompositeVideoClip([img_clip, text_clip]).set_audio(audio_clip)
    final.write_videofile(output, fps=24)
    print("✅ Video creato:", output)

if __name__ == "__main__":
    story_text = "C'era una volta un mondo magico nascosto tra le stelle..."
    image_file = get_image("fantasy landscape")
    audio_file = text_to_speech(story_text)
    create_video(image_file, audio_file, story_text)
