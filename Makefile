default: format test

test:
	@python quick.py
	@nosetests --with-coverage --cover-package quick

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
