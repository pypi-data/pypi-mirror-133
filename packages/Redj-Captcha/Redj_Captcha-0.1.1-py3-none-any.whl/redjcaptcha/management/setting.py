class Base:
    size = 6
    debug = False
    font_size = 50
    timeout = 6000
    type = "str-int"
    image_height = 70
    image_weight = 180
    text_color= "random"
    background_color= "#fff"


def init(**kwargs):
    for key, value in kwargs.items():
        if key == "timeout":
            Base.timeout = value

        if key == "size" and (value > 2 or value < 10):
            Base.size = value

        if key == "debug" and (value == False or value == True):
            Base.debug = value

        if key == "type" and (value == "int" or value == "str"):
            Base.type = value
