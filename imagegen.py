import datetime
from PIL import Image, ImageDraw, ImageFont

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def generate_image(collection, rank):
    """
        Generates an image displaying the amount of collected
        redstone and the leaderboard rank of the player.
    """

    # Setup
    image = Image.new(mode = "RGB", size=(1200,160), color="black")
    draw = ImageDraw.Draw(image)

    # Fonts
    font_lg = ImageFont.truetype('minecraft.ttf', 56)
    font_sm = ImageFont.truetype('minecraft.ttf', 28)

    # Text segments
    text = [
        ("Redstone:", "#aaaaaa", "#555555"),
        ("_", "#000000", "#000000"),
        (format(collection, ","), "#55ff55", "#005500"),
        ("_", "#000000", "#000000"),
        ("(", "#aaaaaa", "#555555"),
        (f"# {rank}", "#55ffff", "#005555"),
        (")", "#aaaaaa", "#555555"),
    ]

    # Draw each segment of text
    x = 28
    margin = 8
    offset = 7
    for text, color, dark_color in text:
        draw.text((x + offset, 28 + offset), text, fill=dark_color, font=font_lg)
        draw.text((x, 28), text, fill=color, font=font_lg)
        w, h = get_text_dimensions(text, font=font_lg)
        x = x + w + margin

    # Draw the current time, formatted
    lastupdated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).strftime("%B %d, %Y, %I:%M:%S %p EDT").replace(" ", "  ")
    draw.text((28, 108), f"Last Updated:  {lastupdated}", fill="#aaaaaa", font=font_sm)

    return image
