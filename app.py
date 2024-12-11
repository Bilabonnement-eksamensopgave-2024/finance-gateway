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
    "user": os.getenv("USER_MICROSERVICE_URL", "http://localhost:5005"),
    "subscription": os.getenv("ABONNEMENT_MICROSERVICE_URL", "http://localhost:5006"),
    "damage": os.getenv("SKADE_MICROSERVICE_URL", "http://localhost:5007"),
}

# Initialize Swagger
init_swagger(app)

# ----------------------------------------------------- GET /
# Root endpoint with gateway documentation
@app.route('/', methods=['GET'])
def service_info():
    return jsonify({
        "service": "Finance Gateway",
        "description": "This gateway handles financial operations including subscriptions, pricing, and damage cost summaries.",
        "endpoints": [
            {
                "path": "/subscriptions",
                "method": "GET",
                "description": "Get all subscriptions",
                "response": "JSON array of subscription objects",
                "role_required": "admin, finance"
            },
            {
                "path": "/subscriptions/current/total-price",
                "method": "GET",
                "description": "Get the total price of current subscriptions",
                "response": "JSON object with total price",
                "role_required": "admin, finance"
            },
            {
                "path": "/damage-reports",
                "method": "GET",
                "description": "Get all damage reports",
                "response": "JSON array of damage report objects",
                "role_required": "admin, finance"
            },
            {
                "path": "/damage-types",
                "method": "GET",
                "description": "Get all damage types",
                "response": "JSON array of damage type objects",
                "role_required": "admin, finance"
            },
            {
                "path": "/cars/<id>/damage-costs",
                "method": "GET",
                "description": "Get damage costs for a specific car by ID",
                "response": "JSON object with damage costs",
                "role_required": "admin, finance"
            },
            {
                "path": "/damage-reports/subscriptions/<subscriptionId>/total-damage",
                "method": "GET",
                "description": "Get total damage costs for a specific subscription by ID",
                "response": "JSON object with total damage costs",
                "role_required": "admin, finance"
            },
            {
                "path": "/login",
                "method": "POST",
                "description": "Authenticate a user and return a token",
                "response": "JSON object with token or error message",
                "role_required": "none"
            }
        ]
    })

# ----------------------------------------------------- GET /subscriptions
@app.route('/subscriptions', methods=['GET'])
@swag_from('swagger/get_subscriptions.yaml')
def get_subscriptions():
    response = requests.get(
        url=f"{MICROSERVICES['subscription']}/subscriptions", 
        cookies=request.cookies
        )
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /subscriptions/current/total-price
@app.route('/subscriptions/current/total-price', methods=['GET'])
@swag_from('swagger/get_current_subscriptions_total_price.yaml')
def get_total_price():
    response = requests.get(f"{MICROSERVICES['subscription']}/subscriptions/current/total-price",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /damage-reports
@app.route('/damage-reports', methods=['GET'])
@swag_from('swagger/get_all_damage_reports.yaml')
def get_damage_reports():
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /damage-types 
@app.route('/damage-types', methods=['GET'])
@swag_from('swagger/get_damage_types.yaml')
def get_damage_types():
    response = requests.get(f"{MICROSERVICES['damage']}/damage-types",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /cars/<id>/total-cost
@app.route('/cars/<int:id>/total-cost', methods=['GET'])
#@swag_from('swagger/get_subscriptions.yaml') # TODO
def get_damage_costs(id):
    response = requests.get(f"{MICROSERVICES['damage']}/cars/{id}/total-cost",cookies=request.cookies)
    try: 
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- GET /subscriptions/<subscriptionId>/total-cost
@app.route('/subscriptions/<subscriptionId>/total-cost', methods=['GET'])
@swag_from('swagger/get_total_cost_by_subscriptionid.yaml')
def get_total_damage(subscriptionId):
    response = requests.get(f"{MICROSERVICES['damage']}/damage-reports/subscriptions/{subscriptionId}/total-cost",cookies=request.cookies)
    try:
        data = response.json() 
    except requests.exceptions.JSONDecodeError: 
        data = []

    if response.status_code in [200, 201, 204]:
        return jsonify(data), response.status_code
    else:
        return jsonify({
            "error": "Failed to fetch from microservice",
            "data_returned_from_microservice": data
        }), response.status_code

# ----------------------------------------------------- POST /login
@app.route('/login', methods=['POST'])
@swag_from('swagger/login.yaml')
def login():
    response = requests.post(
        url=f"{MICROSERVICES['user']}/login",
        cookies=request.cookies,
        json=request.json,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        response_data = response.json()
        
        # Create the Flask response
        flask_response = jsonify(response_data)
        
        # Extract cookies from the microservice response
        if 'Authorization' in response.cookies:
            auth_cookie = response.cookies['Authorization']
            flask_response.set_cookie('Authorization', auth_cookie, httponly=True, secure=True)
        
        return flask_response, 200
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5002)))
