
"""
This is an example dag for using the Kubernetes Executor.
"""
import os
from datetime import datetime

from airflow import DAG
from airflow.example_dags.libs.helper import print_stuff
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='example_update_worker_pod_specs',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example', 'example2'],
) as dag:
    affinity = {
        'podAntiAffinity': {
            'requiredDuringSchedulingIgnoredDuringExecution': [
                {
                    'topologyKey': 'kubernetes.io/hostname',
                    'labelSelector': {
                        'matchExpressions': [{'key': 'app', 'operator': 'In', 'values': ['airflow']}]
                    },
                }
            ]
        }
    }

    tolerations = [{'key': 'dedicated', 'operator': 'Equal', 'value': 'airflow'}]


    start_task = PythonOperator(task_id="start_task", python_callable=print_stuff)

    change_worker_pod_airflow_tag = PythonOperator(
        task_id="one_task",
        python_callable=print_stuff,
        executor_config={"KubernetesExecutor": {"image": "apache/airflow:2.2.0-python3.9"}},
    )

    # Limit resources on this operator/task with node affinity & tolerations
    change_worker_pod_resource_specs = PythonOperator(
        task_id="two_task",
        python_callable=print_stuff,
        executor_config={
            "KubernetesExecutor": {
                "request_memory": "128Mi",
                "limit_memory": "128Mi",
                "tolerations": tolerations,
                "affinity": affinity,
            }
        },
    )

    # Add arbitrary labels to worker pods
    add_worker_pod_label = PythonOperator(
        task_id="three_task",
        python_callable=print_stuff,
        executor_config={"KubernetesExecutor": {"labels": {"foo": "bar"}}},
    )

    start_task >> [change_worker_pod_airflow_tag, change_worker_pod_resource_specs, add_worker_pod_label]