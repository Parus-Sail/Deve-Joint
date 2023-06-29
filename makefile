# How using Make? Just write in shell: make [command].
# 
# Example:
# > make go_local


# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

go: down build up

down: 
	docker-compose --file ./docker-compose.dev.yml down --remove-orphans

go_db: down
	docker-compose --file ./docker-compose.dev.yml up db -d;
	docker exec -it devejoint-db psql -U postgres -d postgres -c "DROP DATABASE deve_joint;"
	docker exec -it devejoint-db psql -U postgres -d postgres -c "CREATE DATABASE deve_joint;"
	chmod +x ./dev_tools/delete_migrations_files.sh & ./dev_tools/delete_migrations_files.sh
	./app/manage.py makemigrations	
	./app/manage.py migrate
	./app/manage.py shell < ./dev_tools/create_superuser.py
	# ✨✨ superuser is created ✨✨ 
	# 👤 login: admin@mail.ru 
	# 🔒 password: pass

	

go_local: go_db
	python app/manage.py runserver localhost:8000
	

build:
	docker-compose --file ./docker-compose.dev.yml build 


up:
	docker-compose --file ./docker-compose.dev.yml up




ff:
	yapf --in-place --recursive .

