# Finance Gateway

This gateway handles financial operations including subscriptions, pricing, and damage cost summaries.

## Table of Contents
- [API Endpoints](#api-endpoints)
  - [GET /](#get)
  - [GET /subscriptions](#get-subscriptions)
  - [GET /subscriptions/current/total-price](#get-subscriptionscurrenttotal-price)
  - [GET /damage-reports](#get-damage-reports)
  - [GET /damage-types](#get-damage-types)
  - [GET /cars/{id}/damage-costs](#get-carsiddamage-costs)
  - [GET /damage-reports/subscriptions/{subscriptionId}/total-damage](#get-damage-reportssubscriptionssubscriptionidtotal-damage)
  - [POST /login](#post-login)
- [Error Handling](#error-handling)
- [License](#license)

## API Endpoints

### GET /
- **Description**: Provides information about the service and its endpoints.
- **Example Request**:
    ```http
    GET /
    ```
- **Response**:
    ```json
    {
        "service": "Finance Gateway",
        "description": "This gateway handles financial operations including subscriptions, pricing, and damage cost summaries.",
        "endpoints": [
            {
                "path": "/subscriptions",
                "method": "GET",
                "description": "Get all subscriptions",
                "response": "JSON array of subscription objects",
                "role_required": "admin or finance"
            },
            ...
        ]
    }
    ```
- **Response Codes**: `200`, `500`

### GET /subscriptions
- **Description**: Retrieve a list of subscriptions.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /subscriptions
    ```
- **Response**:
    ```json
    [
        {
            "subscription_id": 1,
            "car_id": 101,
            "subscription_start_date": "2024-12-01",
            "subscription_end_date": "2025-12-01",
            "subscription_duration_months": 12,
            "km_driven_during_subscription": 15000,
            "contracted_km": 20000,
            "monthly_subscription_price": 26500,
            "delivery_location": "Copenhagen",
            "has_delivery_insurance": true
        },
        ...
    ]
    ```
- **Response Codes**: `200`, `400`, `500`

### GET /subscriptions/current/total-price
- **Description**: Retrieve the total price of current active subscriptions.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /subscriptions/current/total-price
    ```
- **Response**:
    ```json
    {
        "total_price": 599.98
    }
    ```
- **Response Codes**: `200`, `400`, `404`, `500`

### GET /damage-reports
- **Description**: Retrieve all damage reports.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /damage-reports
    ```
- **Response**:
    ```json
    [
        {
            "damagereportid": 1,
            "carid": 1,
            "subscriptionid": 1,
            "reportdate": "2024-12-07",
            "description": "Scratch on front bumper",
            "damagetypeid": 1
        },
        ...
    ]
    ```
- **Response Codes**: `200`, `204`, `500`

### GET /damage-types
- **Description**: Retrieve all damage types.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /damage-types
    ```
- **Response**:
    ```json
    [
        {
            "id": 1,
            "damage_type": "Ridse",
            "severity": "Minor",
            "repair_cost": 500
        },
        ...
    ]
    ```
- **Response Codes**: `200`, `500`

### GET /cars/{id}/damage-costs
- **Description**: Retrieve damage costs for a specific car by ID.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /cars/{id}/damage-costs
    ```
- **Response**:
    ```json
    {
        "car_id": 1,
        "total_damage_costs": 1500
    }
    ```
- **Response Codes**: `200`, `404`, `500`

### GET /damage-reports/subscriptions/{subscriptionId}/total-damage
- **Description**: Retrieve total damage costs for a specific subscription by ID.
- **Role Required**: admin or finance
- **Example Request**:
    ```http
    GET /damage-reports/subscriptions/{subscriptionId}/total-damage
    ```
- **Response**:
    ```json
    {
        "subscriptionid": 1,
        "total_amount": 1000
    }
    ```
- **Response Codes**: `200`, `404`, `500`

### POST /login
- **Description**: Authenticate an existing user.
- **Role Required**: none
- **Example Request**:
    ```http
    POST /login
    Content-Type: application/json

    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Login successful.",
        "Authorization": "Bearer <token>"
    }
    ```
- **Response Codes**: `200`, `400`, `401`, `500`

## Error Handling
- **400**: Bad Request - The request could not be understood or was missing required parameters.
- **401**: Unauthorized - Authentication failed or user does not have permissions for the desired action.
- **404**: Not Found - The requested resource could not be found.
- **500**: Internal Server Error - An error occurred on the server.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
