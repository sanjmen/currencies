web: gunicorn --bind :8000 --workers 2 --threads 8 config.wsgi:application
worker1: celery -A apps.taskapp worker -B -l INFO --autoscale=6,1 -Q update_klines,update_markets -n worker1@%n