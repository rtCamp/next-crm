from datetime import datetime

from frappe.utils import get_datetime


def get_duration(from_date, to_date):
    if not isinstance(from_date, datetime):
        from_date = get_datetime(from_date)
    if not isinstance(to_date, datetime):
        to_date = get_datetime(to_date)
    duration = to_date - from_date
    return duration.total_seconds()
