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
	pip install -r requirements.txt -t package

update-package:
	pip install -r requirements.txt -t package

zip-package:
	cd package && zip -r ../function.zip .
	cd ..
	zip -r function.zip data
	zip -r function.zip utils
	zip -r function.zip function
	zip function.zip lambda_function.py

