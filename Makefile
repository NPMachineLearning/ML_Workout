# help
.PHONY: help
help:
	@echo "Commands:"
	@echo "init: for first time initialization"
	@echo "orchestration-up: start up orchestration in docker"
	@echo "orchestration-down: tear down orchestration in docker"
	@echo "label-studio-up: start up label studio in docker"
	@echo "label-studio-down: tear down label studio in docker"
	@echo "sftp-up: start up sftp(ftp server) in docker"
	@echo "sftp-down: tear down sftp(ftp server) in docker"
	@echo "airbyte-up: start up airbyte in docker"
	@echo "airbyte-down: tear down airbyte in docker"
	@echo "dbt-up: start up dbt in docker"
	@echo "dbt-down: tear down dbt in docker"
	@echo "airflow-up: start up airflow in docker"
	@echo "airflow-down: tear down airflow in docker"

# Init
.PHONY: init
init:
	docker compose -f airflow/docker-compose.yaml up airflow-init

# Network
.PHONY: init-network
init-network:
	docker network create airflow_default

.PHONY: rm-network
rm-network:
	docker network rm airflow_default

# Orchestration
.PHONY: orchestration-up
orchestration-up: # start container in background
	$(MAKE) airflow-up
	$(MAKE) warehouse-up
	$(MAKE) label-studio-up
	$(MAKE) sftp-up
	$(MAKE) airbyte-up
	$(MAKE) dbt-up

.PHONY: orchestration-down
orchestration-down:
	$(MAKE) dbt-down
	$(MAKE) airbyte-down
	$(MAKE) label-studio-down
	$(MAKE) sftp-down
	$(MAKE) warehouse-down
	$(MAKE) airflow-down

# Label Studio
.PHONY: label-studio-up
label-studio-up:
	docker compose -f label_studio/docker-compose.yaml \
	-f label_studio/docker-compose.override.yaml up -d

.PHONY: label-studio-down
label-studio-down:
	docker compose -f label_studio/docker-compose.yaml \
	-f label_studio/docker-compose.override.yaml down

# sftp
.PHONY: sftp-up
sftp-up:
	docker compose -f sftp/docker-compose.yaml \
	-f sftp/docker-compose.override.yaml up -d

.PHONY: sftp-down
sftp-down:
	docker compose -f sftp/docker-compose.yaml \
	-f sftp/docker-compose.override.yaml down

# Airbyte
.PHONY: airbyte-up
airbyte-up:
	docker compose -f airbyte/docker-compose.yaml \
	-f airbyte/docker-compose.override.yaml up -d

.PHONY: airbyte-down
airbyte-down:
	docker compose -f airbyte/docker-compose.yaml \
	-f airbyte/docker-compose.override.yaml down

# dbt
.PHONY: dbt-up
dbt-up:
	docker compose -f dbt/docker-compose.yaml \
	-f dbt/docker-compose.override.yaml up -d

.PHONY: dbt-down
dbt-down:
	docker compose -f dbt/docker-compose.yaml \
	-f dbt/docker-compose.override.yaml down

# warehouse database
.PHONY: warehouse-up
warehouse-up:
	docker compose -f warehouse/docker-compose.yaml \
	-f warehouse/docker-compose.override.yaml up -d

.PHONY: warehouse-down
warehouse-down:
	docker compose -f warehouse/docker-compose.yaml \
	-f warehouse/docker-compose.override.yaml down

# Airflow
.PHONY: airflow-up
airflow-up:
	docker compose -f airflow/docker-compose.yaml up -d

.PHONY: airflow-down
airflow-down:
	docker compose -f airflow/docker-compose.yaml down
