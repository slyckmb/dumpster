# =============================================================================
# 🧪 DUMPSTER Makefile — Versioned Test CLI Runner
# =============================================================================
# Auto-detects version from __version__.py to keep output & structure DRY
# Guardrails 2.2.2: All test folders, output folders, and logs trace back
# to tool version and spec used. No manual TAG input required.
# =============================================================================

NOW := $(shell date +"%Y%m%d-%H%M%S")
SRC ?= test/test_export.zip
BIN ?= ./dumpster.py
VERSION := $(shell grep VERSION __version__.py | head -n1 | cut -d '"' -f2)
DIR := ./test_output/$(VERSION)_$(NOW)

.DEFAULT_GOAL := help

## help: Show usage menu
help:
	@echo "🧪 DUMPSTER Test CLI — Make Targets"
	@echo "📦 VERSION: $(VERSION)"
	@echo "📂 OUTPUT DIR BASE: $(DIR)"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?##"}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

## test-tree: Output in TREE structure
test-tree: ## Test: Output in TREE structure
	@echo "🧪 [$(VERSION)] Testing TREE output to $(DIR)"
	@$(BIN) $(SRC) --structure tree --savepath "$(DIR)"

## test-flat: Output in FLAT structure
test-flat: ## Test: Output in FLAT structure
	@echo "🧪 [$(VERSION)] Testing FLAT output to $(DIR)"
	@$(BIN) $(SRC) --structure flat --savepath "$(DIR)"

## test-summary: Show summary only (no file output)
test-summary: ## Test: Show summary only (no file output)
	@echo "🧪 [$(VERSION)] Testing SUMMARY only"
	@$(BIN) $(SRC) --summary

## clean-tests: Remove all test_output folders
clean-tests: ## Clean: Remove all test_output folders
	@echo "🧼 Cleaning test_output/"
	@rm -rf ./test_output/*

## test-qa: Run all tests and generate QA log with version + timestamp
test-qa: ## QA: Full pipeline + log with version/timestamp
	@timestamp=$$(date +"%Y%m%d-%H%M"); \
	qafile="test_output/qa_log_$(VERSION)_$${timestamp}.txt"; \
	echo "🧪 QA TEST for DUMPSTER $(VERSION) at $${timestamp}" > "$$qafile"; \
	make clean-tests >> "$$qafile" 2>&1; \
	make test-summary >> "$$qafile" 2>&1; \
	make test-tree >> "$$qafile" 2>&1; \
	make test-flat >> "$$qafile" 2>&1; \
	echo "\n[📁 TEST OUTPUT FOLDER STRUCTURE]" >> "$$qafile"; \
	tree test_output >> "$$qafile" 2>&1; \
	echo "\n[📄 FILE CONTENTS]" >> "$$qafile"; \
	find test_output -type f ! -name "$$(basename $$qafile)" | while read file; do \
			echo "\n--- $$file ---" >> "$$qafile"; \
		cat "$$file" >> "$$qafile"; \
	done; \
	echo "\n✅ QA log saved to $$qafile"

.PHONY: help clean-tests test-summary test-tree test-flat test-qa
