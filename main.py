import os, requests, random
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip

# ===== 1. Testo della storia =====
story_text = os.getenv("STORY_TEXT", "C'era una volta una notte molto buia...")

# ===== 2. Genera voce narrata =====
tts = gTTS(story_text, lang="it")
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
total_duration = audio.duration

# ===== 3. Sfondo random da Pexels =====
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_API_KEY:
    raise ValueError("⚠️ Devi impostare la variabile PEXELS_API_KEY")

headers = {"Authorization": PEXELS_API_KEY}
query = random.choice(["dark forest", "creepy house", "night sky", "abandoned building"])
url = f"https://api.pexels.com/videos/search?query={query}&per_page=5"
resp = requests.get(url, headers=headers).json()

if resp.get("videos"):
    video_url = resp["videos"][0]["video_files"][0]["link"]
    with open("background.mp4", "wb") as f:
        f.write(requests.get(video_url).content)
    background = VideoFileClip("background.mp4").resize((1080,1920)).subclip(0, total_duration)
else:
    background = ImageClip("black.jpg").set_duration(total_duration).resize((1080,1920))

# ===== 4. Sottotitoli sincronizzati =====
sentences = [s.strip() for s in story_text.split(".") if s.strip()]
total_chars = sum(len(s) for s in sentences)
clips = []
start = 0
for s in sentences:
    dur = (len(s) / total_chars) * total_duration
    txt = TextClip(s, fontsize=50, color="white", size=(1000,None),
                   method="caption", align="center"
                  ).set_position(("center","bottom")).set_duration(dur).set_start(start)
    clips.append(txt)
    start += dur

# ===== 5. Composizione =====
final = CompositeVideoClip([background.set_duration(total_duration)] + clips)
final = final.set_audio(audio)

# ===== 6. Esporta =====
final.write_videofile("output_tiktok.mp4", fps=30, codec="libx264", audio_codec="aac")
