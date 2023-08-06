# Alliance Auth Celery Analytics Housekeeping
Housekeeping for Alliance Auth Celery Analytics

```shell
pip install allianceauth-celeryanalytics-housekeeping
```

In `local.py` add `celeryanalytics_housekeeping` to your `INSTALLED_APPS`.

Also add the following:

```python
## AA Celery Analytics Housekeeping
if (
    "celeryanalytics" in INSTALLED_APPS
    and "celeryanalytics_housekeeping" in INSTALLED_APPS
):
    # Keep 10 days (default)
    CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG = 10

    # Run every hour
    CELERYBEAT_SCHEDULE["celeryanalytics_housekeeping.tasks.run_housekeeping"] = {
        "task": "celeryanalytics_housekeeping.tasks.run_housekeeping",
        "schedule": crontab(minute=0, hour=0),
    }
```
