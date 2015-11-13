db.rebuild:
	rm -rf migrations
	dropdb inspectors_dev
	createdb inspectors_dev
	make db.init

db.init:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade
	python manage.py seed_roles

db.empty:
	dropdb inspectors_dev
	createdb inspectors_dev
	python manage.py db upgrade
	python manage.py seed_roles
	make load_surveys
	make load_users

deploy:
	git push heroku master

load_users:
	python manage.py seed_user -e ehsiung@codeforamerica.org -r 1
	python manage.py seed_user -e sdengo@codeforamerica.org -r 1
	python manage.py seed_user -e mathias@codeforamerica.org -r 1
	python manage.py seed_user -e sarasti@miamidade.gov -r 1

load_surveys:
	python ./feedback/scripts/pull_data.py
