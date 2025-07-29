import datetime

import frappe
import frappe.client
import pytz


@frappe.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
    if not frappe.conf.developer_mode:
        frappe.throw("This method is only meant for developer mode")
    return get_boot()


def get_boot():
    return frappe._dict(
        {
            "frappe_version": frappe.__version__,
            "default_route": get_default_route(),
            "site_name": frappe.local.site,
            "read_only_mode": frappe.flags.read_only,
            "csrf_token": frappe.sessions.get_csrf_token(),
            "server_timezone": frappe.client.get_time_zone().get("time_zone", None),
            "server_timezone_offset": get_server_timezone_offset(),
        }
    )


def get_server_timezone_offset():
    timezone_str = frappe.client.get_time_zone().get("time_zone", "UTC")

    # Get current time in that timezone
    tz = pytz.timezone(timezone_str)
    now = datetime.datetime.now(tz)

    # Get UTC offset as a timedelta
    offset = now.utcoffset()

    # Format timedelta to "+HH:MM" or "-HH:MM"
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    hours, minutes = divmod(abs(total_minutes), 60)
    return f"{sign}{hours:02}:{minutes:02}"


def get_default_route():
    return "/next-crm"
