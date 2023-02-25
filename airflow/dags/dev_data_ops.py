from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from dataops_utils.label_studio_utils import sync_export_storage,  export_annotation
from dataops_utils.sftp_utils import write_csv_to_sftp
from dataops_utils.dbt_utils import dbt_transforms
import logging

default_args = {
    "owner": "airflow",
}

AIRBYTE_CONN_ID = "0f87b214-0d03-45b5-a72e-58382657a9c4"

SFTP_HOSTNAME = "SFTP"
SFTP_USERNAME = "usr"
SFTP_PASSWORD = "pass"

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
        connection_id=AIRBYTE_CONN_ID, # retrive from airbyte web (in url)
        asynchronous=False,
        timeout=3600,
        wait_seconds=3
    )

    # sync label studio export storage
    sync_storage_result = sync_export_storage()

    # export annotation from label studio
    resp_csv =  sync_storage_result >> export_annotation(export_type="CSV")

    # save csv to sftp aka mimic DataLake
    write_csv_result = write_csv_to_sftp(
        csv_data=resp_csv, 
        filename="ml_workout.csv", 
        host_name=SFTP_HOSTNAME, 
        user_name=SFTP_USERNAME, 
        user_password=SFTP_PASSWORD)
    
    # trigger airbyte extract and load
    extract_load_result = write_csv_result >> extract_and_load

    # trigger dbt data transformation
    extract_load_result >> dbt_transforms()

dev_data_flow = dev_data_ops()