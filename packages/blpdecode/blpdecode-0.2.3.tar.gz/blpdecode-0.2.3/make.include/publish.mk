# publish - build package and publish

#.dist:	gitclean tox

.PHONY: dist 
dist: .dist ## create distributable files if sources have changed
.dist:	gitclean 
	@echo Building $(project)
	pip wheel -w dist .
	@touch $@

# add a release tag to the current commit and git push it
release: dist 
	@echo pushing Release $(project) v$(version) to github...
	git tag -f -a 'v$(version)' -m 'Release v$(version)'
	git push -f origin 'v$(version)'

# publish to pypi
pypi-publish: release
	$(call require_pypi_config)
	@set -e;\
	if [ "$(version)" != "$(pypi_version)" ]; then \
	  $(call verify_action,publish to PyPi) \
	  echo publishing $(project) $(version) to PyPI...;\
	  flit publish;\
	else \
	  echo $(project) $(version) is up-to-date on PyPI;\
	fi

publish: pypi-publish

# check current pypi version 
pypi-check:
	$(call require_pypi_config)
	@echo '$(project) local=$(version) pypi=$(call check_pypi_version)'

publish-clean:
	rm -f .dist
	rm -rf .tox

# functions
define require_pypi_config =
$(if $(wildcard ~/.pypirc),,$(error publish failed; ~/.pypirc required))
endef

pypi_version := $(shell pip install $(project)==fnord.plough.plover.xyzzy 2>&1 |\
  awk -F'[,() ]' '/^ERROR: Could not find a version .* \(from versions:.*\)/{print $$(NF-1)}')

define check_null =
$(if $(1),$(1),$(error $(2)))
endef

check_pypi_version = $(call check_null,$(pypi_version),PyPi version query failed)
