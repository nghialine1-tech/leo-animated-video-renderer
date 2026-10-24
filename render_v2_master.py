import os
import sys
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
CLIPS_DIR = os.path.join(BASE_DIR, "clips_v2")
CONCAT_FILE = os.path.join(BASE_DIR, "concat_v2.txt")
CONCAT_VIDEO = os.path.join(BASE_DIR, "video_v2_temp.mp4")
BGM_AUDIO = os.path.join(AUDIO_DIR, "bgm.wav")
SFX_AUDIO = os.path.join(AUDIO_DIR, "sfx.wav")
FINAL_VIDEO = os.path.join(BASE_DIR, "leo_sunny_day_60s_v2_master.mp4")

os.makedirs(CLIPS_DIR, exist_ok=True)

# 10 Scenes Configurations
SCENES = [
    {
        "id": 1,
        "words": ["Wait!", "Look", "at", "Leo!", "Let", "us", "explore!"],
        "vi": "Khoan đã! Nhìn Leo này! Hãy cùng khám phá nào!",
        "audio_start": 0.35,
        "audio_dur": 2.8,
        "motion": "zoom_in"
    },
    {
        "id": 2,
        "words": ["This", "is", "my", "green", "backpack."],
        "vi": "Đây là chiếc ba lô màu xanh lá của tớ.",
        "audio_start": 0.4,
        "audio_dur": 2.5,
        "motion": "pan_right"
    },
    {
        "id": 3,
        "words": ["I", "like", "walking", "in", "the", "forest."],
        "vi": "Tớ thích đi dạo trong rừng.",
        "audio_start": 0.4,
        "audio_dur": 2.6,
        "motion": "tracking"
    },
    {
        "id": 4,
        "words": ["Look!", "A", "big", "red", "apple!"],
        "vi": "Nhìn kìa! Một quả táo đỏ to đùng!",
        "audio_start": 0.35,
        "audio_dur": 2.6,
        "motion": "tilt_up"
    },
    {
        "id": 5,
        "words": ["It", "is", "round", "and", "very", "red."],
        "vi": "Nó tròn và rất là đỏ.",
        "audio_start": 0.4,
        "audio_dur": 2.5,
        "motion": "macro_zoom"
    },
    {
        "id": 6,
        "words": ["I", "have", "the", "apple", "now."],
        "vi": "Giờ tớ có quả táo rồi.",
        "audio_start": 0.35,
        "audio_dur": 2.2,
        "motion": "push_in"
    },
    {
        "id": 7,
        "words": ["Mmm!", "It", "is", "sweet", "and", "yummy."],
        "vi": "Mmm! Nó ngọt và ngon tuyệt cú mèo.",
        "audio_start": 0.4,
        "audio_dur": 3.0,
        "motion": "bite_zoom"
    },
    {
        "id": 8,
        "words": ["A", "pretty", "butterfly", "is", "here."],
        "vi": "Một bạn bướm xinh đẹp đang ở đây.",
        "audio_start": 0.4,
        "audio_dur": 2.5,
        "motion": "float_zoom"
    },
    {
        "id": 9,
        "words": ["We", "are", "good", "happy", "friends."],
        "vi": "Chúng tớ là những người bạn tốt vui vẻ.",
        "audio_start": 0.4,
        "audio_dur": 2.5,
        "motion": "pan_left"
    },
    {
        "id": 10,
        "words": ["What", "fruit", "do", "you", "like?", "See", "you", "soon!"],
        "vi": "Bạn thích quả gì? Hãy bình luận nhé! Hẹn sớm gặp lại!",
        "audio_start": 0.35,
        "audio_dur": 3.2,
        "motion": "dolly_out"
    }
]

