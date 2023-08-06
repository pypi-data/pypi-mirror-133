"""
Our app setting
"""

# Alliance Auth (External Libs)
from app_utils.django import clean_setting

# Name of this app, as shown in the Auth sidebar and page titles
CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG = clean_setting(
    "CELERYANALYTICS_HOUSEKEEPING_DB_BACKLOG", 10, required_type=int
)
