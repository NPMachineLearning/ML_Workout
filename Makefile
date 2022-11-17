# help
.PHONY: help
help:
	@echo "Commands:"
	@echo "orchestration-up: start up orchestration in docker"
	@echo "orchestration-down: tear down orchestration in docker"

# Orchestration
.PHONY: orchestration-up
orchestration-up: # start container in background
	docker compose -f label_studio/docker-compose.yaml up -d
	docker compose -f airbyte/docker-compose.yaml up -d
	docker compose -f sftp/docker-compose.yaml up -d
	docker compose -f airflow/docker-compose.yaml up airflow-init
	docker compose -f airflow/docker-compose.yaml up -d

.PHONY: orchestration-down
orchestration-down:
	docker compose -f label_studio/docker-compose.yaml down
	docker compose -f airbyte/docker-compose.yaml down
	docker compose -f sftp/docker-compose.yaml down
	docker compose -f airflow/docker-compose.yaml down
