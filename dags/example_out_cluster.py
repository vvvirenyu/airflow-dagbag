"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""

from datetime import datetime, timedelta

from airflow import configuration
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
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
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('out-cluster', default_args=default_args, schedule_interval=None)

# namespace = configuration.conf.get("kubernetes","namespace")
# config_file="/opt/airflow/.kube/config/out-config",
namespace = "nautilus-airflow"

t3 = KubernetesPodOperator(
    namespace=namespace,
    image="alpine/k8s:1.20.7",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo3",
    in_cluster=True,
    task_id="echo3",
    is_delete_operator_pod=False,
    dag=dag
)

t4 = KubernetesPodOperator(
    namespace=namespace,
    image="alpine/k8s:1.20.7",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo4",
    in_cluster=False,
    cluster_context="human-torch",
    task_id="echo4",
    is_delete_operator_pod=False,
    dag=dag
)




t5 = KubernetesPodOperator(
    namespace=namespace,
    image="alpine/k8s:1.20.7",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo5",
    in_cluster=False,
    cluster_context="human-torch",
    config_file="/home/airflow/.kube/config",
    task_id="echo5",
    is_delete_operator_pod=False,
    dag=dag
)

t6 = KubernetesPodOperator(
    namespace=namespace,
    image="alpine/k8s:1.20.7",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo6",
    in_cluster=False,
    cluster_context="james-howlett",
    task_id="echo6",
    is_delete_operator_pod=False,
    dag=dag
)



t7 = KubernetesPodOperator(
    namespace=namespace,
    image="alpine/k8s:1.20.7",
    cmds=["bash", "-cx"],
    arguments=["echo $(helm version --client --short)"],
    name="echo7",
    in_cluster=False,
    cluster_context="james-howlett",
    config_file="/home/airflow/.kube/config",
    task_id="echo7",
    is_delete_operator_pod=False,
    dag=dag
)

t3 >> [t4, t5, t6, t7]
