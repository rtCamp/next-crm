from datetime import datetime

import frappe
from frappe.utils import get_datetime


def get_duration(from_date, to_date):
    if not isinstance(from_date, datetime):
        from_date = get_datetime(from_date)
    if not isinstance(to_date, datetime):
        to_date = get_datetime(to_date)
    duration = to_date - from_date
    return duration.total_seconds()


def link_gmail_threads(doctype, docname, doc):
    gmail_thread_list = get_linked_gmail_thread_list(doctype, docname)

    for gmail_thread in gmail_thread_list:
        gmail_thread_doc = frappe.get_doc("Gmail Thread", gmail_thread)
        gmail_thread_doc.reference_doctype = doc.doctype
        gmail_thread_doc.reference_name = doc.name
        gmail_thread_doc.save()


def get_linked_gmail_thread_list(doctype, docname):
    gmail_threads = frappe.get_all(
        "Gmail Thread",
        filters={"reference_doctype": doctype, "reference_name": docname},
        pluck="name",
    )
    return gmail_threads
