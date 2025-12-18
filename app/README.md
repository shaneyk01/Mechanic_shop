# Mechanic Shop API

Simple Flask REST API to manage customers, mechanics, and service tickets (with many-to-many assignment of mechanics to tickets).

## Features
- Customers CRUD
- Mechanics CRUD
- Service tickets CRUD
- Assign / remove mechanics on a ticket
- Marshmallow serialization
- MySQL (or sqlite if configured) via SQLAlchemy

## Tech Stack
- Python 3.11
- Flask / Flask-SQLAlchemy / Marshmallow
- MySQL (connector) or sqlite fallback

## Requirements
```
python -m pip install -r requirements.txt
```

## Environment
Example config (config/DevelopmentConfig):
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS = False

## Run
```
# Activate venv (PowerShell)
& venv/Scripts/Activate.ps1
python main.py
```

## Database Reset (DEV ONLY)
```
python scripts/reset_db.py
```

## Core Models
- Customer(id, name, email, phone, password, service_tickets[])
- Mechanic(id, name, email, salary, password, service_tickets[])
- ServiceTickets(id, date, customer_id, service_descr, mechanics[])

## API Endpoints (Base: http://127.0.0.1:5000)

### Customers
- POST /customers/
- GET /customers/
- GET /customers/<id>
- PUT /customers/<id>
- DELETE /customers/<id>

### Mechanics
- POST /mechanics/
- GET /mechanics/
- PUT /mechanics/<id>
- DELETE /mechanics/<id>

### Service Tickets
- POST /service_tickets/
- GET /service_tickets/
- PUT /service_tickets/<ticket_id>/add_mechanic/<mechanic_id>
- PUT /service_tickets/<ticket_id>/remove_mechanic/<mechanic_id>

## Example JSON

Create mechanic:
```
{
  "name": "Alice",
  "email": "alice@example.com",
  "salary": 60000,
  "password": "pw"
}
```

Create service ticket:
```
{
  "date": "2025-11-19",
  "customer_id": 1,
  "service_descr": "Brake pad replacement"
}
```

Add mechanic to ticket (PUT):
```
/service_tickets/1/add_mechanic/2
`-

submitted by:shaney hoyohoy

