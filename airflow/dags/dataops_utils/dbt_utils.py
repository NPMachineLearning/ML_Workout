from airflow.decorators import task
from airflow.exceptions import AirflowException
import requests
import uuid

DBT_RPC_SERVER_URL = "http://DBTServer:8580/jsonrpc"

# return dbt rpc server json data request for compile
# https://docs.getdbt.com/reference/commands/rpc#compile-a-project-docs
def dbt_compile_json():
    return {
                "jsonrpc": "2.0",
                "method": "compile",
                "id": str(uuid.uuid4()),
            }

# return dbt rpc server json data request for run
# https://docs.getdbt.com/reference/commands/rpc#run-models-docs
def dbt_run_json():
    return {
                "jsonrpc": "2.0",
                "method": "cli_args",
                "id": str(uuid.uuid4()),
                "params": {
                    "cli": "run --full-refresh",
                }
            }

# check if dbt response has an any error and
# raise exception
def check_dbt_response_error(response):
    res_json = response.json()
    if res_json.get("error") != None:
        code = res_json["error"]["code"]
        msg = res_json["error"]["message"]
        raise Exception(f"An error occured from dbt {code}, {msg}")

# task that trigger dbt data transformation
# through dbt rpc server
@task(task_id="dbt_transforms")
def dbt_transforms():
    try:
        # compile dbt model
        response = requests.post(DBT_RPC_SERVER_URL, json=dbt_compile_json())
        check_dbt_response_error(response)

        # run dbt model
        response = requests.post(DBT_RPC_SERVER_URL, json=dbt_run_json())
        check_dbt_response_error(response)

        return response
    except Exception as e:
        raise AirflowException(e)