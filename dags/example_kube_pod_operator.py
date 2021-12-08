"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""

from datetime import datetime, timedelta

from airflow import configuration
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(days=30),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('example_kube_pod_operator', default_args=default_args, schedule_interval=None)

namespace = "nautilus-airflow"
echo_helm = "echo $(helm version --client --short); sleep 2"


ubuntu_image_task = KubernetesPodOperator(
    namespace=namespace,
    image="ubuntu:16.04",
    cmds=["bash", "-cx"],
    arguments=["echo", "Hello world"],
    name="echo",
    in_cluster=True,
    task_id="echo",
    is_delete_operator_pod=True,
    dag=dag
)

rhel_image_task = KubernetesPodOperator(
    namespace=namespace,
    image="registry.access.redhat.com/rhscl/python-36-rhel7",
    cmds=["bash", "-cx"],
    arguments=["echo", "Hello world"],
    name="python-version",
    in_cluster=True,
    task_id="pythonversion",
    is_delete_operator_pod=True,
    dag=dag
)


incluster_task = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["/bin/bash", "-cx"],
    arguments=[echo_helm],
    name="echo3",
    in_cluster=True,
    task_id="echo3",
    is_delete_operator_pod=False,
    service_account_name="default",
    get_logs=True,
    dag=dag
)


outcluster_task = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["/bin/bash", "-cx"],
    arguments=[echo_helm],
    name="echo66",
    in_cluster=False,
    cluster_context="cerebro",
    config_file="/opt/airflow/.kube/config",
    task_id="echo66",
    service_account_name="default",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

[ubuntu_image_task, rhel_image_task, incluster_task, outcluster_task]