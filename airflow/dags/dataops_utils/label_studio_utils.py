from airflow.decorators import task
from airflow.exceptions import AirflowException
from paramiko.client import SSHClient
import paramiko
import csv
import requests

# project id from label-studio
LABEL_STUDIO_PROJECT_ID = 2
LABEL_STUDIO_URL = "http://label-studio:8080"
LABEL_STUDIO_TOKEN = "8823cc4fb910406253548fac3c458e495d6de86c"
LABEL_STUDIO_DEFAULT_EXPORT_TYPE = "CSV"

# sync label studio import storage
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

# sync label studio export storage
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

# export annotation from label studio
@task(task_id="export_annotation")
def export_annotation(export_type=LABEL_STUDIO_DEFAULT_EXPORT_TYPE):
    # export csv from label-studio
    response = requests.get(
                            f"{LABEL_STUDIO_URL}/api/projects/2/export",
                            params={"export_type": export_type},
                            headers={"Authorization": f"Token {LABEL_STUDIO_TOKEN}"})

    return response