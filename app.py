from flask import Flask, jsonify, request, make_response
import requests
import os
from flasgger import swag_from
from dotenv import load_dotenv
from swagger.config import init_swagger


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MICROSERVICES:
MICROSERVICES = {
    "abonnement": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5002"),
    "user": os.getenv("LOGIN_MICROSERVICE_URL", "http://localhost:5005"),
}

# Initialize Swagger
init_swagger(app)

# ----------------------------------------------------- GET /subscriptions
@app.route('/subscriptions', methods=['GET']) 
def get_subscriptions(): 
    response = requests.get(f"{MICROSERVICES['abonnement']}/subscriptions") 
    if response.status_code == 200: 
        return jsonify(response.json()), 200 
    else: 
        data = response.json
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /subscriptions/total-price
@app.route('/subscriptions/total-price', methods=['GET'])
def get_total_price():
    response = requests.get(f"{MICROSERVICES['abonnement']}/subscriptions/total-price")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /damage-reports
@app.route('/damage-reports', methods=['GET'])
def get_damage_reports():
    response = requests.get(f"{MICROSERVICES['abonnement']}/damage-reports") # TODO update microservice
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /damage-types 
@app.route('/damage-types', methods=['GET'])
def get_damage_types():
    response = requests.get(f"{MICROSERVICES['abonnement']}/damage-types") # TODO update microservice
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /cars/<id>/damage-costs
@app.route('/cars/<id>/damage-costs', methods=['GET'])
def get_damage_costs(id):
    response = requests.get(f"{MICROSERVICES['abonnement']}/cars/{id}/damage-costs") # TODO update microservice
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /damage-reports/subscriptions/<subscriptionId>/total-damage
@app.route('/damage-reports/subscriptions/<subscriptionId>/total-damage', methods=['GET'])
def get_total_damage(subscriptionId):
    response = requests.get(f"{MICROSERVICES['abonnement']}/damage-reports/subscriptions/{subscriptionId}/total-damage") # TODO update microservice
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- POST /login
@app.route('/login', methods=['POST'])
def login():
    response = requests.post(f"{MICROSERVICES['user']}/login")
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        data = response.json()
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ----------------------------------------------------- Catch-all route for unmatched endpoints 
@app.errorhandler(404)
def page_not_found_404(e):
    return jsonify({"message": "Endpoint does not exist"})

@app.errorhandler(405)
def page_not_found_405(e):
    return jsonify({"message": "Method not allowed - double check the method you are using"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
