# allianceauth-celeryanalytics-housekeeping
Housekeeping for Alliance Auth Celery Analytics

```python
## AA Celery Analytics Housekeeping
# Keep 10 days (default)
CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG = 10

# Run every hour
CELERYBEAT_SCHEDULE["celeryanalytics_housekeeping.tasks.run_housekeeping"] = {
    "task": "celeryanalytics_housekeeping.tasks.run_housekeeping",
    "schedule": crontab(minute=0, hour="*/1"),
}
```
