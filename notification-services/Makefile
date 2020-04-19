# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20
## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## build grpc proto
proto:
	mkdir rpc/autogen
	cp protos/*.proto rpc/autogen
	python -m grpc_tools.protoc -I rpc --python_out=rpc/ --grpc_python_out=rpc/ rpc/autogen/*.proto
	rm rpc/autogen/*.proto
	rm -r autogen || true
	mv rpc/autogen .
## run application locally
start-local:
	python manage.py
build:
	docker build -t notif-grpc .
run:
	docker run --rm -p 11003:11000 --env-file=".env" notif-grpc python manage.py
