worker:
	celery -A config.celery_app worker -l info

loaddata:
	python manage.py loaddata api/ecommerces/fixtures/platform.json

coverage:
	coverage run -m pytest
	coverage html
	open htmlcov/index.html
