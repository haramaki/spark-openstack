# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request
import argparse
import oscontroller
from sparkmessage import SparkController

# Create an instance of Flask
app = Flask(__name__)
TOKEN = ""
CON = {}
HELP = """
+----------
server list           list active servers
server show <name>    show server
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
    os = oscontroller.OSController(CON["url"], "RegionOne", CON["project"], CON["user"], CON["password"])
    sc = SparkController(os, json, TOKEN)
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
