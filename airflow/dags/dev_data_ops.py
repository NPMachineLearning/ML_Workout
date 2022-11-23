from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.exceptions import AirflowException
from paramiko.client import SSHClient
import paramiko
import csv
import requests
import logging

default_args = {
    "owner": "airflow",
}

LABEL_STUDIO_URL = "http://label-studio:8080"
LABEL_STUDIO_EXPORT_TYPE = "CSV"
LABEL_STUDIO_TOKEN = "8823cc4fb910406253548fac3c458e495d6de86c"
SFTP_HOSTNAME = "sftp"
SFTP_USERNAME = "usr"
SFTP_PASSWORD = "pass"

@task(task_id="export_annotation")
def export_annotation():
    # export csv from label-studio
    response = requests.get(
                            f"{LABEL_STUDIO_URL}/api/projects/2/export",
                            params={"export_type": LABEL_STUDIO_EXPORT_TYPE},
                            headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})

    # create a ssh client for sftp server
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:                       
        # connect ssh client to sftp server 
        client.connect(SFTP_HOSTNAME, username=SFTP_USERNAME, password=SFTP_PASSWORD)

        # create a session
        session = client.open_sftp()

        # go to upload folder in sftp server
        session.chdir("upload")

        # create a file in sftp server and write data into file and save
        with session.open("ml_workout.csv", mode="w") as f:
            writer = csv.writer(f, delimiter=",")
            for line in response.iter_lines():
                writer.writerow(line.decode("utf-8").split(","))

        # close session and client        
        session.close()
        client.close()
    except Exception as e:
        client.close()
        print(e)
        raise AirflowException(e)

    return response

@dag(
    dag_id = "DevDataOps",
    description = "Data operation flow",
    default_args = default_args,
    schedule=None,
    start_date=days_ago(2),
    tags=["dev", "data_ops", "flow"],
)
def dev_data_ops():
    extract_and_load = AirbyteTriggerSyncOperator(
        task_id='airbyte_extract_and_load',
        airbyte_conn_id='airbyte', # configured in adim->connections in airflow
        connection_id='3c29d719-2e40-4b85-b056-5c62587881c2', # retrive from airbyte web (in url)
        asynchronous=False,
        timeout=3600,
        wait_seconds=3
    )

    resp = export_annotation()
    extract_and_load

dev_data_flow = dev_data_ops()