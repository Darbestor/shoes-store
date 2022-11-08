# Shoes store. Example of microservices in Python

# Overview
**Shoes store** is an example project which demonstrates the use of microservices. Consists of 5 services and gateway written in **FastAPI**.

# Usage

## Run application in **docker compose**

```./compose.sh up -d --build```

## Run loccally

### Requirements

- Python 3.10
- Poetry

**Run commands in service's folder root**

Create virual environment:

```poetry install```

Run command with created virtual env:

``` uvicorn main:app --reload --port "port number" ``` 
 

# Architecture
![Alt text](Architecture_diagram.jpg?raw=true "Architecture")

| Service                          | Description                                                                 |
| ---------------------------------| :---------------------------------------------------------------------------|
| [gateway](./gateway)             | Entry point for client. Handles all requests and route to appropriate service. Contains openapi docs gathered from all services. |
| [users](./users)                 | Registers users and contain information about them in PostgreSQL |
| [catalog](./catalog)             | Serve as warehouse for store. Management of store products |
| [cart](./cart)                   | Stores the items in the user's shopping cart in MongoDB and retrieves it. When user ready to order send cart information to **orders** service through RabbitMQ |
| [orders](./orders)               | Consumes RabbitMQ messages and creates active user's orders. Order document in MongoDB has limited lifetime (15 min) before user complete the order. If user completed the order send order to **order_history** |
| [order_history](./order_history) | Contains user's order history |

