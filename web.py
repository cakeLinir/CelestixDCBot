from flask import Flask, redirect, request, session, jsonify
import os
import requests
from dotenv import load_dotenv

# .env Datei laden
load_dotenv()

RIOT_CLIENT_ID = os.getenv("RIOT_CLIENT_ID")
RIOT_CLIENT_SECRET = os.getenv("RIOT_CLIENT_SECRET")
RIOT_REDIRECT_URI = os.getenv("RIOT_REDIRECT_URI")

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Setze hier eine sichere Secret Key

# Riot OAuth2 URL
RIOT_AUTH_URL = "https://auth.riotgames.com/authorize"
RIOT_TOKEN_URL = "https://auth.riotgames.com/token"


@app.route('/')
def home():
    return '<h2>Valorant Verification</h2><a href="/login">Login mit Riot</a>'


@app.route('/login')
def login():
    riot_auth_link = f"{RIOT_AUTH_URL}?client_id={RIOT_CLIENT_ID}&response_type=code&redirect_uri={RIOT_REDIRECT_URI}&scope=openid"
    return redirect(riot_auth_link)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Fehler: Kein Code erhalten."

    # OAuth2 Token anfordern
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': RIOT_REDIRECT_URI,
        'client_id': RIOT_CLIENT_ID,
        'client_secret': RIOT_CLIENT_SECRET
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(RIOT_TOKEN_URL, data=data, headers=headers)
    token_info = response.json()

    if 'id_token' not in token_info:
        return "Fehler bei der Authentifizierung."

    session['riot_token'] = token_info['id_token']
    return "Login erfolgreich! Du kannst jetzt zum Discord-Bot zurückkehren."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
