from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException
import csv
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
                            "http://label-studio:8080/api/projects/2/export",
                            params={"export_type": "CSV"},
                            headers={"Authorization": "Token 8823cc4fb910406253548fac3c458e495d6de86c"})

    try:                       
        with open('out.csv', 'wt') as f:
            writer = csv.writer(f)
            for line in response.iter_lines():
                print(line.decode('utf-8'))
                writer.writerow(line.decode('utf-8'))
    except Exception as e:
        print(e)
        raise AirflowException(e)

    return response

@task(task_id="logging")
def log(x):
    logging.debug(x)
    print(x.url)
    print(x.text)
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