from datetime import datetime, timedelta

from airflow import configuration
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks.ssh_hook import SSHHook
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

dag = DAG('ssh-operator', default_args=default_args, schedule_interval=None)

# config_private_key = "{{ dag_run.conf['private_key'] }}"
# config_private_key_passphrase = "{{ dag_run.conf['private_key_passphrase'] }}"
# config_no_host_key_check = "{{ dag_run.conf['no_host_key_check'] }}"

config_key_file = "{{ dag_run.conf['key_file'] }}"
config_username = "{{ dag_run.conf['username'] }}"
config_remote_host = "{{ dag_run.conf['remote_host'] }}"

ssh_hook_example = SSHHook(
    key_file = config_key_file,
    username = config_username,
    remote_host = config_remote_host
)

echo_world_task = SSHOperator(
    task_id = "echo world task",
    ssh_hook = ssh_hook_example,
    dag = dag,
    command = 'echo "Hello world!"'
)