# Django Notes

A small multi-user notes app: sign up / log in, create, edit, delete, pin and search your own notes.
Each user only ever sees their own notes.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations notes
python manage.py migrate
python manage.py createsuperuser  # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign up.

## Tests

```bash
python manage.py test
```

## Production notes

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` and `DJANGO_ALLOWED_HOSTS=yourdomain.com`,
then run `python manage.py collectstatic` and serve with gunicorn plus a static file server
(or WhiteNoise).
