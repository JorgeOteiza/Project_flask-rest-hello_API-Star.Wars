"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet

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

# Endpoints de Favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    
    favorite = FavoritePlanet(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite added"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    
    favorite = FavoriteCharacter(user_id=user.id, character_id=character.id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite added"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    favorite = FavoritePlanet.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    current_user_id = 1  # Esto debe ser reemplazado por la lógica de autenticación real
    favorite = FavoriteCharacter.query.filter_by(user_id=current_user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Favorite deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
