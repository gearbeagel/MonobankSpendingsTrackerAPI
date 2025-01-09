run:
	poetry run python backend/manage.py runserver

migrate:
	docker-compose run --rm app sh -c "poetry run python manage.py migrate"

migrations:
	docker-compose run --rm app sh -c "poetry run python manage.py makemigrations"

superuser:
	docker-compose run --rm app sh -c "poetry run python manage.py createsuperuser"

create-app:
	docker-compose run --rm app sh -c "poetry run python manage.py startapp $(N)"

