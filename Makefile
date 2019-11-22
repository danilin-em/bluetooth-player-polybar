help:
	@echo "Usage:"
init:
	@python3 -m virtualenv env
	@( \
		source env/bin/activate; \
		python3 -m pip install -r requirements.txt; \
		python3 -m pip install -r requirements.dev.txt; \
	)
	@echo "Activate env: source env/bin/activate"
lint:
	@( \
		source env/bin/activate; \
		python -m flake8 bt_player_control.py tests/*; \
		python -m pylint bt_player_control.py tests/*; \
	)
test: lint
	@( \
		source env/bin/activate; \
		python3 -m unittest tests/test_*.py; \
	)
