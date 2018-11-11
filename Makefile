.PHONY: build run test

build:
	./build_images.sh
run: build
	docker-compose -p surveyor up -d
stop:
	docker-compose -p surveyor down
test:
	docker run -t --network=container:surveyor_manager_1 surveyor -i inventory/docker.yml
