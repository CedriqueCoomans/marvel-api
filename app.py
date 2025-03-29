from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/marvel-api"

@app.route("/")
def home():
    return render_template("home.html")


# 🎬 FILMS
@app.route("/films")
def show_films():
    response = requests.get(f"{BASE_URL}/movies")
    films = response.json() if response.status_code == 200 else []
    return render_template("films.html", films=films)

@app.route("/films/<int:film_id>")
def film_detail(film_id):
    response = requests.get(f"{BASE_URL}/movies/{film_id}")
    film = response.json() if response.status_code == 200 else None
    return render_template("film_detail.html", film=film)


# 🦸 CHARACTERS
@app.route("/characters")
def show_characters():
    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=characters, title="Marvel Characters")

@app.route("/characters/<int:char_id>")
def character_detail(char_id):
    response = requests.get(f"{BASE_URL}/characters/{char_id}")
    character = response.json() if response.status_code == 200 else None
    return render_template("character_detail.html", character=character)


# 🪐 PLANETS
@app.route("/planets")
def show_planets():
    response = requests.get(f"{BASE_URL}/planets")
    planets = response.json() if response.status_code == 200 else []
    return render_template("planets.html", planets=planets)

@app.route("/planets/<int:planet_id>")
def planet_detail(planet_id):
    response = requests.get(f"{BASE_URL}/planets/{planet_id}")
    planet = response.json() if response.status_code == 200 else None
    return render_template("planet_detail.html", planet=planet)


if __name__ == "__main__":
    app.run(debug=True)
