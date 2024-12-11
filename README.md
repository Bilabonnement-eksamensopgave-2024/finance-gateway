# Finance Gateway

## Table of Contents 
1. [Overview](#overview) 
    - [Purpose](#purpose) 
    - [Key Responsibilities](#key-responsibilities) 
2. [Features](#features) 
3. [Technology Stack](#technology-stack) 
4. [Environment Variables](#environment-variables) 
5. [Routing Configuration](#routing-configuration) 
6. [Endpoints](#endpoints) 
    - [Base URL](#base-url) 
    - [Endpoint Documentation](#endpoint-documentation) 
7. [Swagger Documentation](#swagger-documentation) 


## Overview
### Purpose
- Acts as a central access point for routing requests to various microservices in the architecture.

### Key Responsibilities
- Load balancing and request forwarding.
- Centralized authentication and authorization.
- API rate limiting and logging (if applicable).

### Roles required: 
One of following roles are required for all endpoints except login and health:
- admin
- finance

## Features
- Reverse proxy for routing requests to services.
- Centralized API endpoint for the entire application.
- Swagger/OpenAPI documentation for the aggregated API endpoints.

## Technology Stack
- **Programming Language**: Python
- **Framework**: Flask
- **Routing Library**: Flask
- **API Documentation**: Swagger/OpenAPI
- **Deployment**: Azure Web App (Docker container)
- **CI/CD**: GitHub Actions

## Environment Variables
| Variable                   | Description                                      |
|----------------------------|--------------------------------------------------|
| SECRET_KEY                 | Secret key for the application                   |
| ABONNEMENT_MICROSERVICE_URL| URL for the subscription microservice              |
| USER_MICROSERVICE_URL      | URL for the user microservice                    |
| SKADE_MICROSERVICE_URL     | URL for the damage microservice                   |

## Routing Configuration
The gateway uses a configuration file (e.g., routes.json) to define service endpoints and routes. Example:
```json
{
    "/subscription": "https://abonnement-microservice-dkeda4efcje4aega.northeurope-01.azurewebsites.net",
    "/user": "https://user-microservice-d6f9fsdkdzh7hndv.northeurope-01.azurewebsites.net",
    "/damage": "https://skade-microservice-cufpgqgfcufqa8er.northeurope-01.azurewebsites.net"
}
```

## Endpoints
### Base URL
- **Local**: http://localhost:5002
- **Production (Azure)**: https://finance-gateway-b3grdpa6e6bterbg.northeurope-01.azurewebsites.net

### Endpoint Documentation

| Method | Endpoint                          | Description                                    | Request Body                                              | Response           |
|--------|-----------------------------------|------------------------------------------------|-----------------------------------------------------------|--------------------|
| GET    | /subscriptions                    | Retrieve all subscriptions                     | N/A                                                       | Depends on service |
| GET    | /subscriptions/current/total-price| Retrieve total price of current subscriptions  | N/A                                                       | Depends on service |
| GET    | /damage-reports                   | Retrieve all damage reports                    | N/A                                                       | Depends on service |
| GET    | /damage-types                     | Retrieve all damage types                      | N/A                                                       | Depends on service |
| GET    | /cars/<int:id>/total-cost         | Retrieve total damage costs for a car          | N/A                                                       | Depends on service |
| GET    | /subscriptions/<subscriptionId>/total-cost | Retrieve total damage costs for a subscription | N/A                                             | Depends on service |
| POST   | /login                            | Handle user login                              | `{"email": "user@example.com", "password": "userpassword"}`| Depends on service |
| GET    | /health                           | Health check for the service                   | N/A                                                       | 200                |

## Swagger Documentation 
Swagger UI is available at [`<Base URL>/docs`](https://finance-gateway-b3grdpa6e6bterbg.northeurope-01.azurewebsites.net/docs).