# Load Fonts from repo fonts dir or fallback
def get_font(filename, size):
    path = os.path.join(FONTS_DIR, filename)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    # Check Windows/Linux system fonts
    for p in [f"/usr/share/fonts/truetype/dejavu/{filename}", f"C:\\Windows\\Fonts\\{filename}"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_active = get_font("segoeuib.ttf", 40)
font_normal = get_font("segoeuib.ttf", 35)
font_vi = get_font("segoeui.ttf", 24)
font_badge = get_font("segoeuib.ttf", 20)

clip_paths = []

for sc in SCENES:
    sc_id = sc["id"]
    print(f"Rendering Upgraded Clip {sc_id:02d}/10...")
    
    img_path = os.path.join(IMAGES_DIR, f"scene_{sc_id:02d}.jpg")
    aud_path = os.path.join(AUDIO_DIR, f"scene_{sc_id:02d}.mp3")
    out_clip = os.path.join(CLIPS_DIR, f"v2_clip_{sc_id:02d}.mp4")
    
    base_img = Image.open(img_path).convert('RGB')
    w_orig, h_orig = base_img.size
    
    words = sc["words"]
    vi_text = sc["vi"]
    audio_start = sc["audio_start"]
    audio_dur = sc["audio_dur"]
    word_dur = audio_dur / len(words)
    motion_type = sc["motion"]
    
    # Particle seeds per scene
    random.seed(42 + sc_id)
    particles = [
        {
            'x': random.randint(80, 1200),
            'y': random.randint(80, 620),
            'speed': random.uniform(0.8, 2.2),
            'size': random.randint(3, 6),
            'phase': random.uniform(0, 6.28)
        }
        for _ in range(22)
    ]
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1280x720', '-r', '25',
        '-i', '-',
        '-i', aud_path,
        '-filter_complex', '[1:a]adelay=350|350,apad=whole_dur=6.0,atrim=end=6.0[aout]',
        '-map', '0:v', '-map', '[aout]',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', '-crf', '20',
        '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
        '-shortest', out_clip
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    for f in range(150):
        t_sec = f / 25.0
        progress = f / 150.0
        
        # Camera Ken Burns Motion
        if motion_type == "zoom_in":
            zoom = 1.0 + 0.15 * progress
            cx, cy = w_orig / 2, h_orig / 2
        elif motion_type == "pan_right":
            zoom = 1.10
            cx = w_orig * (0.42 + 0.16 * progress)
            cy = h_orig / 2
        elif motion_type == "tracking":
            zoom = 1.12
            cx = w_orig * (0.38 + 0.24 * progress)
            cy = h_orig / 2
        elif motion_type == "tilt_up":
            zoom = 1.05 + 0.12 * progress
            cx = w_orig / 2
            cy = h_orig * (0.58 - 0.16 * progress)
        elif motion_type == "macro_zoom":
            zoom = 1.05 + 0.18 * progress
            cx, cy = w_orig / 2, h_orig / 2
        elif motion_type == "push_in":
            zoom = 1.0 + 0.12 * progress
            cx, cy = w_orig / 2, h_orig / 2
        elif motion_type == "bite_zoom":
            zoom = 1.08 + 0.20 * progress
            cx, cy = w_orig / 2, h_orig * 0.48
        elif motion_type == "float_zoom":
            zoom = 1.04 + 0.12 * math.sin(progress * math.pi)
            cx = w_orig / 2 + math.sin(progress * 4.0) * 15
            cy = h_orig / 2
        elif motion_type == "pan_left":
            zoom = 1.10
            cx = w_orig * (0.58 - 0.16 * progress)
            cy = h_orig / 2
        elif motion_type == "dolly_out":
            zoom = 1.16 - 0.15 * progress
            cx, cy = w_orig / 2, h_orig / 2
        else:
            zoom = 1.0
            cx, cy = w_orig / 2, h_orig / 2
            
        crop_w = int(w_orig / zoom)
        crop_h = int(h_orig / zoom)
        crop_x = int(max(0, min(w_orig - crop_w, cx - crop_w / 2)))
        crop_y = int(max(0, min(h_orig - crop_h, cy - crop_h / 2)))
        
        frame = base_img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h)).resize((1280, 720), Image.Resampling.BILINEAR)
        draw = ImageDraw.Draw(frame)
        
        # Floating Sunlight Sparkles
        for p in particles:
            py = (p['y'] - f * p['speed']) % 680
            px = p['x'] + int(math.sin(f * 0.08 + p['phase']) * 6)
            alpha_factor = 0.4 + 0.6 * math.sin(f * 0.12 + p['phase'])
            r_sz = int(p['size'] * alpha_factor) + 1
            draw.ellipse([px - r_sz, py - r_sz, px + r_sz, py + r_sz], fill=(255, 245, 170))
            draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(255, 255, 255))
            
        # Top-left Branding Badge
        draw.rounded_rectangle([30, 25, 290, 68], radius=12, fill=(15, 23, 42), outline=(255, 215, 0), width=2)
        draw.text((45, 34), '🌟 English A1 with Leo', font=font_badge, fill=(255, 235, 120))
        
        # Word highlight index
        active_idx = -1
        if t_sec >= audio_start:
            rel_t = t_sec - audio_start
            active_idx = int(rel_t / word_dur)
            if active_idx >= len(words):
                active_idx = len(words) - 1 if t_sec < audio_start + audio_dur + 0.6 else -2
                
        # Subtitle Container Pill
        box_w = 920
        box_h = 105
        box_x0 = (1280 - box_w) // 2
        box_y0 = 580
        draw.rounded_rectangle([box_x0, box_y0, box_x0 + box_w, box_y0 + box_h], radius=22, fill=(12, 18, 34), outline=(255, 215, 0), width=3)
        
        # Measure words
        total_w = 0
        word_metrics = []
        for i, w in enumerate(words):
            fnt = font_active if i == active_idx else font_normal
            bbox = draw.textbbox((0, 0), w, font=fnt)
            ww = bbox[2] - bbox[0]
            word_metrics.append((w, ww, fnt))
            total_w += ww + 12
        total_w -= 12
        
        start_x = (1280 - total_w) // 2
        curr_x = start_x
        
        for i, (w, ww, fnt) in enumerate(word_metrics):
            is_active = (i == active_idx)
            is_past = (i < active_idx)
            
            y_pos = box_y0 + (11 if is_active else 15)
            
            if is_active:
                # Bouncing golden dot above active word
                dot_x = curr_x + ww // 2
                dot_y = y_pos - 6 + int(math.sin(f * 0.8) * 2)
                draw.ellipse([dot_x - 4, dot_y - 4, dot_x + 4, dot_y + 4], fill=(255, 235, 0))
                color = (255, 235, 0)
            elif is_past:
                color = (255, 255, 255)
            else:
                color = (175, 185, 200)
                
            # Outline
            for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
                draw.text((curr_x + ox, y_pos + oy), w, font=fnt, fill=(0, 0, 0))
            draw.text((curr_x, y_pos), w, font=fnt, fill=color)
            curr_x += ww + 12
            
        # Vietnamese translation
        bbox_vi = draw.textbbox((0, 0), vi_text, font=font_vi)
        w_vi = bbox_vi[2] - bbox_vi[0]
        draw.text(((1280 - w_vi) // 2, box_y0 + 64), vi_text, font=font_vi, fill=(130, 225, 255))
        
        proc.stdin.write(frame.tobytes())
        
    proc.stdin.close()
    proc.wait()
    clip_paths.append(out_clip)

print("All 10 clips rendered!")

# Write concat list (use forward slashes for Linux & Windows compatibility)
with open(CONCAT_FILE, "w", encoding="utf-8") as f:
    for c in clip_paths:
        escaped = c.replace("\\", "/")
        f.write(f"file '{escaped}'\n")

# Concat
print("Concatenating clips...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", CONCAT_FILE, "-c", "copy", CONCAT_VIDEO], check=True)

# Final Mix: Video + Voiceover + SFX + BGM
print("Mixing Video + Voiceover + Synchronized SFX + Cozy Kalimba BGM...")
mix_filter = (
    "[0:a]volume=1.0[voice];"
    "[1:a]volume=0.18[bgm];"
    "[2:a]volume=0.65[sfx];"
    "[voice][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2[aout]"
)

cmd_master = [
    "ffmpeg", "-y",
    "-i", CONCAT_VIDEO,
    "-i", BGM_AUDIO,
    "-i", SFX_AUDIO,
    "-filter_complex", mix_filter,
    "-map", "0:v", "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    FINAL_VIDEO
]
subprocess.run(cmd_master, check=True)

print(f"Master upgraded video saved at: {FINAL_VIDEO}")
