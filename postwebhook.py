# import the requests and json library so we can use it to make REST calls
import requests
import argparse

# the main function
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
    p.add_argument("-url", default="")
    p.add_argument("-room", default="")
    args = p.parse_args()

    # define a variable for the hostname of Spark
    hostname = "api.ciscospark.com"

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer " + args.token

    # add authorization to the header
    header = {"Authorization": "%s" % token, "content-type": "application/json"}

    # disable warnings about using certificate verification
    requests.packages.urllib3.disable_warnings()

    # create request url
    post_message_url = "https://" + hostname + "/v1/webhooks"

    # create request body
    payload = {
        "resource": "messages",
        "event": "created",
        "filter": "roomId="+args.room,
        "targetUrl": args.url,
        "name": "bot"
    }

    # send the POST request resource and do not verify SSL certificate for simplicity of this example
    api_response = requests.post(post_message_url, json=payload, headers=header, verify=False)

    # get the response status code
    response_status = api_response.status_code

    # print the status code
    print(response_status)


# run the function
main()
