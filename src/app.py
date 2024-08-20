import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .utils import APIException, generate_sitemap, validate_swapi_id
from .admin import setup_admin
from .models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoritePlanet, FavoriteVehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup database
db_url = os.getenv("DATABASE_URL")
if db_url:
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
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
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

# Endpoints de Vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    result = [vehicle.serialize() for vehicle in vehicles]
    return jsonify(result), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

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
    favorite_vehicles = [fav.vehicle.serialize() for fav in user.favorite_vehicles]

    return jsonify({
        "favorite_characters": favorite_characters,
        "favorite_planets": favorite_planets,
        "favorite_vehicles": favorite_vehicles
    }), 200

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

@app.route('/favorite/vehicle', methods=['POST'])
def add_favorite_vehicle():
    data = request.get_json()
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    
    vehicle_id = data.get('vehicle_id')
    if not vehicle_id or not validate_swapi_id('vehicles', vehicle_id):
        return jsonify({"msg": "Vehicle not found in SWAPI"}), 404

    favorite = FavoriteVehicle(user_id=current_user_id, vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite vehicle added"}), 201

# Endpoints para eliminar favoritos
@app.route('/favorite/people/<int:favorite_id>', methods=['DELETE'])
def remove_favorite_character(favorite_id):
    favorite = FavoriteCharacter.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite character not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite character removed"}), 200

@app.route('/favorite/planet/<int:favorite_id>', methods=['DELETE'])
def remove_favorite_planet(favorite_id):
    favorite = FavoritePlanet.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite planet removed"}), 200

@app.route('/favorite/vehicle/<int:favorite_id>', methods=['DELETE'])
def remove_favorite_vehicle(favorite_id):
    favorite = FavoriteVehicle.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite vehicle not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite vehicle removed"}), 200

# This only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", 8080), debug=True)
