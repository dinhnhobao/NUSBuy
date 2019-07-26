from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def redirect():
    url = "https://openid.nus.edu.sg/server/"
    url += "?openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select"
    url += "&openid.identity=http://specs.openid.net/auth/2.0/identifier_select"
    url += "&openid.mode=checkid_setup"
    url += "&openid.ns=http://specs.openid.net/auth/2.0"
    url += "&openid.sreg.required=email,nickname,fullname"
    url += "&openid.identity=http://specs.openid.net/auth/2.0/identifier_select"
    url += "&openid.return_to=http://localhost:5000/callback"
    print("url: ", url)
    return "<a href={}>NUS OpenID</a>".format(url)

@app.route("/callback")
def callback():
    email = request.args.get("openid.sreg.email")
    fullname = request.args.get("openid.sreg.fullname")
    nickname = request.args.get("openid.sreg.nickname")
    reply = "email:{}, fullname:{}, nickname{}. ".format(email, fullname, nickname)
    if authenticate(request.args):
        reply += "This user is valid."
    else:
        reply += "This user is invalid."
    print("request.args: ", request.args)
    return reply

def authenticate(args):
    params = request.args.copy()
    params["openid.mode"] = "check_authentication"
    response = requests.get(url = "https://openid.nus.edu.sg/server/", params = params)
    body = response.content.decode("utf-8")
    print("body: ", body)
    return "is_valid:true" in body
