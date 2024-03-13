import scratchattach as sa
from io import BytesIO
from PIL import Image
import requests
from scratchattach import Encoding
import os
import random
import time
sessionID = os.environ.get("scratchSessionID")
connection = sa.CloudConnection(project_id = 683289707, username="ninja_6734_", session_id=sessionID)
CloudEvents = sa.CloudEvents(project_id = 683289707)

MaxNumberLimit = 256

def rgb_to_hex(rgb):
    r, g, b = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    hex_color = "{:02X}{:02X}{:02X}".format(r, g, b)
    
    return hex_color

def generatePfp(user):
    userVar = sa.get_user(user)
    req = requests.get(userVar.icon_url).content
    req = BytesIO(req)
    Img = Image.open(req)
    Img = Img.convert("RGB")
    Img.resize((15,15))
    pixelList = []
    for pixelX in range(Img.width):
        for pixelY in range(Img.height):
            pixel = Img.getpixel((pixelX, pixelY))
            pixel = rgb_to_hex(pixel)
            pixelList.append(pixel)
    return pixelList

def splitToPackages(package):
    if (len(package) <= MaxNumberLimit - 8):
        return [str(random.randint(1,99999999)).zfill(8) + str(package)]
    else:
        packages = []
        for i in range(0,len(package),MaxNumberLimit - 8):
            packages.append(str(random.randint(1,99999999)).zfill(8)+str(package)[i:i+MaxNumberLimit-8])
        return packages

def sendPackage(package):
    packages = splitToPackages(Encoding.encode(package))
    for i in packages:
        connection.set_var("testing",i)
        print("sent package: "+ Encoding.decode(i[8:]))
        #be nice :)
        time.sleep(0.2)
    connection.set_var("testing",str(random.randint(1,99999999)).zfill(8)+str(Encoding.encode("end")))
    print("sent package ending")


@CloudEvents.event
def on_set(event):
    out = Encoding.decode(event.value)
    action = out.split(";")
    if action[0] == "pfp":
        send = ""
        for color in generatePfp(action[1]):
            send += color
        sendPackage(send)

@CloudEvents.event
def on_ready():
    print("listener ready!")

CloudEvents.start()