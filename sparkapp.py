from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = "C691218311f03a9a1b4e69350b96298fbf2b0b5e66678ebd50a3ce3fcfee15730"
CLIENT_SECRET = "14f1d4d866944896ba51c1b20408a361f616ebc8f1a2ba8eea92918bea2008fc"
REDIRECT_URI = "http://38.84.67.164:8080/redirect"

@app.route('/')
def auth_start():
    show_auth = """
<form action="https://api.ciscospark.com/v1/authorize" method="get">
<input type="hidden" name="response_type" value="code" />
<input type="hidden" name="client_id" value="C691218311f03a9a1b4e69350b96298fbf2b0b5e66678ebd50a3ce3fcfee15730" />
<input type="hidden" name="redirect_uri" value="http://38.84.67.164:8080/redirect" />
<input type="hidden" name="scope" value="spark:rooms_read" />
<input type="hidden" name="state" value="test" />
<p><input type="submit" name="submit" value="send" /></p>
</form>
"""
    return show_auth


@app.route('/redirect')
def redirect():
    code = request.args.get('code')
    payload = {'grant_type': 'authorization_code', 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
               'code ': code, 'redirect_uri': REDIRECT_URI}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url="https://api.ciscospark.com/v1/access_token", data=payload, headers=headers)
    json = r.json()
    print json
    return "your access key is " + r.text


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)