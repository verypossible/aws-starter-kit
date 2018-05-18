NAME = "verypossible/stacker"

all : docker-build

docker-build :
	docker build -t $(NAME) .
.PHONY: build


guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "\xE2\x98\xA0 " \
		"\033[31mEnvironment variable $* required but not set\033[0m" \
		"\xE2\x98\xA0"; \
		exit 1; \
	fi


shell: guard-AWS_ACCESS_KEY_ID guard-AWS_SECRET_ACCESS_KEY guard-AWS_DEFAULT_REGION
	docker-compose run --rm stacker bash
.PHONY: shell


build: guard-STACK
	stacker build --region ${AWS_DEFAULT_REGION} ${ARGS} conf/$(STACK).env stacker.yaml
.PHONY: build


destroy: guard-STACK
	stacker destroy --force --region ${AWS_DEFAULT_REGION} ${ARGS} conf/$(STACK).env stacker.yaml
.PHONY: destroy
