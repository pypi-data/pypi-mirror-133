import io
import random
import string
import base64
from .setting import Base
from PIL import Image, ImageDraw, ImageFont

padding_x = 7
colors = ["#9C27B0", "#E91E63", "#F44336", "#2196F3",
          "#3F51B5", "#3F51B5", "#3F51B5", "#00BCD4",
          "#03A9F4", "#CDDC39", "#8BC34A", "#8BC34A",
          "#795548", "#607D8B", "#000000", "#9E9E9E"]


def getColor():
    return colors[int(random.random()*len(colors))]


def getHeight():
    deff = int(Base.image_height-Base.font_size)
    return int(random.random()*deff)


def getWeight():
    return int((Base.image_weight-padding_x)/Base.size)


def randomString(size=6, set_int=True, set_str=True):
    text = ""
    if set_int:
        text += string.digits
    if set_str:
        text += string.ascii_lowercase

    if len(text) == 0:
        text += string.ascii_lowercase

    return ''.join(random.sample(text, size))


def generateImage(text):
    background_color = Base.background_color
    if background_color == "random":
        background_color = "#fff"

    font = ImageFont.truetype('arial.ttf', Base.font_size)
    image = Image.new(
        mode="RGB", size=(Base.image_weight, Base.image_height), color=background_color
    )
    draw = ImageDraw.Draw(image)
    x_position = padding_x
    for item in text:
        text_color = Base.text_color
        if Base.text_color == "random":
            text_color = getColor()
        draw.text((x_position, getHeight()), item, font=font, fill=text_color)
        x_position += getWeight()

    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)
    img_bytes = in_mem_file.read()

    base64_encoded_result_bytes = base64.b64encode(img_bytes)
    base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')

    return "data:image/png;base64,"+base64_encoded_result_str


def getsize(font, text):
    if hasattr(font, 'getoffset'):
        return tuple(
            [x + y for x, y in zip(font.getsize(text), font.getoffset(text))])
    else:
        return font.getsize(text)
