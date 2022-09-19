# turn_on_alarms

gcloud activate / deactivate was OK in Sandbox:  

Activate:  
```
gcloud alpha monitoring policies update projects/tenacious-post-355715/alertPolicies/419697551138669198 --enabled
```
De-activate:  
```
gcloud alpha monitoring policies update projects/tenacious-post-355715/alertPolicies/419697551138669198 --no-enabled
```

In python didn't work
```
pip install google-cloud-monitoring
```
