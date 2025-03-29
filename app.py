from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/marvel-api"

@app.route("/")
def home():
    return render_template("home.html")


# FILMS
@app.route("/films")
def show_films():
    response = requests.get(f"{BASE_URL}/movies")
    films = response.json() if response.status_code == 200 else []
    return render_template("films.html", films=films)

@app.route("/films/<int:film_id>")
def film_detail(film_id):
    film_res = requests.get(f"{BASE_URL}/movies/{film_id}")
    char_res = requests.get(f"{BASE_URL}/characters")

    film = film_res.json() if film_res.status_code == 200 else None
    characters = char_res.json() if char_res.status_code == 200 else []

    film_characters = [char for char in characters if char["film_id"] == film_id]

    return render_template("film_detail.html", film=film, characters=film_characters)



# CHARACTERS
@app.route("/characters")
def all_characters():
    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=characters)


@app.route("/characters/<string:type>s/<int:char_id>")
def character_detail(type, char_id):
    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []
    character = next((char for char in characters if char["id"] == char_id and char["role"] == type), None)
    return render_template("character_detail.html", character=character)



# PLANETS
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
