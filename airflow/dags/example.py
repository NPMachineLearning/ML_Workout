from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
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

@task(task_id="logging")
def log(x):
    logging.info(x)


@dag(
    dag_id = "Example",
    description = "Data operation flow",
    default_args = default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["dev", "example", "flow"],
)
def example():
    x = task1()
    y = task2(x)
    log(y)

dag_example = example()