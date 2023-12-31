INITIAL SETUP

Clone the repository:
git clone https://github.com/Kalyani-washimkar/Vendor-Management-System.git

Navigate to the project directory:
cd Vendor-Management-System


Activate virtualenv:
VMS_env\scripts\activate

Install Django:
pip install Django

Install the Django Rest Framework:
pip install djangorestframework


Apply database migrations:
python manage.py makemigrations
python manage.py migrate


Run the development server using following command:
python manage.py runserver


In the VSCode terminal, first create a superuser by the command: 
python manage.py createsuperuser --username your_username --email your_email


After the superuser created, add the username and password to request body of apitoken api, and token will be generated.
Add this token to all apis's request headers as authorization as key and token as its value.


Setup instructions and details on using the API endpoints:

I have used Postman for API testing and demonstrated the functionality and reliability of the endpoints.
Follow the url below and click on 'Run in Postman' which is in the top right side corner to open Postman.


API test suite - https://documenter.getpostman.com/view/22758399/2s9Ykq8gJg


API Endpoint Details:

VENDORS:

1. List/Create Vendors:

URL: vendors/
Method: GET (List Vendors), POST (Create Vendor)
Authentication: Token Authentication required

2. Retrieve/Update Vendor:

URL: vendor_details/<int:pk>/
Method: GET (Retrieve Vendor), PUT (Update Vendor)
Authentication: Token Authentication required

3. Delete Vendor:

URL: vendors/delete/<int:pk>/
Method: DELETE
Authentication: Token Authentication required

PURCHASE ORDERS:

1. List/Create Purchase Orders:

URL: purchase_orders/
Method: GET (List Purchase Orders), POST (Create Purchase Order)
Authentication: Token Authentication required

2. Retrieve/Update Purchase Order:

URL: purchase_orders/<int:pk>/
Method: GET (Retrieve Purchase Order), PUT (Update Purchase Order)
Authentication: Token Authentication required

3. Delete Purchase Order:

URL: purchase_orders/delete/<int:pk>/
Method: DELETE
Authentication: Token Authentication required.


Acknowledge Purchase Order:

URL: purchase_orders/<int:pk>/acknowledge/
Method: PUT (Acknowledge Purchase Order)
Authentication: Token Authentication required


Retrieve Vendor Performance:

URL: /vendors/<int:pk>/performance/
Method: GET (Retrieve Vendor Performance)
Authentication: Token Authentication required
