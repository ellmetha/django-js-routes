PROJECT_PACKAGE := js_routes
TEST_PACKAGE := tests


init:
	@printf "\n\n${YELLOW}---------------- Initialization ---${RESET} ${GREEN}Python dependencies${RESET}\n\n"

	pipenv install --dev --three

	@printf "\n\n${YELLOW}---------------- Done.${RESET}\n\n"


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
	pipenv run ipython

.PHONY: static_resolver
## Regenerate the static version of the routes resolver.
static_resolver:
	pipenv run ipython ./js_routes/_scripts/build_static_resolver.py


# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

.PHONY: qa
## Trigger all quality assurance checks.
qa: lint isort

.PHONY: lint
## Trigger Python code quality checks (flake8).
lint:
	pipenv run flake8

.PHONY: isort
## Check Python imports sorting.
isort:
	pipenv run isort --check-only --recursive --diff $(PROJECT_PACKAGE) $(TEST_PACKAGE)


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------

.PHONY: t tests
## Alias of "tests".
t: tests
## Run all the test suites.
tests: tests_python tests_javascript
## Run the Javascript test suite.
tests_javascript:
	npm test
## Run the Python test suite.
tests_python:
	pipenv run py.test

.PHONY: coverage
## Collects code coverage data for all codebases.
coverage: coverage_python coverage_javascript
## Collects code coverage data for the Javascript codebase.
coverage_javascript:
	npm test
## Collects code coverage data for the Python codebase.
coverage_python:
	pipenv run py.test --cov-report term-missing --cov $(PROJECT_PACKAGE)

.PHONY: spec spec_python
# Run test suites in "spec" mode.
spec: spec_python
# Run the Python test suite in "spec" mode.
spec_python:
	pipenv run py.test --spec -p no:sugar


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
