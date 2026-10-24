import os
import sys
import glob
import subprocess
import wave
import math
import struct

PROJECT_DIR = r"C:\Users\trung\.gemini\antigravity\scratch\leo_animated_story"
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
CLIPS_DIR = os.path.join(PROJECT_DIR, "clips")
OUTPUT_VIDEO = os.path.join(PROJECT_DIR, "leo_sunny_day_60s.mp4")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(CLIPS_DIR, exist_ok=True)

SCENES_DATA = [
    {
        "id": 1,
        "en": "Hello! My name is Leo.",
        "vi": "Xin chào! Tên tớ là Leo.",
        "zoom": "min(zoom+0.0012,1.15)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 2,
        "en": "This is my green backpack.",
        "vi": "Đây là chiếc ba lô màu xanh lá của tớ.",
        "zoom": "min(zoom+0.0010,1.12)",
        "x": "iw/2-(iw/zoom/2)+x*0.0005",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 3,
        "en": "I like walking in the forest.",
        "vi": "Tớ thích đi dạo trong rừng.",
        "zoom": "1.08",
        "x": "x+1.5",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 4,
        "en": "Look! A big red apple!",
        "vi": "Nhìn kìa! Một quả táo đỏ to đùng!",
        "zoom": "min(zoom+0.0015,1.18)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "max(0,ih/2-(ih/zoom/2)-y*0.001)"
    },
    {
        "id": 5,
        "en": "It is round and very red.",
        "vi": "Nó tròn và rất là đỏ.",
        "zoom": "min(zoom+0.0014,1.16)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 6,
        "en": "I have the apple now.",
        "vi": "Giờ tớ có quả táo rồi.",
        "zoom": "min(zoom+0.0010,1.12)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 7,
        "en": "Mmm! It is sweet and yummy.",
        "vi": "Mmm! Nó ngọt và ngon tuyệt cú mèo.",
        "zoom": "min(zoom+0.0015,1.18)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 8,
        "en": "A pretty butterfly is here.",
        "vi": "Một bạn bướm xinh đẹp đang ở đây.",
        "zoom": "min(zoom+0.0012,1.14)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 9,
        "en": "We are good happy friends.",
        "vi": "Chúng tớ là những người bạn tốt vui vẻ.",
        "zoom": "min(zoom+0.0010,1.12)",
        "x": "x-1.0",
        "y": "ih/2-(ih/zoom/2)"
    },
    {
        "id": 10,
        "en": "Goodbye, my friend! See you soon!",
        "vi": "Tạm biệt bạn nhé! Hẹn sớm gặp lại!",
        "zoom": "max(1.0,1.15-on*0.001)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)"
    }
]

print("Script template ready.")
