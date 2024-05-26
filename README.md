# ISS_Backend

## Installation & Run
- pip install -r requirements.txt
- python manage.py runserver
  - If that fails, try "python manage.py makemigrations driveway_data; python manage.py migrate"
- profit!

## Server url: http://127.0.0.1:8000
## Current endpoints:
- POST parking_spot/
  - example data:
  { "tags": "handicapped, bigger_spot" }
- GET parking_spot/{id}/
- GET parking_spot_actions/
