import requests
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
    p.add_argument("-room")
    p.add_argument("-text")
    args = p.parse_args()

    # define a variable for the hostname of Spark
    hostname = "api.ciscospark.com"

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer " + args.token

    # add authorization to the header
    header = {"Authorization": "%s" % token, "content-type": "application/json"}

    # specify request url
    post_message_url = "https://" + hostname + "/hydra/api/v1/messages"

    # create message in Spark room
    payload = {
        "roomId": args.room,
        "text": args.text
    }

    # create POST request do not verify SSL certificate for simplicity of this example
    api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)

    # get the response status code
    response_status = api_response.status_code

    # return the text value
    print(response_status)

if __name__ == '__main__':
    main()