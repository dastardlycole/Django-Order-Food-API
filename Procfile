web: gunicorn -b "0.0.0.0:$PORT" -w 3 food_api.wsgi
release: python manage.py migrate