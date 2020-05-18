# Website log storage API

- Run the Django server on port 8001 ~ ```python manage.py runserver 127.0.0.1:8001```
- Run monitor_queue.py ~ ```python monitor_queue.py```
- After generating 5 visit logs, check logs_api collection of logs_api MongoDB database.

# Tutorial progress logs API

pip install django-cors-headers

- Run the Django server on port 8001 ~ ```python manage.py runserver 127.0.0.1:8001```
- The views defined in *logs_api/views.py* define the API methods for tutorial progress logs.
