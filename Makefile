help:
	@echo "Usage:"
init:
	@rm -rf env venv
	@python3 -m virtualenv venv
	@( \
		source venv/bin/activate; \
		python3 -m pip install -r requirements.txt; \
		python3 -m pip install -r requirements.dev.txt; \
	)
	@echo "Activate venv: source venv/bin/activate"
lint:
	@( \
		source venv/bin/activate; \
		python -m flake8 bt_player_control.py tests/*; \
		python -m pylint --disable=fixme bt_player_control.py tests/*; \
	)
test: lint
	@( \
		source venv/bin/activate; \
		python3 -m unittest tests/test_*.py; \
	)
