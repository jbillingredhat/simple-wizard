.PHONY: install dev test clean run example help

help:
	@echo "Simple Wizard - Available targets:"
	@echo ""
	@echo "  make install          - Install Simple Wizard"
	@echo "  make dev              - Install in development mode"
	@echo "  make run              - Run the wizard server"
	@echo "  make example-sh       - Run bash example (requires wizard running)"
	@echo "  make example-py       - Run Python example (requires wizard running)"
	@echo "  make test             - Run test script (requires wizard running)"
	@echo "  make test-log         - Run log panel test (requires wizard running)"
	@echo "  make test-validation  - Run validation test (requires wizard running)"
	@echo "  make clean            - Remove build artifacts and socket file"
	@echo "  make deps             - Install system dependencies (Fedora)"
	@echo ""

deps:
	@echo "Installing system dependencies..."
	sudo dnf install python3-gobject gtk4 jq

install:
	@echo "Installing Simple Wizard..."
	pip install .

dev:
	@echo "Installing Simple Wizard in development mode..."
	pip install -e .

run:
	@echo "Starting wizard server..."
	@echo "Use Ctrl+C to stop"
	simple-wizard

example-sh:
	@echo "Running bash example..."
	./examples/example_install.sh

example-py:
	@echo "Running Python example..."
	./examples/example_install.py

test:
	@echo "Running tests..."
	./test_wizard.sh

test-log:
	@echo "Running log panel test..."
	./test_log.sh

test-validation:
	@echo "Running validation test..."
	./test_validation.sh

clean:
	@echo "Cleaning up..."
	rm -rf build dist *.egg-info
	rm -rf simple_wizard/__pycache__ simple_wizard/*.pyc
	rm -f /tmp/simple-wizard.sock
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete"

# Targets for running wizard and example together
demo-sh:
	@echo "This will run the wizard and bash example"
	@echo "Press Ctrl+C when done"
	@echo ""
	@echo "Starting wizard in 2 seconds..."
	@sleep 2
	@(simple-wizard &) && sleep 2 && ./examples/example_install.sh ; killall simple-wizard 2>/dev/null || true

demo-py:
	@echo "This will run the wizard and Python example"
	@echo "Press Ctrl+C when done"
	@echo ""
	@echo "Starting wizard in 2 seconds..."
	@sleep 2
	@(simple-wizard &) && sleep 2 && ./examples/example_install.py ; killall simple-wizard 2>/dev/null || true
