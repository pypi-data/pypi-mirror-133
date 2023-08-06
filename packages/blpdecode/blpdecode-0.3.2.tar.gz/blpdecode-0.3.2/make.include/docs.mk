# make clean targets

# generate Sphinx HTML documentation, including API docs
docs: clean-docs
	pip install -U .[docs]
	sphinx-apidoc -o docs/ blpdecode
	$(MAKE) -C docs html
	$(browser) docs/_build/html/index.html

# clean up documentation files
clean-docs:
	pip uninstall .[docs]
	rm -f docs/blpdecode.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean

# run a dev-mode docs webserver; recompiling on changes 
servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .
