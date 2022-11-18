# Workout with Machine Learning

Allow machine to learn workout postures from the data that was produced by human. The postures such as push up, pull up and squat...etc. Later the machine can be used to detect certain postures that performed by user.

Increaseing performance in workout without human intervention is the goal.

# Project detail

## [Flow chart](https://whimsical.com/ml-workout-active-learning-labelling-flow-RfPRWopbAnZ1vMbQWoHS7m)

## Orchestration

[Airflow](https://airflow.apache.org/) is a tool to manage entire workflow including DataOps and MLOps.

## DataOps

Data opration flow involved selecting storage for data, extract data, loading data and transform data.

### Data Storage

Select a right data storage is important

- [DataLake](https://madewithml.com/courses/mlops/data-stack/#data-lake)
  Amazon S3, Azure Blob Storage, Google Cloud Storage are common choices for cloud. However to mimic DataLake at local machine we can use [SFTP with Docker](https://hub.docker.com/r/atmoz/sftp).
- [DataWarehouse](https://madewithml.com/courses/mlops/data-stack/#data-warehouse)
- [Database](https://madewithml.com/courses/mlops/data-stack/#database)

### Labeling

[Label Studio](https://labelstud.io/) is a tool for labeling data. As data coming in in form of image without label, human resource is needed to label these image.

### Extract and Load

[Airbyte](https://airbyte.com/) is a tool to extract data in [DataLake](https://madewithml.com/courses/mlops/data-stack/#data-lake) and then load it into destination [DataWarehouse](https://madewithml.com/courses/mlops/data-stack/#data-warehouse). The ability to extract data from multiple source and load data into multiple destination is the key. In addition it can be scheduled.
