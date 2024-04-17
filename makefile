lint:
	flake8 --max-line-length=100 --per-file-ignores="__init__.py:F401"

black:
	black . --skip-string-normalization

cleanimports:
	isort --force-single-line-imports -rc .
	autoflake -r -i --remove-all-unused-imports --ignore-init-module-imports .

clean-lint: cleanimports black lint