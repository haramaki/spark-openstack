# import the requests library so we can use it to make REST calls
import requests
import argparse
import json


# the main function
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-token", default="")
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
    get_webhooks_url = "https://" + hostname + "/v1/webhooks"

    # send GET request and do not verify SSL certificate for simplicity of this example
    api_response = requests.get(get_webhooks_url, headers=header, verify=True)

    # parse the response in json
    response_json = api_response.json()

    # print the response
    print(json.dumps(response_json ,sort_keys=True, indent=4))

# run main function
if __name__ == '__main__':
    main()
