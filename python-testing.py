import requests
import scratchattach as sa
from io import BytesIO
from PIL import Image

def rgb_to_hex(rgb):
    r, g, b = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    hex_color = "{:02X}{:02X}{:02X}".format(r, g, b)
    
    return hex_color

def generatePfp(user,resolution):
    userVar = sa.get_user(user)
    req = requests.get(userVar.icon_url).content
    req = BytesIO(req)
    Img = Image.open(req)
    Img = Img.convert("RGB")
    Img = Img.resize((resolution,resolution))
    Img.save("pfp.png")
    pixelList = []
    for pixelX in range(Img.width):
        for pixelY in range(Img.height):
            pixel = Img.getpixel((pixelX, pixelY))
            pixel = rgb_to_hex(pixel)
            pixelList.append(pixel)
    return pixelList

generatePfp("griffpatch",90)