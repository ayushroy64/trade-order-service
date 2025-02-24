# Trade Order API

This repository contains the implementation of a Trade Order API using FastAPI and SQLAlchemy. The API supports CRUD operations for managing trade orders.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Docker](#docker)
- [AWS Deployment](#aws-deployment)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Schemas](#schemas)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/trade_order_api.git
    cd trade_order_api
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.

## Docker

To run the application using Docker:

1. Build the Docker image:
    ```sh
    docker build -t trade_order_api .
    ```

2. Run the Docker container:
    ```sh
    docker run -d -p 8000:8000 trade_order_api
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.

## AWS Deployment

The service is deployed on AWS EC2 instance and can be accessed by navigating to `http://3.145.151.161:8000/`

## API Endpoints

### `POST /orders/`

Creates a new order.

#### Request Body:
- `order` (OrderCreate): The order data to be created.

#### Response:
- `200 OK`: The created order object.

### `GET /orders/`

Retrieves a list of orders with optional pagination.

#### Query Parameters:
- `skip` (int, optional): The number of records to skip. Default is 0.
- `limit` (int, optional): The maximum number of records to return. Default is 100.

#### Response:
- `200 OK`: A list of order objects.

## Database Models

### [Order](http://_vscodecontentref_/0)

Represents an order in the database.

#### Fields:
- [id](http://_vscodecontentref_/1) (int): The unique identifier of the order.
- [symbol](http://_vscodecontentref_/2) (str): The symbol of the order.
- [price](http://_vscodecontentref_/3) (float): The price of the order.
- [quantity](http://_vscodecontentref_/4) (int): The quantity of the order.
- [order_type](http://_vscodecontentref_/5) (str): The type of the order (e.g., "buy" or "sell").

## Schemas

### `OrderCreate`

Schema for creating a new order.

#### Fields:
- `symbol` (str): The symbol of the order.
- `price` (float): The price of the order.
- `quantity` (int): The quantity of the order.
- `order_type` (str): The type of the order (e.g., "buy" or "sell").

### `OrderStatusUpdate`

Schema for updating the status of an order.

#### Fields:
- `status` (str): The new status of the order.
