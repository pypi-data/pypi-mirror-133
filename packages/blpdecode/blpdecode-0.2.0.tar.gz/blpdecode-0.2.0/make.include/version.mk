# version - automatic version management
 
# - Prevent version changes with uncommited changes
# - tag and commit version changes
# - Use 'lightweight tags'


bumpversion = bumpversion $(1) --commit --tag --current-version $(version) \
  --search '__version__ = "{current_version}"' --replace '__version__ = "{new_version}"' \
  $(project)/version.py

bump-patch: ## bump patch level
	$(call bumpversion,patch)

bump-minor: ## bump minor version, reset patch to zero
	$(call bumpversion,minor)

bump-major: ## bump version, reset minor and patch to zero
	$(call bumpversion,major)

timestamp: .timestamp ## update timestamp if sources have changed
.timestamp: $(src)
	sed -E -i $(project)/__init__.py -e "s/(.*__timestamp__.*=).*/\1 \"$$(date -Isec)\"/"
	@touch $@
	@echo "Timestamp Updated."

version-clean: # clean up version tempfiles
	rm -f .timestamp
