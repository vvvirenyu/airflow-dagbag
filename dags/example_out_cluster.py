"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""

from datetime import datetime, timedelta

from airflow import configuration
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
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

dag = DAG('out-cluster', default_args=default_args, schedule_interval=None)

# namespace = configuration.conf.get("kubernetes","namespace")
# config_file="/opt/airflow/.kube/config/out-config",
namespace = "nautilus-airflow"
dummyNamespace = "nautilus-airflow-dummy"
echo_helm = "echo $(helm version --client --short); sleep 5"
install_helm = "helm install example2 helloworld-1.0.0.tgz -n nautilus-airflow"

t3 = KubernetesPodOperator(
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

t4 = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["/bin/bash", "-cx"],
    arguments=[echo_helm],
    name="echo4",
    in_cluster=False,
    cluster_context="slapstick",
    config_file="/opt/airflow/.kube/config",
    task_id="echo4",
    is_delete_operator_pod=False,
    service_account_name="default",
    get_logs=True,
    dag=dag
)

# t66 = KubernetesPodOperator(
#     namespace=namespace,
#     image="vvvirenyu/k8py:latest",
#     image_pull_secrets="regcred",
#     cmds=["/bin/bash", "-cx"],
#     arguments=[echo_helm],
#     name="echo66",
#     in_cluster=False,
#     cluster_context="sebastian-shaw",
#     config_file="/opt/airflow/.kube/config",
#     task_id="echo66",
#     service_account_name="default",
#     is_delete_operator_pod=False,
#     get_logs=True,
#     dag=dag
# )


t44 = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["/bin/bash", "-cx"],
    arguments=[echo_helm],
    name="echo44",
    in_cluster=False,
    cluster_context="slapstick",
    config_file="/opt/airflow/.kube/config",
    task_id="echo44",
    service_account_name="airflow-release-worker",
    is_delete_operator_pod=False,
    get_logs=True,
    dag=dag
)

# t55 = KubernetesPodOperator(
#     namespace=namespace,
#     image="vvvirenyu/k8py:latest",
#     image_pull_secrets="regcred",
#     cmds=["/bin/bash", "-cx"],
#     arguments=[echo_helm],
#     name="echo55",
#     in_cluster=False,
#     cluster_context="sebastian-shaw",
#     config_file="/opt/airflow/.kube/config",
#     task_id="echo55",
#     service_account_name="airflow-release-worker",
#     is_delete_operator_pod=False,
#     get_logs=True,
#     dag=dag
# )




t5 = KubernetesPodOperator(
    namespace=namespace,
    image="devops-repo.isus.emc.com:8116/nautilus/nautilus-kubectl:1.16.12",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo5",
    in_cluster=False,
    cluster_context="slapstick",
    config_file="/opt/airflow/.kube/config",
    task_id="echo5",
    is_delete_operator_pod=False,
    service_account_name="default",
    dag=dag
)

t6 = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo6",
    in_cluster=False,
    task_id="echo6",
    is_delete_operator_pod=False,
    service_account_name="airflow-release-worker",
    cluster_context="slapstick",
    config_file="/opt/airflow/.kube/config",
    get_logs=True,
    dag=dag
)



t7 = KubernetesPodOperator(
    namespace=namespace,
    image="devops-repo.isus.emc.com:8116/nautilus/nautilus-kubectl:1.16.12",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo7",
    in_cluster=False,
    task_id="echo7",
    is_delete_operator_pod=False,
    config_file="/home/virentu/.kube/config",
    get_logs=True,
    cluster_context="slapstick",
    service_account_name="default",
    dag=dag
)


t9 = KubernetesPodOperator(
    namespace=namespace,
    image="vvvirenyu/k8py:latest",
    image_pull_secrets="regcred",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo9",
    in_cluster=False,
    cluster_context="slapstick",
    config_file="/opt/airflow/.kube/config",
    task_id="echo9",
    is_delete_operator_pod=False,
    get_logs=True,
    service_account_name="airflow-release-worker",
    dag=dag
# )

t3 >> [t4, t44, t5, t6, t7, t9]