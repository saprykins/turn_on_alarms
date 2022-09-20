import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
import requests
import json
from google.cloud import monitoring_v3
from google.protobuf import field_mask_pb2 as field_mask


def enable_alert_policies(project_name='projects/tenacious-post-355715', enable=True, filter_=None):
    """Enable or disable alert policies in a project.

    Arguments:
        project_name (str): The Google Cloud Project to use. The project name
            must be in the format - 'projects/<PROJECT_NAME>'.
        enable (bool): Enable or disable the policies.
        filter_ (str, optional): Only enable/disable alert policies that match
            this filter_.  See
            https://cloud.google.com/monitoring/api/v3/sorting-and-filtering
        
        enable = True // means enable the policy
        enable = False // means disable

    """

    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(
        # policies includes all policies
        request={"name": project_name, "filter": filter_}
    )

    # print(policies)

    for policy in policies:
        if bool(enable) == policy.enabled:
            print(
                "Policy",
                policy.name,
                "is already",
                "enabled" if policy.enabled else "disabled",
            )
        else:
            policy.enabled = bool(enable)
            mask = field_mask.FieldMask()
            mask.paths.append("enabled")
            
            #
            # policy = "/alertPolicies/419697551138669198"
            #
            
            client.update_alert_policy(alert_policy=policy, update_mask=mask)
            # print("Enabled" if enable else "Disabled", policy.name)


default_args = {
    'owner': 'airflow',    
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    #'email': ['airflow@example.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retries': 1,
    'retry_delay': timedelta(minutes=5),
    }


dag_python = DAG(
	dag_id = "enable_alerts",
	default_args=default_args,
	schedule_interval='0 6 * * 1,2,3,4,5',
	# schedule_interval='@daily',
	dagrun_timeout=timedelta(minutes=60),
	description='use case of python operator in airflow',
	start_date = airflow.utils.dates.days_ago(1),

    # yesturday = airflow.utils.dates.days_ago(1),
    # start_date = airflow.utils.dates.days_ago(1).replace(hour=20, minute=30)
    )

power_on_alerts = PythonOperator(
    task_id='alerts_enabled', 
    python_callable=enable_alert_policies, 
    dag=dag_python
    )


power_on_alerts
