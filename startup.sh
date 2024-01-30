# This file is used as startup file in azure
flask db upgrade
gunicorn --bind=0.0.0.0 --timeout 600 codein:app