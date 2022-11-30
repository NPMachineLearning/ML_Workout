from airflow.decorators import task
from airflow.exceptions import AirflowException
from paramiko.client import SSHClient
import paramiko
import csv

# write csv file to sftp
@task(task_id="write_csv_to_sftp")
def write_csv_to_sftp(csv_data, filename, host_name, user_name, user_password):
    # create a ssh client for sftp server
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:                       
        # connect ssh client to sftp server 
        client.connect(host_name, username=user_name, password=user_password)

        # create a session
        session = client.open_sftp()

        # go to upload folder in sftp server
        session.chdir("upload")

        # create a file in sftp server and write data into file and save
        with session.open(filename, mode="w") as f:
            writer = csv.writer(f, delimiter=",")
            for line in csv_data.iter_lines():
                writer.writerow(line.decode("utf-8").split(","))

        # close session and client        
        session.close()
        client.close()
    except Exception as e:
        client.close()
        print(e)
        raise AirflowException(e)
