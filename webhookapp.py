# import Flask
from flask import Flask, request
# import  custom-made modules
import sparkmessage

# Create an instance of Flask
app = Flask(__name__)

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
    message = sparkmessage.get(message_id)
    print(message)

    # check if the message is the command to get hosts
    if message == "Hi"
        sparkmessage.post(person_id, person_email, room_id, "Hi")
#    if message == "GET HOSTS":
#        # get list of hosts from APIC-EM Controller
#        hosts = gethosts.main()
#        # post the list of hosts into the Spark room
#        sparkmessage.post(person_id, person_email, room_id, hosts)
    else:
       print("do nothing")

# run the application
if __name__ == "__main__":
    app.run()
