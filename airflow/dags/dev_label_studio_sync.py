from airflow.decorators import dag
from airflow.utils.dates import days_ago
from dataops_utils.label_studio_utils import sync_import_storage, sync_export_storage, export_annotation
from dataops_utils.sftp_utils import write_csv_to_sftp

default_args = {
    "owner": "airflow",
}

SFTP_HOSTNAME = "sftp"
SFTP_USERNAME = "usr"
SFTP_PASSWORD = "pass"

@dag(
    dag_id = "DevLabelStudioStorageSync",
    description = "Labeling flow",
    default_args = default_args,
    schedule=None,
    start_date=days_ago(2),
    tags=["dev", "labeling", "flow"],
)
def dev_labeling_ops():
    # sync label studio import and export storage
    result = sync_import_storage() >> sync_export_storage()

    # export label studio annotation as csv
    resp_csv =  result >> export_annotation(export_type="CSV")

    # save csv to sftp aka mimic DataLake
    result = write_csv_to_sftp(
        csv_data=resp_csv, 
        filename="ml_workout.csv", 
        host_name=SFTP_HOSTNAME, 
        user_name=SFTP_USERNAME, 
        user_password=SFTP_PASSWORD)


dev_labeling_flow = dev_labeling_ops()