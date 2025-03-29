from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/Json-Api-webserver"

@app.route("/")
def home():
    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=characters)

@app.route("/characters/<int:char_id>")
def character_detail(char_id):
    response = requests.get(f"{BASE_URL}/characters/{char_id}")
    character = response.json() if response.status_code == 200 else None
    return render_template("character_detail.html", character=character)

if __name__ == "__main__":
    app.run(debug=True)
