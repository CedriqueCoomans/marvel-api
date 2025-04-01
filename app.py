from flask import Flask, render_template  # Webframework en HTML rendering
import requests  # Voor het ophalen van data via API

app = Flask(__name__)  # Start een nieuwe Flask-applicatie

# Basis URL van de JSON API
BASE_URL = "https://my-json-server.typicode.com/CedriqueCoomans/marvel-api"

# Homepage
@app.route("/")
def home():
    return render_template("home.html")

# Overzicht van alle films
@app.route("/films")
def show_films():
    response = requests.get(f"{BASE_URL}/movies")
    films = response.json() if response.status_code == 200 else []
    return render_template("films.html", films=films)

# Detailpagina van een specifieke film
@app.route("/films/<int:film_id>")
def film_detail(film_id):
    film_res = requests.get(f"{BASE_URL}/movies/{film_id}")
    character_res = requests.get(f"{BASE_URL}/characters")

    film = film_res.json() if film_res.status_code == 200 else None
    characters = character_res.json() if character_res.status_code == 200 else []

    # Filter personages die in deze film voorkomen
    film_characters = [
        char for char in characters if film_id in char.get("movie_ids", [])
    ]

    return render_template("film_detail.html", film=film, characters=film_characters)

# Toon alle personages
@app.route("/characters")
def all_characters():
    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []
    return render_template("characters.html", characters=characters)

# Toon lijst van helden of schurken
@app.route("/characters/<string:role>/")
def character_list_by_role(role):
    role_map = {"heroes": "hero", "villains": "villain"}
    role_value = role_map.get(role)

    if not role_value:
        return "Role not found", 404

    response = requests.get(f"{BASE_URL}/characters")
    characters = response.json() if response.status_code == 200 else []

    filtered = [char for char in characters if char["role"] == role_value]

    return render_template("characters.html", characters=filtered)

# Detailpagina van een specifiek personage (held of schurk)
@app.route("/characters/<string:role>/<int:char_id>")
def character_detail(role, char_id):
    role_map = {"heroes": "hero", "villains": "villain"}
    role_value = role_map.get(role)

    if not role_value:
        return "Role not found", 404

    character_res = requests.get(f"{BASE_URL}/characters")
    movie_res = requests.get(f"{BASE_URL}/movies")

    characters = character_res.json() if character_res.status_code == 200 else []
    movies = movie_res.json() if movie_res.status_code == 200 else []

    # Zoek het personage op
    character = next((c for c in characters if c["id"] == char_id and c["role"] == role_value), None)

    # Zoek films waarin het personage voorkomt
    character_movies = [m for m in movies if m["id"] in character.get("movie_ids", [])] if character else []

    return render_template("character_detail.html", character=character, character_movies=character_movies)

# Overzicht van alle planeten
@app.route("/planets")
def show_planets():
    response = requests.get(f"{BASE_URL}/planets")
    planets = response.json() if response.status_code == 200 else []
    return render_template("planets.html", planets=planets)

# Detailpagina van een specifieke planeet
@app.route("/planets/<int:planet_id>")
def planet_detail(planet_id):
    response = requests.get(f"{BASE_URL}/planets/{planet_id}")
    planet = response.json() if response.status_code == 200 else None
    return render_template("planet_detail.html", planet=planet)

# Start de Flask server
if __name__ == "__main__":
    app.run(debug=True)
