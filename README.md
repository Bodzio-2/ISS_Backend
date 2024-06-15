# ISS_Backend

## Installation & Run
- pip install -r requirements.txt
- python manage.py runserver
  - If that fails, try "python manage.py makemigrations driveway_data; python manage.py migrate"
- profit!

## Server url: http://127.0.0.1:8000
## Current endpoints:
- **POST** `parking_spot/` - create a new parking spot
  - example data:
  `{ "tags": "handicapped, bigger_spot" }`
- **GET** `parking_spot_actions/` - get possible actions (i.e. "Free" and "Take")
- **GET** `parking_spot/<int:spot_id>/` - get information about a specific parking spot
- **POST** `parking_spot/<int:spot_id>/new_entry/` - add a new entry to the database
  - example data:
  `{
    "timestamp": "2021-12-10",
    "action": "Free"
  }`
- **GET** `driveway_entry/<int:entry_id>/` - get a specific driveway entry
- **DELETE** `parking_spot/<int:spot_id>/delete_all/` - delete all entries from given parking spot
- **GET** `parking_spot/<int:spot_id>/all_entries/` - fetch all entries from given parking spot
