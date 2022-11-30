# Workout with Machine Learning

Allow machine to learn workout postures from the data that was produced by human. The postures such as push up, pull up and squat...etc. Later the machine can be used to detect certain postures that performed by user.

Increaseing performance in workout without human intervention is the goal.

# Project detail

## [Flow chart](https://whimsical.com/ml-workout-active-learning-labelling-flow-RfPRWopbAnZ1vMbQWoHS7m)

## Note
In local development, each tool is running in individual container in [Docker](https://www.docker.com/). Each tool has its own docker-compose.yaml file in addition there is a docker-compose.override.yaml file to override tool's network in docker, thus each container is able to communicate with each other such as consuming web api.

## Orchestration

[Airflow](https://airflow.apache.org/) is a tool to manage entire workflow including DataOps and MLOps. The goal is to trigger tasks such as data flow task, ML flow task.

### LabelingOps
Labeling operation flow involved human labeling. In addition import raw data from source and export data to destination(storage).

- **Tool**:
[Label Studio](https://labelstud.io/) is a tool for labeling data. As data coming in as form of image without label, human menual is required to label these image. Allow operation through web api.

- **Integration**:
[Label Studio](https://labelstud.io/) import/export storage require menual operation in order to sync data from souce or export labelled data to destination. Through web api, airflow is able to trigger syncing process for import and export storage. Airflow can trigger final data export as lablled CSV or JSON file and save it in data storage.

### DataOps

Data opration flow involved selecting storage for data, extract data from multiple source, loading data into multiple destination and transform data.

- **Data Storage**:
Select a right data storage is important for raw data or structured data.
    - [DataLake](https://madewithml.com/courses/mlops/data-stack/#data-lake):
  Amazon S3, Azure Blob Storage, Google Cloud Storage are common choices for cloud.
    - [DataWarehouse](https://madewithml.com/courses/mlops/data-stack/#data-warehouse)
    - [Database](https://madewithml.com/courses/mlops/data-stack/#database)

- **Extract and Load**:
[Airbyte](https://airbyte.com/) is a tool to extract data in [DataLake](https://madewithml.com/courses/mlops/data-stack/#data-lake) and then load it into destination [DataWarehouse](https://madewithml.com/courses/mlops/data-stack/#data-warehouse). The ability to extract data from multiple source and load data into multiple destination is the key. In addition it can be scheduled.
    - **Intergration**:
    Airflow is able to trigger extract and load task in airbyte.
    - **Local data source**: We can use [SFTP with Docker](https://hub.docker.com/r/atmoz/sftp) as a source for Airbyte locally. 
    - **Local data destination**: We can use [Postgres with Docker](https://hub.docker.com/_/postgres) as a destination for Airbyte locally. In addition combine it with [Adminer](https://hub.docker.com/_/adminer) to visualize and manage database easily. 
    
