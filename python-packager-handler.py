import scratchattach as sa
from io import BytesIO
from PIL import Image
import requests
from scratchattach import Encoding
import os
sessionID = os.environ.get("scratchSessionID")
connection = sa.CloudConnection(project_id = 683289707, username="ninja_6734_", session_id=sessionID)
CloudEvents = sa.CloudEvents(project_id = 683289707)

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

def sendPackage(package):
    connection.set_var("testing", package)


@CloudEvents.event
def on_set(event):
    out = Encoding.decode(event.value)
    action = out.split(";")
    if action[0] == "pfp":
        send = generatePfp(action[1])
CloudEvents.start()