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
HELP = """
+----------
server list           list active servers
server create <name>  create server
server delete <name>  delete server
flavor list           list flavors
image  list           list image
volume list           list volumes
+----------
"""


# Index page will trigger index() function
@app.route('/')
def index():
    return 'Hello World'


# Webhook page will trigger webhooks() function
@app.route("/webhook", methods=['POST'])
def webhooks():
    # Get the json data
    json = request.json

    # convert the message id into readable text
    sc = SparkController(CON["url"], "RegionOne", CON["project"], CON["user"], CON["password"], json, TOKEN)
    message = sc.get_message()

    # check if the message is the command to get hosts
    com_list = message.split()
    operator = com_list[0]

    if operator == "Hi":
        sc.send_message("How are you")
    elif operator == "help":
        sc.send_message(HELP)
    elif operator == "server":
        sc.server_control(com_list)
    elif operator == "volume":
        sc.volume_control(com_list)
    elif operator == "image":
        sc.image_control(com_list)
    elif operator == "flavor":
        sc.flavor_control(com_list)
    
    return "OK"


class SparkController:
    def __init__(self, url, region, project, user, password, json, token):
        self.con = oscontroller.create_connection(url, region, project, user, password)
        self.token = token
        self.json = json

    def get_message(self):
        message_id = self.json["data"]["id"]
        return sparkmessage.get(self.token, message_id)

    def send_message(self, msg):
        person_id = self.json["data"]["personId"]
        person_email = self.json["data"]["personEmail"]
        room_id = self.json["data"]["roomId"]
        sparkmessage.post(self.token, person_id, person_email, room_id, msg)

    def server_control(self, com_list):
        if len(com_list) == 1:
            self.send_message("Please add list or create or delete")
        elif com_list[1] == "list":
            reply_msg = oscontroller.get_server(self.con)
            self.send_message(reply_msg)
        elif com_list[1] == "create":
            if len(com_list) == 2:
                self.send_message("Please add vm name")
            else:
                oscontroller.create_server(self.con, com_list[2])
                self.send_message("Server "+com_list[2]+" is created")
        elif com_list[1] == "delete":
            if len(com_list) == 2:
                self.send_message("Please add vm name")
            else:
                oscontroller.delete_server(self.con, com_list[2])
                self.send_message("Server "+com_list[2]+" is deleted")

    def volume_control(self, com_list):
        if len(com_list) == 1:
            self.send_message("Please add list")
        elif com_list[1] == "list":
            volume = prettytable.PrettyTable(['name', 'status', 'size'])
            volume.add_row(['volume1', 'OK', '2'])
            volume.add_row(['volume2', 'OK', '4'])
            self.send_message(volume.get_string())

    def image_control(self, com_list):
        if len(com_list) == 1:
            self.send_message("Please add list")
        elif com_list[1] == "list":
            reply_msg = oscontroller.get_image(self.con)
            self.send_message(reply_msg)

    def flavor_control(self, com_list):
        if len(com_list) == 1:
            self.send_message("Please add list")
        elif com_list[1] == "list":
            reply_msg = oscontroller.get_flavor(self.con)
            self.send_message(reply_msg)


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

