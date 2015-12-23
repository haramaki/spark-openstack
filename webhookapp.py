# import Flask
from flask import Flask, request
# import  custom-made modules
import sparkmessage
import argparse
import prettytable
import oscontroller

# Create an instance of Flask
app = Flask(__name__)
TOKEN = ""
CON = {}

# Index page will trigger index() function
@app.route('/')
def index():
    return 'Hello World'

# Webhook page will trigger webhooks() function
@app.route("/webhook", methods=['POST'])
def webhooks():

    # Get the json data
    json = request.json
    con = oscontroller.create_connection(CON["url"], "RegionOne", CON["project"], CON["user"], CON["password"])

    # parse the message id, person id, person email, and room id
    message_id = json["data"]["id"]
    person_id = json["data"]["personId"]
    person_email = json["data"]["personEmail"]
    room_id = json["data"]["roomId"]

    # convert the message id into readable text
    message = sparkmessage.get(TOKEN, message_id)
    print(message)

    # create data table
    volume = prettytable.PrettyTable(['name', 'status', 'size'])
    volume.add_row(['volume1', 'OK', '2'])
    volume.add_row(['volume2', 'OK', '4'])

    # check if the message is the command to get hosts
    if message == "Hi":
        sparkmessage.post(TOKEN, person_id, person_email, room_id, "Hi, How are you")
    if message == "server list":
        reply = oscontroller.get_server(con)
        sparkmessage.post(TOKEN, person_id, person_email, room_id, reply)
    if message == "volume list":
        sparkmessage.post(TOKEN, person_id, person_email, room_id, volume.get_string())
    return "OK"

# @app.route("/token", methods=['GET'])
# def gettoken():
#    return TOKEN

# run the application
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
    p.add_argument("-url")
    p.add_argument("-project")
    p.add_argument("-user")
    p.add_argument("-password")
    args = p.parse_args()
    CON = {"url": args.url, "project": args.project, "user": args.user, "password": args.password}
    TOKEN = args.token
    print (TOKEN)
    app.run(host="0.0.0.0", port=8000)
