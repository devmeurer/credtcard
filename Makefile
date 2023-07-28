export PYTHONPATH=$(shell pwd)/
export PYTHONDONTWRITEBYTECODE=1

test:
	docker-compose up --build -d
	docker-compose exec api coverage run -m pytest . --disable-warnings
	docker-compose exec api coverage report

down: ## down all containers
	docker-compose down -v

isort: # sort imports PEP8
	docker-compose run --service-ports -e --rm api bash -c "isort ."

black: # linter to organize readable code
	docker-compose run --service-ports -e --rm api bash -c "python -m black ."
	
clear:
	docker-compose down -v
	docker system prune -af
	docker volume prune -f
