# pip install google-cloud-monitoring

from google.cloud import monitoring_v3
from google.protobuf import field_mask_pb2 as field_mask

def enable_alert_policies(project_name='projects/tenacious-post-355715', enable=False, filter_=None):
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

# adding in filter policy id doesn't work
# enable_alert_policies(project_name='projects/tenacious-post-355715', enable=False, filter_="419697551138669198")
# enable_alert_policies(project_name='projects/tenacious-post-355715', enable=True, filter_="/alertPolicies/419697551138669198")

# working version
# enable_alert_policies(project_name='projects/tenacious-post-355715', enable=False)

enable_alert_policies()
