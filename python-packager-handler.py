import scratchattach as sa
import os
sessionID = os.environ.get("scratchSessionID")
connection = sa.CloudConnection(project_id = 683289707, username="ninja_6734_", session_id=sessionID)
CloudEvents = sa.CloudEvents(project_id = 683289707)

@CloudEvents.event
def on_set(event):
    print(f"{event.user} set the variable {event.var} to the value {event.value} at {event.timestamp}")

CloudEvents.start()