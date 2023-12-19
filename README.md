# Notifications_service
A Django application for managing clients and mailings

# Overview

The project is a notification service developed using Django framework. 
It facilitates the creation of mailings and targeted message delivery to clients meeting specific criteria such as mobile operator codes and tags

# Installation

## Clone the repository to your local machine:
```
git clone https://github.com/Githumaru/Notifications_service.git
```

## Navigate to the project directory:
```
cd notifications_service
```

## Run the project using Docker Compose:
```
docker-compose up
```

### Open your web browser and go to http://localhost:8000 to access the application.

# Usage

## API Endpoints

### Creating a Mailing

Endpoint: /mailings/
Method: POST
Description: Create a new mailing to send messages to clients based on specific criteria.
Request Body:

```
{
    "start_datetime": "2024-01-01T00:00:00Z",
    "end_datetime": "2024-01-10T00:00:00Z",
    "message_text": "Your message here",
    "tag": "example_tag",
    "mobile_operator_code": "ABC"
}
```

### Sending Messages to Clients

Endpoint: /mailings/{mailing_id}/send-messages/
Method: POST
Description: Trigger sending messages to clients who fit the criteria specified in the mailing.
