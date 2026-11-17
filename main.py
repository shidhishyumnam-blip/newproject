
import math
import os
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 24
DURATION = 60
SCENE_LENGTH = 10

def font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/"
        + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    )
    return ImageFont.truetype(path, size)

def story(topic):
    return [
        (f"THE MYSTERY OF {topic.upper()}",
         "Every strange story begins with something unusual."),
        ("SOMETHING WAS WRONG",
         "At first, everything appeared completely normal."),
        ("THE CLUES",
         "But small details started raising serious questions."),
        ("THE BIG QUESTION",
         "Nobody could agree on what had really happened."),
        ("POSSIBLE EXPLANATIONS",
         "Several theories emerged, but evidence was still needed."),
        ("THE STORY CONTINUES",
         "Sometimes the truth is stranger than fiction.")
    ]

def background(draw, scene, time):
    colors = [
        (30, 48, 65), (42, 48, 65), (25, 53, 65),
        (48, 39, 55), (31, 48, 58), (25, 38, 53)
    ]

    draw.rectangle((0, 0, W, H), fill=colors[scene])

    # Distant buildings and structures
    drift = int(time * 12)

    for i in range(10):
        x = (i * 100 - drift) % (W + 100)
        height = 130 + (i * 37 % 180)

        draw.rectangle(
            (x, 800-height, x+65, 800),
            fill=(20, 31, 43)
        )

    # Ground
    draw.polygon(
        [(0, 850), (W, 790), (W, H), (0, H)],
        fill=(34, 39, 44)
    )

def character(draw, x, y, t, scale=1):
    s = scale
    bob = math.sin(t * 3) * 7 * s
    y += bob

    ink = (23, 25, 28)

    # Legs
    movement = math.sin(t * 4) * 15 * s

    draw.line(
        (x-15*s, y+175*s, x-25*s+movement, y+270*s),
        fill=ink, width=int(12*s)
    )

    draw.line(
        (x+15*s, y+175*s, x+25*s-movement, y+270*s),
        fill=ink, width=int(12*s)
    )

    # Body
    draw.rounded_rectangle(
        (x-42*s, y+80*s, x+42*s, y+190*s),
        radius=int(20*s),
        fill=(190, 180, 153),
        outline=ink,
        width=int(5*s)
    )

    # Arms
    wave = math.sin(t * 2.5) * 20 * s

    draw.line(
        (x-40*s, y+105*s, x-75*s, y+145*s+wave),
        fill=ink, width=int(11*s)
    )

    draw.line(
        (x+40*s, y+105*s, x+75*s, y+145*s-wave),
        fill=ink, width=int(11*s)
    )

    # Irregular rounded head
    draw.ellipse(
        (x-57*s, y-15*s, x+57*s, y+90*s),
        fill=(210, 180, 148),
        outline=ink,
        width=int(5*s)
    )

    # Eyes
    draw.ellipse(
        (x-25*s, y+25*s, x-15*s, y+36*s),
        fill=ink
    )
    draw.ellipse(
        (x+15*s, y+25*s, x+25*s, y+36*s),
        fill=ink
    )

    # Mouth
    draw.arc(
        (x-15*s, y+40*s, x+15*s, y+60*s),
        0, 180, fill=ink, width=3
    )

def render(topic, output):
    scenes = story(topic)

    os.makedirs("frames", exist_ok=True)

    title_font = font(38, True)
    caption_font = font(26, True)
    small_font = font(18)

    for frame in range(FPS * DURATION):
        time = frame / FPS
        scene = min(5, int(time // SCENE_LENGTH))

        img = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(img)

        background(d, scene, time)

        x = 360 + math.sin(time * 0.5) * 35
        character(d, x, 580, time, 1.25)

        title, caption = scenes[scene]

        # Cinematic text panels
        d.rectangle((0, 0, W, 190), fill=(10, 17, 25))
        d.rectangle((0, 1040, W, H), fill=(10, 17, 25))

        d.text(
            (40, 35),
            f"CASE FILE / {scene+1:02d}",
            font=small_font,
            fill=(180, 190, 195)
        )

        d.text(
            (40, 85),
            title[:35],
            font=title_font,
            fill=(245, 240, 220)
        )

        d.rounded_rectangle(
            (25, 1080, W-25, 1230),
            radius=18,
            fill=(27, 36, 45)
        )

        d.text(
            (45, 1120),
            caption,
            font=caption_font,
            fill="white"
        )

        progress = int(W * (frame+1) / (FPS*DURATION))
        d.rectangle((0, H-8, progress, H), fill=(210, 185, 140))

        img.save(
            f"frames/{frame:05d}.jpg",
            quality=88
        )

        if frame % 120 == 0:
            print(f"Rendering: {frame}/{FPS*DURATION}")

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", "frames/%05d.jpg",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output
    ], check=True)

    print("VIDEO COMPLETE:", output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output", default="short.mp4")

    args = parser.parse_args()
    render(args.topic, args.output)
      
