from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/marvel-api"

@app.route("/")
def home():
    response = requests.get(f"{BASE_URL}/films")
    films = response.json() if response.status_code == 200 else []
    return render_template("films.html", films=films)

@app.route("/heroes")
def show_heroes():
    response = requests.get(f"{BASE_URL}/heroes")
    heroes = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=heroes, title="Marvel Helden", type="hero")

@app.route("/villains")
def show_villains():
    response = requests.get(f"{BASE_URL}/villains")
    villains = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=villains, title="Marvel Schurken", type="villain")

@app.route("/planets")
def show_planets():
    response = requests.get(f"{BASE_URL}/planets")
    planets = response.json() if response.status_code == 200 else []
    return render_template("planets.html", planets=planets)

# 🎯 Detailpagina per held/schurk
@app.route("/characters/<string:type>/<int:char_id>")
def character_detail(type, char_id):
    response = requests.get(f"{BASE_URL}/{type}s/{char_id}")
    character = response.json() if response.status_code == 200 else None
    return render_template("character_detail.html", character=character)

# 🌍 Detailpagina voor planeten
@app.route("/planets/<int:planet_id>")
def planet_detail(planet_id):
    response = requests.get(f"{BASE_URL}/planets/{planet_id}")
    planet = response.json() if response.status_code == 200 else None
    return render_template("planet_detail.html", planet=planet)

# 🎬 Detailpagina voor films
@app.route("/films/<int:film_id>")
def film_detail(film_id):
    response = requests.get(f"{BASE_URL}/films/{film_id}")
    film = response.json() if response.status_code == 200 else None
    return render_template("film_detail.html", film=film)

if __name__ == "__main__":
    app.run(debug=True)
