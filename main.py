import os
import requests
from gtts import gTTS
import moviepy.editor as mp

# ====== TESTO DELLA STORIA ======
story_text = os.getenv("STORY_TEXT", "Era una notte buia e tempestosa...")

# ====== TTS (voce narrante) ======
tts = gTTS(story_text, lang="it")
tts.save("story.mp3")

# ====== SCARICA UN VIDEO RANDOM DA PEXELS ======
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
headers = {"Authorization": PEXELS_API_KEY}
url = "https://api.pexels.com/videos/search?query=nature&per_page=1"

response = requests.get(url, headers=headers).json()
video_url = response["videos"][0]["video_files"][0]["link"]

video_data = requests.get(video_url).content
with open("background.mp4", "wb") as f:
    f.write(video_data)

# ====== MONTA VIDEO ======
video_clip = mp.VideoFileClip("background.mp4").subclip(0, 15)  # primi 15s
audio_clip = mp.AudioFileClip("story.mp3")

# aggiungi audio al video
final_clip = video_clip.set_audio(audio_clip)

# aggiungi testo sovrapposto
txt_clip = mp.TextClip(story_text, fontsize=40, color='white', size=video_clip.size, method="caption")
txt_clip = txt_clip.set_duration(final_clip.duration).set_pos("center")

final = mp.CompositeVideoClip([final_clip, txt_clip])

# ====== ESPORTA ======
final.write_videofile("output_tiktok.mp4", fps=24)
