run:
	poetry run python backend/manage.py runserver

create-su:
	poetry run python backend/manage.py createsuperuser

make-migrations:
	poetry run python backend/manage.py makemigrations

migrate:
	poetry run python backend/manage.py migrate