from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def auth_start():
    show_auth = """
<form action="https://api.ciscospark.com/v1/authorize" method="post">
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
    return "Welcome to redirect! code is " + code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)