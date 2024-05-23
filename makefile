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
	pip install -r requirements.txt -t package
	cd package
	zip -r ../function.zip .
	cd ..
	cd data
	zip -r ../function.zip ./data
	cd ..
	cd function
	zip -r ../function.zip ./function
	cd ..
	zip function.zip lambda_function.py
	aws lambda update-function-code --function-name notify-purchases --zip-file fileb://function.zip
	rm -rf packagez
