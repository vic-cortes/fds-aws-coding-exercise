
deploy-env:
	scripts/deploy-env.sh > /dev/null
	
deploy-go:
	scripts/deploy-go.sh > /dev/null

deploy-python:
	scripts/deploy-python.sh > /dev/null

deploy-node:
	scripts/deploy-node.sh > /dev/null

set_env_variables:
	@echo "Setting AWS Credentials..."
	export $(grep -v '^#' .env)

# Python only
export_serverless_requirements:
	@echo "Exporting requirements..."
	uv pip compile pyproject.toml -o app/python/requirements.txt