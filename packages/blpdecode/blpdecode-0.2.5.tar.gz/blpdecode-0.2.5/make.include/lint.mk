# lint / source format

# blacken python source (code formatter)
fmt:  
	black $(project) tests

# check style, lint with flake8
lint: fmt
	isort $(project) tests
	flake8 $(project) tests
	black --check $(project) tests

# vim:ft=make
