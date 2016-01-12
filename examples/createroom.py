# import the requests library so we can use it to make REST calls
import requests
import argparse


# the main function
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-token", required=True)
    p.add_argument("-title", required=True)
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
    post_room_url = "https://" + hostname + "/v1/rooms"

    payload = {"title": args.title}

    # send the POST request resource and do not verify SSL certificate for simplicity of this example
    api_response = requests.post(post_room_url, json=payload, headers=header, verify=False)

    # parse the response in json
    response_json = api_response.json()

    # print the response
    print(response_json)


# run main function
if __name__ == '__main__':
    main()
