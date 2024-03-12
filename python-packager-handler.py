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

def generatePfp(user):
    userVar = sa.get_user(user)
    req = requests.get(userVar.icon_url).content
    req = BytesIO(req)
    Img = Image.open(req)
    pixelList = []
    for pixelX in Img.width:
        for pixelY in Img.height:
            pixelList.append(Img.getpixel((pixelX, pixelY)))
    return pixelList

def splitToPackages(package):
    if (len(package) <= MaxNumberLimit - 7):
        return [str(random.randint(1,9999999)) + str(package)]
    else:
        packages = []
        for i in range(0,len(package),MaxNumberLimit - 7):
            packages.append(str(random.randint(1,9999999))+str(package)[i:i+MaxNumberLimit-7])
        return packages

def sendPackage(package):
    packages = splitToPackages(package)
    for i in packages:
        connection.set_var("testing",i)
        #be nice :)
        time.sleep(0.5)


@CloudEvents.event
def on_set(event):
    out = Encoding.decode(event.value)
    action = out.split(";")
    if action[0] == "pfp":
        send = generatePfp(action[1])
CloudEvents.start()