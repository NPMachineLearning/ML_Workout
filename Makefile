# help
.PHONY: help
help:
	@echo "Commands:"
	@echo "init: for first time initialization"
	@echo "orchestration-up: start up orchestration in docker"
	@echo "orchestration-down: tear down orchestration in docker"
	@echo "label-studio-up: start up label studio in docker"
	@echo "label-studio-down: tear down label studio in docker"
	@echo "airbyte-up: start up airbyte in docker"
	@echo "airbyte-down: tear down airbyte in docker"
	@echo "airflow-up: start up airflow in docker"
	@echo "airflow-down: tear down airflow in docker"

# Init
.PHONY: init
init:
	docker compose -f airflow/docker-compose.yaml up airflow-init

# Airflow network
.PHONY: create-net
create-net:
	docker network create airflow_default

.PHONY: remove-net
remove-net:
	docker network rm airflow_default

# Orchestration
.PHONY: orchestration-up
orchestration-up: # start container in background
	docker compose -f airflow/docker-compose.yaml up -d
	docker compose -f label_studio/docker-compose.yaml up -d
	docker compose -f airbyte/docker-compose.yaml up -d
	docker compose -f sftp/docker-compose.yaml up -d

.PHONY: orchestration-down
orchestration-down:
	docker compose -f label_studio/docker-compose.yaml down
	docker compose -f airbyte/docker-compose.yaml down
	docker compose -f sftp/docker-compose.yaml down
	docker compose -f airflow/docker-compose.yaml down

# Label Studio
.PHONY: label-studio-up
label-studio-up:
	$(MAKE) create-net
	docker compose -f label_studio/docker-compose.yaml up -d

.PHONY: label-studio-down
label-studio-down:
	docker compose -f label_studio/docker-compose.yaml down
	$(MAKE) remove-net

# Airbyte
.PHONY: airbyte-up
airbyte-up:
	$(MAKE) create-net
	docker compose -f airbyte/docker-compose.yaml up -d

.PHONY: airbyte-down
airbyte-down:
	docker compose -f airbyte/docker-compose.yaml down
	$(MAKE) remove-net

# Airflow
.PHONY: airflow-up
airflow-up:
	docker compose -f airflow/docker-compose.yaml up -d

.PHONY: airflow-down
airflow-down:
	docker compose -f airflow/docker-compose.yaml down
