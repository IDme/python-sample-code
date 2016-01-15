import os
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Get this information by registering your app at https://developer.id.me
client_id              = 'YOUR_CLIENT_ID'
client_secret          = 'YOUR_CLIENT_SECRET'
redirect_uri           = 'YOUR_REDIRECT_URI'
authorization_base_url = 'https://api.id.me/oauth/authorize'
token_url              = 'https://api.id.me/oauth/token'
attributes_url         = 'https://api.id.me/api/public/v2/attributes.json'

# possible scope values: "military", "student", "responder", "government", "teacher"
scope = ['YOUR_SCOPE_VALUE']

@app.route("/")

def demo():
    return render_template('index.html')


@app.route("/callback", methods=["GET"])
def callback():
    # Exchange your code for an access token
    idme  = OAuth2Session(client_id, redirect_uri=redirect_uri)
    token = idme.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    # At this point you can fetch a user's attributes but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    # Fetching the user's attributes using an OAuth 2 token.
    idme = OAuth2Session(client_id, token=session['oauth_token'])
    payload = idme.get(attributes_url).json()

    session['profile'] = true
    return jsonify(payload)


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.secret_key = os.urandom(24)
    app.run(debug=True)
