# How using Make? Just write in shell: make [command].
# 
# Example:
# > make go_local
# > make go_docker


# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1



go_db: down
	docker-compose --file ./docker-compose.dev.yml up db;
	docker exec -it devejoint-db psql -U postgres -d postgres -c "DROP DATABASE deve_joint;"
	docker exec -it devejoint-db psql -U postgres -d postgres -c "CREATE DATABASE deve_joint;"
	chmod +x ./dev_tools/delete_migrations_files.sh & ./dev_tools/delete_migrations_files.sh
	./app/manage.py makemigrations	
	./app/manage.py migrate
	./app/manage.py migrate --run-syncdb
	./app/manage.py shell < ./dev_tools/create_superuser.py
	# ✨✨ superuser is created ✨✨ 
	# 👤 login: admin@mail.ru 
	# 🔒 password: pass
	# 📦 add fake datas:
	./app/manage.py loaddata ./dev_tools/fixtures/auth_app_user.yaml
	./app/manage.py loaddata ./dev_tools/fixtures/project_app_project.yaml
	./app/manage.py loaddata ./dev_tools/fixtures/role_app_role.yaml
	./app/manage.py loaddata ./dev_tools/fixtures/project_app_membership.yaml

go_docker: down build up

go_local: down go_db local

local:
	python app/manage.py runserver localhost:8000

test:
	chmod +x ./dev_tools/delete_migrations_files.sh & ./dev_tools/delete_migrations_files.sh
	./app/manage.py makemigrations	
	./app/manage.py migrate
	./app/manage.py migrate --run-syncdb
	pytest

ff:
	autoflake .
	isort .
	yapf --in-place --recursive .
	djlint --reformat ./app


# ============ Docker ============

down: 
	docker-compose --file ./docker-compose.dev.yml down --remove-orphans


build:
	docker-compose --file ./docker-compose.dev.yml build 


up:
	docker-compose --file ./docker-compose.dev.yml up

