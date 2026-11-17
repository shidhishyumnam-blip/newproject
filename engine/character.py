from PIL import Image, ImageDraw
import math


WIDTH = 320
HEIGHT = 480
SCALE = 3

INK = (35, 31, 30, 255)
SKIN = (235, 190, 153, 255)
SHIRT = (65, 105, 135, 255)


def scaled(value):
    return int(value * SCALE)


def draw_character(path, pose="idle"):
    image = Image.new(
        "RGBA",
        (WIDTH * SCALE, HEIGHT * SCALE),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(image)

    def line(points, fill=INK, width=5):
        points = [(scaled(x), scaled(y)) for x, y in points]
        draw.line(
            points,
            fill=fill,
            width=scaled(width),
            joint="curve"
        )

    def ellipse(box, fill, outline=INK, width=4):
        box = tuple(scaled(v) for v in box)
        draw.ellipse(
            box,
            fill=fill,
            outline=outline,
            width=scaled(width)
        )

    # Legs
    if pose == "walk":
        line([(145, 310), (120, 365), (95, 410)], width=9)
        line([(175, 310), (205, 355), (225, 395)], width=9)
    else:
        line([(145, 310), (140, 365), (135, 420)], width=9)
        line([(175, 310), (180, 365), (185, 420)], width=9)

    # Shoes
    line([(135, 420), (110, 425), (105, 435)], width=9)
    line([(185, 420), (210, 425), (215, 435)], width=9)

    # Arms
    if pose == "point":
        line([(125, 205), (95, 250), (55, 210)], width=9)
        line([(195, 205), (220, 250), (245, 290)], width=9)
    else:
        line([(125, 205), (95, 260), (105, 310)], width=9)
        line([(195, 205), (225, 260), (215, 310)], width=9)

    # Torso
    draw.rounded_rectangle(
        (
            scaled(115), scaled(175),
            scaled(205), scaled(320)
        ),
        radius=scaled(22),
        fill=SHIRT,
        outline=INK,
        width=scaled(4)
    )

    # Neck
    draw.rectangle(
        (
            scaled(145), scaled(145),
            scaled(175), scaled(190)
        ),
        fill=SKIN,
        outline=INK,
        width=scaled(3)
    )

    # Slightly crooked, imperfect rounded head
    head = [
        (112, 65), (120, 42), (145, 30),
        (175, 34), (200, 48), (211, 72),
        (207, 112), (190, 139), (163, 151),
        (135, 141), (113, 119), (105, 91)
    ]

    head = [(scaled(x), scaled(y)) for x, y in head]

    draw.polygon(head, fill=SKIN)
    draw.line(head + [head[0]], fill=INK, width=scaled(4))

    # Eyes
    ellipse((143, 83, 151, 94), INK, INK, 1)
    ellipse((174, 83, 182, 94), INK, INK, 1)

    # Small mouth
    line([(151, 112), (161, 115), (171, 111)], width=2)

    # Downsample for smooth edges
    image = image.resize(
        (WIDTH, HEIGHT),
        Image.Resampling.LANCZOS
    )

    image.save(path)


if __name__ == "__main__":
    draw_character("character_preview.png")
  
