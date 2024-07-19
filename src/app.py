"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from API.admin import setup_admin
from API.models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup database
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints de Characters
@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    result = [person.serialize() for person in people]
    return jsonify(result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(person.serialize()), 200

# Endpoints de Planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = [planet.serialize() for planet in planets]
    return jsonify(result), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# Endpoints de Users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [user.serialize() for user in users]
    return jsonify(result), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    favorite_characters = [fav.character.serialize() for fav in user.favorite_characters]
    favorite_planets = [fav.planet.serialize() for fav in user.favorite_planets]

    return jsonify({
        "favorite_characters": favorite_characters,
        "favorite_planets": favorite_planets
    }), 200

# Función para validar ID desde SWAPI
def validate_swapi_id(entity_type, entity_id):
    response = requests.get(f"https://swapi.dev/api/{entity_type}/{entity_id}/")
    return response.status_code == 200

# Endpoints de Favoritos
@app.route('/favorite/people', methods=['POST'])
def add_favorite_character():
    data = request.get_json()
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    
    character_id = data.get('character_id')
    if not character_id or not validate_swapi_id('people', character_id):
        return jsonify({"msg": "Character not found in SWAPI"}), 404

    favorite = FavoriteCharacter(user_id=current_user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite character added"}), 201

@app.route('/favorite/planet', methods=['POST'])
def add_favorite_planet():
    data = request.get_json()
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    
    planet_id = data.get('planet_id')
    if not planet_id or not validate_swapi_id('planets', planet_id):
        return jsonify({"msg": "Planet not found in SWAPI"}), 404

    favorite = FavoritePlanet(user_id=current_user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite planet added"}), 201

@app.route('/favorite/people/<int:favorite_id>', methods=['PUT'])
def update_favorite_character(favorite_id):
    data = request.get_json()
    favorite = FavoriteCharacter.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    character_id = data.get('character_id')
    if character_id and validate_swapi_id('people', character_id):
        favorite.character_id = character_id
    
    db.session.commit()
    return jsonify({"msg": "Favorite character updated"}), 200

@app.route('/favorite/planet/<int:favorite_id>', methods=['PUT'])
def update_favorite_planet(favorite_id):
    data = request.get_json()
    favorite = FavoritePlanet.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    planet_id = data.get('planet_id')
    if planet_id and validate_swapi_id('planets', planet_id):
        favorite.planet_id = planet_id
    
    db.session.commit()
    return jsonify({"msg": "Favorite planet updated"}), 200

@app.route('/favorite/people/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_character(favorite_id):
    favorite = FavoriteCharacter.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character deleted"}), 200

@app.route('/favorite/planet/<int:favorite_id>', methods=['DELETE'])
def delete_favorite_planet(favorite_id):
    favorite = FavoritePlanet.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
