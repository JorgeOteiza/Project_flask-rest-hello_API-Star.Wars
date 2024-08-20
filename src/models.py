from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime)
    favorite_characters = db.relationship('FavoriteCharacter', back_populates='user')
    favorite_planets = db.relationship('FavoritePlanet', back_populates='user')
    favorite_vehicles = db.relationship('FavoriteVehicle', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    height = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    favorites = db.relationship('FavoriteCharacter', back_populates='character')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'gender': self.gender,
            'height': self.height,
            'skin_color': self.skin_color,
            'eye_color': self.eye_color,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(50))
    diameter = db.Column(db.String(50))
    population = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    favorites = db.relationship('FavoritePlanet', back_populates='planet')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'diameter': self.diameter,
            'population': self.population,
            'terrain': self.terrain,
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    cost_in_credits = db.Column(db.String(50))
    passengers = db.Column(db.String(50))
    vehicle_class = db.Column(db.String(50))
    favorites = db.relationship('FavoriteVehicle', back_populates='vehicle')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'cost_in_credits': self.cost_in_credits,
            'passengers': self.passengers,
            'vehicle_class': self.vehicle_class,
        }

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    user = db.relationship('User', back_populates='favorite_characters')
    character = db.relationship('Character', back_populates='favorites')

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    user = db.relationship('User', back_populates='favorite_planets')
    planet = db.relationship('Planet', back_populates='favorites')

class FavoriteVehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    user = db.relationship('User', back_populates='favorite_vehicles')
    vehicle = db.relationship('Vehicle', back_populates='favorites')