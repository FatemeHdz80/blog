set -o errexit
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py collectstatic --no-input


