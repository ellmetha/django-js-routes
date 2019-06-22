PROJECT_PACKAGE := main
PROJECT_CONFIGURATION_PACKAGE := project
DJANGO_SETTINGS_MODULE := $(PROJECT_CONFIGURATION_PACKAGE).settings.dev


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to launch development server, generate
# locales, etc.
# --------------------------------------------------------------------------------------------------


.PHONY: c console
## Alias of "console".
c: console
## Launch a development console.
console:
	pipenv run python manage.py shell --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: s server
## Alias of "server".
s: server
## Launch a development server.
server:
	pipenv run python manage.py runserver 0.0.0.0:8000 --settings=$(DJANGO_SETTINGS_MODULE)

## Generate new database migrations.
migrations:
	pipenv run python manage.py makemigrations --settings=$(DJANGO_SETTINGS_MODULE) ${ARG}

.PHONY: migrate
## Run the database migrations.
migrate:
	pipenv run python manage.py migrate --settings=$(DJANGO_SETTINGS_MODULE)

.PHONY: superuser
## Create a superuser.
superuser:
pipenv run python manage.py createsuperuser --settings=$(DJANGO_SETTINGS_MODULE)


# MAKEFILE HELPERS
# ~~~~~~~~~~~~~~~~
# The following rules can be used to list available commands and to display help messages.
# --------------------------------------------------------------------------------------------------

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help
## Print Makefile help.
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<action>${RESET}'
	@echo ''
	@echo 'Actions:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)-30s${RESET}\t${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -t'|' -sk1,1
