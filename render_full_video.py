import os
import subprocess
import glob

PROJECT_DIR = r"C:\Users\trung\.gemini\antigravity\scratch\leo_animated_story"
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
SUBS_DIR = os.path.join(PROJECT_DIR, "subtitles")
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
CLIPS_DIR = os.path.join(PROJECT_DIR, "clips")
CONCAT_FILE = os.path.join(PROJECT_DIR, "concat_list.txt")
CONCAT_VIDEO = os.path.join(PROJECT_DIR, "video_temp_no_bgm.mp4")
BGM_AUDIO = os.path.join(AUDIO_DIR, "bgm.wav")
FINAL_VIDEO = os.path.join(PROJECT_DIR, "leo_sunny_day_60s.mp4")

os.makedirs(CLIPS_DIR, exist_ok=True)

# 10 Scenes motion configurations (6.0s = 150 frames @ 25fps)
SCENE_MOTIONS = [
    # 1: Leo waves hello - gentle zoom in center
    "zoompan=z='min(zoom+0.0010,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 2: Leo shows green backpack - pan left to right
    "zoompan=z='1.10':x='if(lte(on,1),(iw-iw/zoom)/3,x+1.2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 3: Walking through forest - tracking pan
    "zoompan=z='1.12':x='if(lte(on,1),(iw-iw/zoom)/4,x+1.5)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 4: Look up at apple - tilt up
    "zoompan=z='min(zoom+0.0012,1.18)':x='iw/2-(iw/zoom/2)':y='if(lte(on,1),ih*0.25,max(0,y-0.8))':d=150:s=1280x720:fps=25",
    # 5: Macro apple - slow push in
    "zoompan=z='min(zoom+0.0014,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 6: Holding apple - gentle focus
    "zoompan=z='min(zoom+0.0008,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 7: Bite apple - close up punch in
    "zoompan=z='min(zoom+0.0015,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 8: Butterfly on nose - slow floating zoom
    "zoompan=z='min(zoom+0.0010,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 9: Friends with butterfly - gentle pan
    "zoompan=z='1.12':x='if(lte(on,1),(iw-iw/zoom)*0.75,x-1.2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
    # 10: Sunset goodbye - dolly out
    "zoompan=z='max(1.001,1.15-on*0.001)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1280x720:fps=25",
]

clip_paths = []

for i in range(1, 11):
    img_path = os.path.join(IMAGES_DIR, f"scene_{i:02d}.jpg")
    sub_path = os.path.join(SUBS_DIR, f"sub_{i:02d}.png")
    aud_path = os.path.join(AUDIO_DIR, f"scene_{i:02d}.mp3")
    out_clip = os.path.join(CLIPS_DIR, f"clip_{i:02d}.mp4")
    
    motion_filter = SCENE_MOTIONS[i - 1]
    
    print(f"Rendering Clip {i:02d}/10...")
    filter_graph = (
        f"[0:v]scale=2560x1440,{motion_filter}[base];"
        f"[base][1:v]overlay=0:0[vout];"
        f"[2:a]adelay=350|350,apad=whole_dur=6.0,atrim=end=6.0[aout]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "6", "-i", img_path,
        "-loop", "1", "-t", "6", "-i", sub_path,
        "-i", aud_path,
        "-filter_complex", filter_graph,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", out_clip
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering clip {i}:\n{res.stderr}")
        raise RuntimeError(f"Clip {i} failed")
    clip_paths.append(out_clip)

print("All 10 clips rendered successfully!")

# Write concat file
with open(CONCAT_FILE, "w", encoding="utf-8") as f:
    for c in clip_paths:
        escaped = c.replace("\\", "/")
        f.write(f"file '{escaped}'\n")

# Concatenate all clips
print("Concatenating 10 clips into video_temp...")
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", CONCAT_FILE,
    "-c", "copy", CONCAT_VIDEO
]
subprocess.run(cmd_concat, check=True)

# Mix Voiceover + BGM
print("Mixing Voiceover with synchronized BGM...")
cmd_mix = [
    "ffmpeg", "-y",
    "-i", CONCAT_VIDEO,
    "-i", BGM_AUDIO,
    "-filter_complex", "[0:a]volume=1.0[vocal];[1:a]volume=0.22[music];[vocal][music]amix=inputs=2:duration=first:dropout_transition=2[aout]",
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    FINAL_VIDEO
]
subprocess.run(cmd_mix, check=True)

# Final probe
cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", FINAL_VIDEO]
res_probe = subprocess.run(cmd_probe, capture_output=True, text=True)
print("FINAL VIDEO RESULT:")
print(res_probe.stdout)
print(f"Master file saved at: {FINAL_VIDEO}")
