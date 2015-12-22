# import Flask
from flask import Flask, request
# import  custom-made modules
import sparkmessage
import argparse
import prettytable

# Create an instance of Flask
app = Flask(__name__)
TOKEN = ""

# Index page will trigger index() function
@app.route('/')
def index():
    return 'Hello World'

# Webhook page will trigger webhooks() function
@app.route("/webhook", methods=['POST'])
def webhooks():

    # Get the json data
    json = request.json

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
    print(volume)

    server = prettytable.PrettyTable(['name', 'status', 'flavor', 'networks'])
    server.add_row(['vm1', 'OK', 'm1.small', 'net01'])
    server.add_row(['vm2', 'OK', 'm1.large', 'net02'])

    # check if the message is the command to get hosts
    if message == "Hi":
        sparkmessage.post(TOKEN, person_id, person_email, room_id, "Hi, How are you")
    if message == "server list":
        sparkmessage.post(TOKEN, person_id, person_email, room_id, server)
    if message == "volume list":
        sparkmessage.post(TOKEN, person_id, person_email, room_id, volume)

#    if message == "GET HOSTS":
#        # get list of hosts from APIC-EM Controller
#        hosts = gethosts.main()
#        # post the list of hosts into the Spark room
#        sparkmessage.post(person_id, person_email, room_id, hosts)
    else:
        print("do nothing")

#@app.route("/token", methods=['GET'])
#def gettoken():
#    return TOKEN

# run the application
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
    args = p.parse_args()
    TOKEN = args.token
    print (TOKEN)
    app.run(host="0.0.0.0", port=8000)
