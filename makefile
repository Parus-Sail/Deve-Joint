# How using Make? Just write in shell: make [command].
# 
# Example:
# > make go_local


# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

go: down build up

go_db: 
	docker-compose --file ./docker-compose.dev.yml up db -d

go_local: go_db
	python app/manage.py runserver localhost:8000

build:
	docker-compose --file ./docker-compose.dev.yml build 

up:
	docker-compose --file ./docker-compose.dev.yml up

down: 
	docker-compose --file ./docker-compose.dev.yml down --remove-orphans


ff:
	yapf --in-place --recursive .

