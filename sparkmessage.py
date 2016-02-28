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

import requests
import prettytable

requests.packages.urllib3.disable_warnings()

class SparkController:
    def __init__(self, os, json, token):
        self.os = os
        self.token = token
        self.json = json

    def get_message(self):
        message_id = self.json["data"]["id"]
        return self.get(message_id)

    def send_message(self, msg):
        person_id = self.json["data"]["personId"]
        person_email = self.json["data"]["personEmail"]
        room_id = self.json["data"]["roomId"]
        self.post(person_id, person_email, room_id, msg)

    def server_control(self, com_list):
        operator = com_list[1]
        if len(com_list) == 1:
            self.send_message("Please add list or create or delete")
        elif operator == "list":
            reply_msg = self.os.list_server()
            self.send_message(reply_msg)
        elif operator == "show":
            if len(com_list) == 2:
                self.send_message("Please add vm name")
            else:
                reply_msg = self.os.show_server(com_list[2])
                self.send_message(reply_msg)
        elif operator == "create":
            if len(com_list) == 2:
                self.send_message("Please add vm name")
            else:
                self.os.create_server(com_list[2])
                self.send_message("Server "+com_list[2]+" is created")
        elif operator == "delete":
            if len(com_list) == 2:
                self.send_message("Please add vm name")
            else:
                self.os.delete_server(com_list[2])
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
            reply_msg = self.os.get_image()
            self.send_message(reply_msg)

    def flavor_control(self, com_list):
        if len(com_list) == 1:
            self.send_message("Please add list")
        elif com_list[1] == "list":
            reply_msg = self.os.get_flavor()
            self.send_message(reply_msg)

    def post(self, person_id, person_email, room_id, text):
        # define a variable for the hostname of Spark
        hostname = "api.ciscospark.com"
        token = "Bearer " + self.token
        # add authorization to the header
        header = {"Authorization": "%s" % token, "content-type": "application/json"}

        # specify request url
        post_message_url = "https://" + hostname + "/hydra/api/v1/messages"

        # create message in Spark room
        payload = {
            "personId": person_id,
            "personEmail": person_email,
            "roomId": room_id,
            "text": text
        }

        # create POST request do not verify SSL certificate for simplicity of this example
        api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)

        # get the response status code
        response_status = api_response.status_code

        # return the text value
        print(response_status)

    def get(self, message_id):
        # define a variable for the hostname of Spark
        hostname = "api.ciscospark.com"

        # login to developer.ciscospark.com and copy your access token here
        # Never hard-code access token in production environment
        token = "Bearer "+self.token

        # add authorization to the header
        header = {"Authorization": "%s" % token}

        # create request url using message ID
        get_rooms_url = "https://" + hostname + "/v1/messages/" + message_id

        # send the GET request and do not verify SSL certificate for simplicity of this example
        api_response = requests.get(get_rooms_url, headers=header, verify=False)

        # parse the response in json
        response_json = api_response.json()

        # get the text value from the response
        text = response_json["text"]

        # return the text value
        return text
