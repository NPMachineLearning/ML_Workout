from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import requests

default_args = {
    "owner": "airflow",
}

# project id from label-studio
LABEL_STUDIO_PROJECT_ID = 2
LABEL_STUDIO_URL = "http://label-studio:8080"
LABEL_STUDIO_TOKEN = "8823cc4fb910406253548fac3c458e495d6de86c"

@task(task_id="sync_import_storage")
def sync_import_storage():
    # get all import storage information for the project
    response = requests.get(
        f"{LABEL_STUDIO_URL}/api/storages/localfiles",
        params={"project": LABEL_STUDIO_PROJECT_ID},
        headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})
    print(response.json())

    # sync all import storage
    for import_storage in response.json():
        id = import_storage["id"]
        response = requests.post(
                                f"{LABEL_STUDIO_URL}/api/storages/localfiles/{id}/sync",
                                params={"project": LABEL_STUDIO_PROJECT_ID},
                                headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})
        print(response.json())

@task(task_id="sync_export_storage")
def sync_export_storage():
    # get all export storage for the project
    response = requests.get(
        f"{LABEL_STUDIO_URL}/api/storages/export/localfiles",
        params={"project": LABEL_STUDIO_PROJECT_ID},
        headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})
    print(response.json())

    # sync all export storage
    for export_storage in response.json():
        id = export_storage["id"]
        response = requests.post(
                                f"{LABEL_STUDIO_URL}/api/storages/export/localfiles/{id}/sync",
                                params={"project": LABEL_STUDIO_PROJECT_ID},
                                headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})
        print(response.text)

@dag(
    dag_id = "DevLabelStudioStorageSync",
    description = "Labeling flow",
    default_args = default_args,
    schedule=None,
    start_date=days_ago(2),
    tags=["dev", "labeling", "flow"],
)
def dev_labeling_ops():
    sync_import_storage()
    sync_export_storage()

dev_labeling_flow = dev_labeling_ops()