
from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/marvel-api"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/films")
def show_films():
    response = requests.get(f"{BASE_URL}/movies")
    films = response.json() if response.status_code == 200 else []
    return render_template("films.html", films=films)

@app.route("/films/<int:film_id>")
def film_detail(film_id):
    film_res = requests.get(f"{BASE_URL}/movies/{film_id}")
    character_res = requests.get(f"{BASE_URL}/characters")

    film = film_res.json() if film_res.status_code == 200 else None
    characters = character_res.json() if character_res.status_code == 200 else []

    film_characters = [char for char in characters if film_id in char.get("movie_ids", [])]

    return render_template("film_detail.html", film=film, characters=film_characters)

@app.route("/characters")
def all_characters():
    character_res = requests.get(f"{BASE_URL}/characters")
    planet_res = requests.get(f"{BASE_URL}/planets")

    characters = character_res.json() if character_res.status_code == 200 else []
    planets = planet_res.json() if planet_res.status_code == 200 else []
    planet_map = {p["id"]: p for p in planets}

    for char in characters:
        char["planet"] = planet_map.get(char.get("planet_id"))

    return render_template("characters.html", characters=characters)

@app.route("/characters/<string:role>/")
def character_list_by_role(role):
    role_map = {"heroes": "hero", "villains": "villain"}
    role_value = role_map.get(role)

    if not role_value:
        return "Role not found", 404

    character_res = requests.get(f"{BASE_URL}/characters")
    planet_res = requests.get(f"{BASE_URL}/planets")

    characters = character_res.json() if character_res.status_code == 200 else []
    planets = planet_res.json() if planet_res.status_code == 200 else []
    planet_map = {p["id"]: p for p in planets}

    filtered = [char for char in characters if char["role"] == role_value]
    for char in filtered:
        char["planet"] = planet_map.get(char.get("planet_id"))

    return render_template("characters.html", characters=filtered)

@app.route("/characters/<string:role>/<int:char_id>")
def character_detail(role, char_id):
    role_map = {"heroes": "hero", "villains": "villain"}
    role_value = role_map.get(role)

    if not role_value:
        return "Role not found", 404

    character_res = requests.get(f"{BASE_URL}/characters")
    movie_res = requests.get(f"{BASE_URL}/movies")
    planet_res = requests.get(f"{BASE_URL}/planets")

    characters = character_res.json() if character_res.status_code == 200 else []
    movies = movie_res.json() if movie_res.status_code == 200 else []
    planets = planet_res.json() if planet_res.status_code == 200 else []
    planet_map = {p["id"]: p for p in planets}

    character = next((c for c in characters if c["id"] == char_id and c["role"] == role_value), None)
    if character:
        character["planet"] = planet_map.get(character.get("planet_id"))

    character_movies = [m for m in movies if m["id"] in character.get("movie_ids", [])] if character else []

    return render_template("character_detail.html", character=character, character_movies=character_movies)

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
