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

start:
	python3 main.py

install-package:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Instalando paquetes en directorio '.venv'"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	mkdir .venv
	pip install -r requirements_need.txt -t .venv

update-package:
	pip install -r requirements.txt -t .venv

zip-package:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Empaquetando código"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	zip -r function.zip .venv
	zip -r function.zip tmp
	zip -r function.zip utils
	zip -r function.zip function
	zip function.zip lambda_function.py

clean-package:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Limpiando archivos"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	rm -rf .venv
	rm function.zip

test-zip: install-package zip-package

test: dev_set lambda_invoke

update: install-package zip-package dev_set update_lambda clean-package

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

update_lambda:
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(HEADER)"Actualizando función lambda"$(END)
	@+echo $(HEADER)"---------------------------------------------"$(END)
	@+echo $(BOLD)""
	@if ! aws lambda update-function-code \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://function.zip \
		--region $(AWS_REGION); then \
		echo $(FAIL)"[ERROR] No se pudo actualizar la función lambda."$(END);\
		exit 1; \
	else \
		echo $(OKGREEN)"[OK] Función lambda actualizada."$(END); \
	fi
