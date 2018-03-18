init:
	pip install -r requirements.txt

test:
	py.test -s tests

.PHONY: init test
