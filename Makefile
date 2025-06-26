.PHONY: install lint test run db-migrate clean

install:
	pip install -r requirements.txt

lint:
	flake8 app/

test:
	PYTHONPATH=$(PWD) pytest

run:
	PYTHONPATH=$(PWD) FLASK_APP=MY_APP:create_app flask run

db-migrate:
	PYTHONPATH=$(PWD) FLASK_APP=MY_APP:create_app flask db upgrade

clean:
	find . -type f -name '*.pyc' -delete