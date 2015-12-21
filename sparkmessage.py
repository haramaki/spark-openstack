# import the requests library so we can use it to make REST calls
import requests

# disable warnings about using certificate verification
requests.packages.urllib3.disable_warnings()

# the main function
def post(token, person_id, person_email, room_id, text):
    # define a variable for the hostname of Spark
    hostname = "api.ciscospark.com"

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer " + token

    # add authorization to the header
    header = {"Authorization": "%s" % token, "content-type": "application/json"}

    # specify request url
    post_message_url = "https://" + hostname + "/hydra/api/v1/messages"

    # create message in Spark room
    payload = {
        "personId" : person_id,
        "personEmail" : person_email,
        "roomId" : room_id,
        "text" : text
    }

    # create POST request do not verify SSL certificate for simplicity of this example
    api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)

    # get the response status code
    response_status = api_response.status_code

    # return the text value
    print(response_status)

def get(token, message_id):
        # define a variable for the hostname of Spark
    hostname = "api.ciscospark.com"

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer "+token

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

