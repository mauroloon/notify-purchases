# ==============================================================================
# DATOS DEL PROYECTO
# ==============================================================================

DEV_AWS_REGION = us-east-2
DEV_TESTING = setup/test/$(TEST_FILE).json
DEV_SETTINGS = setup/secrets.json

FUNCTION_NAME = notify-purchases

ifdef TEST
	TEST_FILE = $(TEST)
else
	TEST_FILE = test
endif

# ==============================================================================
# CONFIGURACIONES DE COLORES
# ==============================================================================
HEADER = '\033[96m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# ==============================================================================
# FUNCIONES
# ==============================================================================

lint:
	flake8 --max-line-length=100 --per-file-ignores="__init__.py:F401"

black:
	black . --skip-string-normalization

cleanimports:
	isort --force-single-line-imports -rc .
	autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports .

clean-lint: cleanimports black lint

update-test:
	zip -r function.zip .
	aws lambda update-function-code --function-name notify-purchases --zip-file fileb://function.zip
	aws lambda get-function --function-name notify-purchases
	rm function.zip

update-test2:
	mkdir package
	pip install -r requirements.txt -t package && cd package && zip -r ../function.zip .
	cd ..
	zip -r function.zip data
	zip -r function.zip utils
	zip -r function.zip function
	zip function.zip lambda_function.py
	aws lambda update-function-code --function-name notify-purchases --zip-file fileb://function.zip
	rm -rf package
	rm function.zip

start:
	python3 main.py

install-package:
	mkdir package
	pip install -r requirements_lambda.txt -t package

update-package:
	pip install -r requirements.txt -t package

zip-package:
	cd package && zip -r ../function.zip .
	cd ..
	zip -r function.zip tmp
	zip -r function.zip utils
	zip -r function.zip function
	zip function.zip lambda_function.py

clean-package:
	rm -rf package
	rm function.zip

test: dev_set lambda_invoke

dev_set:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Carga Desarrollo"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	$(eval AWS_REGION=$(DEV_AWS_REGION))
	$(eval TESTING=file://$(DEV_TESTING))
	$(eval SETTINGS=file://$(DEV_SETTINGS))
	$(eval SETTINGS_PATH=$(DEV_SETTINGS))
	$(eval STAGE=dev)


lambda_invoke:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Invocando prueba síncrona a función lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(BOLD)""
	@if ! aws lambda invoke \
		--invocation-type RequestResponse \
		--function-name $(FUNCTION_NAME) \
		--region $(AWS_REGION) \
		--log-type Tail \
		--payload $(TESTING) \
		--cli-binary-format raw-in-base64-out \
		--cli-binary-format raw-in-base64-out \
		output | grep LogResult | sed 's/.*LogResult": "//; s/", //' | base64 --decode -i; then \
		echo $(FAIL)"[ERROR] Invocación fallida, revisar formato de 'test.json' o que los parámetros sean correctos."$(END);\
		exit 1; \
	else \
		echo $(OKGREEN)"[OK] Invocación existosa. Logs de invocación generados."$(END); \
	fi
	@+echo ""
	@+echo $(HEADER)"Resultado de la invocación"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(WARNING)""
	@if ! cat output | jq; then \
		echo $(FAIL)"\n[ERROR] No se pudo generar el resultado de la función."$(END);\
		exit 1; \
	else \
		echo $(OKGREEN)"\n\n[OK] Resultado de función lambda existoso."$(END); \
	fi
	@rm -rf output
