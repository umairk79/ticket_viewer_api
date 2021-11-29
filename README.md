# Ticket Viewer
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs. This backend REST API application is build on Django REST Framework.

## Requirements
- Python 3.6/3.7/3.8(recommended)
- Django 
- Django REST Framework
- Other packages mentioned in requirements.txt

## Installation
After you cloned the repository, please install python and pip. Official documentation for python and pip installation can be found [here](https://www.python.org/doc/)

Once python and pip setup is complete, please move into the root project directory and run the following command. This will install all the required libraries.
```
pip install -r requirements.txt
```

## Structure
In this API, we have one single resource, `tickets`, so we will use the following URL - `/tickets/` for fetching tickets from Zendesk API:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`tickets/` | POST | READ | Get all tickets for a given user and a given page(pagination)

The reason for the above URL being POST is because user sensitive data is being taken which shouldn't be passed as URL params as in the case of GET.

## Server Startup

Run the commands below for starting up the server
```
python manage.py makemigrations (Not required/mandatory)
python manage.py migrate (Not required/mandatory)
python manage.py runserver
```

## API Usage
We can test the API using [curl](https://curl.haxx.se/), or we can use [Postman](https://www.postman.com/)

Once the server has started we can access the below URL (Note: The default port is set as 8000, if changed please change the port in the API URL too.)
```
curl -d '{"email":"a@b.c", "password":"xxx", "subdomain": "zcc", "page": 1}' -H "Content-Type: application/json" -X POST https://127.0.0.1:8000/tickets/
```
Success Response:
```
{
    "tickets": [
        {
            "id": 1,
            "subject": "Sample ticket: Meet the ticket",
            "description": "I’m having a problem setting up your new product.",
            "requester_id": 1523712327041,
            "assignee_id": 1523619291862,
            "status": "open",
            "created_at": "2021-11-20T06:04:51Z",
            "updated_at": "2021-11-20T06:04:51Z",
            "tags": [
                "sample",
                "support",
                "zendesk"
            ]
        }
    ],
    "count": 110
}
```

Error response (with status code 401)
```
{
    "error": "Couldn't authenticate you"
}
```
The API internally calls the Zendesk tickets API for fetching ticket details for the users. The query params and sort params are defined in the global settings file (more on this below). Also the fields that are to be sent in the response are mentioned in the settings file. This API takes all the details from the user (email, password, subdomain, page number) and then calls the Zendesk Tickets API. The response payload is then filtered and then sent back to the frontend. All API exceptions are also handled in the code (eg. Timeout, Bad URL, Not found, Authentication failure etc).


## Testing

The unit test for the tickets api are written in tickets/test.py.
For testing run the following command.
```
python manage.py test
```

## Configuration

The configuration for the applicaiton is maintained in the global settings.py file.

```
ZENDESK_API_URL = "https://<<subdomain>>.zendesk.com/api/v2/tickets?"
ZENDESK_API_QUERY = "sort_by=updated_at&sort_order=desc"
FIELDS_TO_SEND = "id,subject,description,requester_id,assignee_id,status,created_at,updated_at,tags"
```
API url is the Zendesk Tickets API URL.

API Query are the query params used for sorting.

Field to send param specifies the ticket keys for which the data is to be sent to the frontend. Can be changed as per use case.

Instead of changing the main code these properties can be changed globally (env properties). Another way to do this is via a .ini file. Both ways are widely used.

## Checkins
All Github checkin commits messages have the corresponding Zendesk ticket ID. For eg. I created a ticket(Zendesk Ticket #3) for initializing Django app and referenced the ticket number in the corresponding commit (cf0e6f1049c1a4e7bbef34c55163f1490d2f1d1c).