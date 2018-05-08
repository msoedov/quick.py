default: format test

test:
	@nosetests --with-coverage --cover-package quick --with-doctest --rednose --nocapture


qc:
	@nosetests --rednose --with-watch


clean:
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -exec rm -fr {} \;
	@rm -rf dist
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build

format:
	@echo "Formating:"
	@yapf  -dr ./
	@yapf  -ir ./

link-examples:
	@rm -f examples
	@ln -s  tests/fixtures examples


req:
	@pip install -r requirements_dev.txt

ts:
	@monkeytype run -m nose