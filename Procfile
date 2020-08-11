release: python manage.py migrate
web: gunicorn central_error.wsgi --max-requests 1200