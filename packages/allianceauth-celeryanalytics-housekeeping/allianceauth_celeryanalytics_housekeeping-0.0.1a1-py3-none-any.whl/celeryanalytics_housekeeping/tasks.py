# Third Party
from celery import shared_task

# Django
from django.apps import apps


@shared_task
def run_housekeeping():
    """
    Cleanup Database
    :return:
    """

    if apps.is_installed("celeryanalytics"):
        # Standard Library
        from datetime import datetime, timedelta

        # Third Party
        from celeryanalytics.models import CeleryTaskCompleted, CeleryTaskFailed

        # Django
        from django.db import transaction

        # Alliance Auth Celery Analytics Housekeeping
        from celeryanalytics_housekeeping.app_settings import (
            CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG,
        )

        with transaction.atomic():
            CeleryTaskCompleted.objects.filter(
                time__lte=datetime.now()
                - timedelta(days=CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG)
            ).delete()

        with transaction.atomic():
            CeleryTaskFailed.objects.filter(
                time__lte=datetime.now()
                - timedelta(days=CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG)
            ).delete()
