import requests
from flask import jsonify, url_for

class APIException(Exception):
    status_code = 500

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            "message": self.message,
            "status_code": self.status_code
        }

def generate_sitemap(app):
    try:
        links = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append(url)
        return jsonify(links)
    except Exception as e:
        raise APIException(f"Error generating sitemap: {str(e)}", 500)

def get_swapi_data(endpoint):
    base_url = "https://swapi.dev/api"
    try:
        response = requests.get(f"{base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APIException(f"Error fetching data from SWAPI: {str(e)}", 502)

# Función para validar ID desde SWAPI
def validate_swapi_id(entity_type, entity_id):
    response = requests.get(f"https://swapi.dev/api/{entity_type}/{entity_id}/")
    return response.status_code == 200
