Support Ticket Management System

Overview

This project is a Django REST Framework based system for managing support tickets, ensuring efficient assignment to agents while preventing race conditions. It is designed to handle high concurrency and scale efficiently.

Features

Admin Capabilities:

Create, update, delete tickets.

Manage all tickets.

Agent Capabilities:

Retrieve unassigned tickets (max 15 at a time).

Assign tickets upon retrieval.

Sell only assigned tickets.

Concurrency Handling:

Ensures no two agents receive the same ticket.

Prevents race conditions when fetching tickets.

Scalability:

Optimized queries to handle thousands of agents simultaneously.

Security:

Only admins can manage tickets.

Agents can only fetch and process their assigned tickets.

API Endpoints

Admin Endpoints

POST /api/tickets/ - Create a ticket.

PUT /api/tickets/{id}/ - Update a ticket.

DELETE /api/tickets/{id}/ - Delete a ticket.

Agent Endpoints

POST /api/tickets/fetch/ - Assign and fetch up to 15 unassigned tickets.

POST /api/tickets/{id}/sell/ - Mark a ticket as sold.


# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run the server
python manage.py runserver

Running Tests

python manage.py test

Deployment

The project includes a Dockerfile and docker-compose.yml for containerized deployment.

To start using Docker:

docker-compose up --build

ERD

The Entity-Relationship Diagram (ERD) for the system is included in erd.drawio.

Postman Collection

A Postman collection with example requests is provided in postman_collection.json.



