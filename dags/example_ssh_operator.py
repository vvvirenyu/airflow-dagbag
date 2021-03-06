from datetime import datetime, timedelta

from airflow import configuration
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.sftp_operator import SFTPOperator
from airflow.models import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(days=30),
}

dag = DAG('example_ssh_operator', default_args=default_args, schedule_interval=None)

# config_private_key = "{{ dag_run.conf['private_key'] }}"
# config_private_key_passphrase = "{{ dag_run.conf['private_key_passphrase'] }}"
# config_no_host_key_check = "{{ dag_run.conf['no_host_key_check'] }}"
# config_key_file = "{{ dag_run.conf['key_file'] }}"
# config_username = "{{ dag_run.conf['username'] }}"
# config_remote_host = "{{ dag_run.conf['remote_host'] }}"

ssh_hook_example = SSHHook(ssh_conn_id = "airflow_ui_conn")

remote_task = SSHOperator(
    task_id = "remote_task",
    ssh_hook = ssh_hook_example,
    dag = dag,
    command = 'kubectl get pods -A && sleep 30'
)

copy_file_task = SFTPOperator(
    task_id = "copy_file_task",
    ssh_hook = ssh_hook_example,
    local_filepath = '/opt/airflow/.kube/config',
    remote_filepath = '/home/sdpadmin/Desktop/config',
    operation="put",
    dag = dag

)

remote_task >> copy_file_task