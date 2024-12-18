# **Airline Management System**

A backend web application built with Django REST Framework (DRF) to manage airline operations, including airplanes,
flights, and passenger reservations.

## 🔰**About Features**

**Airplane Management:** Add, update, view, and delete airplanes.\
**Flight Management:** Add, update, and manage flights.\
**Reservation Management:** Add, update, and manage reservations.\
**Occupancy Check:** Ensures flight capacity isn't exceeded during reservations.\
**Unique Reservation Codes:** Automatically generated for every reservation.

## 🔌**Installation**
1. Clone the repository:
```bash
git clone https://github.com/b21827076/TechNarts.git
``` 
```bash
cd your-repository
```

## ⚡**Usage**
1. Set up a virtual environment and install dependencies:
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows:venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```

2. Apply database migrations:
```bash
python manage.py migrate
```

3.  **(0ptional)** Create superuser for [http://127.0.0.1:8000/admin/]() 
```bash
python manage.py createsuperuser
```
You can use admin panel with this user. For example, all airplane can be seen from this panel regardless of their status.

4. Start the development server:
```bash
python manage.py runserver
```

## 🔗**API Endpoints**
It is possible to test via [Postman Collection](AirlineManagementSystem.postman_collection.json) file which contains
API endpoints. Detailed descriptions and restrictions of all endpoints are available.


## _🚀I will be waiting for your reviews, thank you_
