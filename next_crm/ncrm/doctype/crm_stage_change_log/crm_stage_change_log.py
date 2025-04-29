# Copyright (c) 2025, rtCamp and contributors
# For license information, please see license.txt

# import frappe

from frappe import session
from frappe.model.document import Document
from frappe.utils import get_datetime

from next_crm.utils import get_duration


class CRMStageChangeLog(Document):
    pass


def add_stage_change_log(doc):
    if not doc.is_new():
        previous_doc = doc.get_doc_before_save()

        if not previous_doc.custom_stage_change_log:
            previous_stage = previous_doc.sales_stage
            previous_time = previous_doc.modified
        else:
            previous_stage = previous_doc.custom_stage_change_log[-1].to
            previous_time = previous_doc.custom_stage_change_log[-1].to_date

        doc.append(
            "custom_stage_change_log",
            {
                "from": previous_stage,
                "to": doc.sales_stage,
                "from_date": previous_time,
                "to_date": get_datetime(),
                "log_owner": session.user,
                "duration": get_duration(previous_time, get_datetime()),
            },
        )
