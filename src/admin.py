import os
from flask_admin import Admin
from .models import db, User, Character, Planet, Vehicle, FavoriteCharacter, FavoriteVehicle, FavoritePlanet
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(Vehicle, db.session))
    admin.add_view(ModelView(FavoriteCharacter, db.session))
    admin.add_view(ModelView(FavoritePlanet, db.session))
    admin.add_view(ModelView(FavoriteVehicle, db.session))

