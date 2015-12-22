# import the requests library so we can use it to make REST calls
import requests
import argparse
import json


# the main function
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
    p.add_argument("-webhook", default="")
    args = p.parse_args()
    # define a variable for the hostname of Spark
    hostname = "api.ciscospark.com"

    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = "Bearer " + args.token

    # add authorization to the header
    header = {"Authorization": "%s" % token}

    # disable warnings about using certificate verification
    requests.packages.urllib3.disable_warnings()

    # create request url
    delete_webhooks_url = "https://" + hostname + "/v1/webhooks"

    # create payroad
    payload = {"webhookId": args.webhook}

    # send GET request and do not verify SSL certificate for simplicity of this example
    api_response = requests.delete(delete_webhooks_url, headers=header, verify=True, params=payload)
    print(api_response.url)

    response_status = api_response.status_code

    # print the status code
    print(response_status)

# run main function
main()
