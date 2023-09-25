tune-with-debug:
	HYDRA_FULL_ERROR=1 python llmflowoptimizer/tune.py

fix-lint:
	black .
