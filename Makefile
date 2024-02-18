SHELL=/bin/bash

.ALL: wellcome init test

wellcome:
	@echo "Hello There ! Welcome to CSU."

init:
	@mkdir -p "./output"
	@( \
       source .venv/bin/activate; \
       pip3 install -r requirements.txt; \
    )

test:
	@( \
       source .venv/bin/activate; \
       python3 -m unittest -v tests/*.py -v; \
    )

cnn:
	@( \
	   source .venv/bin/activate; \
   	   cd examples; \
       python3 for_cnn.py; \
    )