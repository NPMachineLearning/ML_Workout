from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
import requests
import logging

default_args = {
    "owner": "airflow",
}

@task
def task1():
    return 1

@task
def task2(x):
    return x+1

@task(task_id="export")
def export_annotation():
    response = requests.get(
                            "http://label_studio:8080/api/projects/2/export",
                            params={"exportType": "CSV"},
                            headers={"Authorization": "Token 8823cc4fb910406253548fac3c458e495d6de86c"},
                            stream=True)
    return response

@task(task_id="logging")
def log(x):
    logging.info(x)
    print(x)
    return x


@dag(
    dag_id = "DevDataOps",
    description = "Data operation flow",
    default_args = default_args,
    schedule=None,
    start_date=days_ago(2),
    tags=["dev", "data_ops", "flow"],
)
def dev_data_ops():
    resp = export_annotation()
    log(resp)

dev_data_flow = dev_data_ops()