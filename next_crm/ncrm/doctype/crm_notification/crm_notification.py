# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CRMNotification(Document):
    def on_update(self):
        frappe.publish_realtime("crm_notification")

    @staticmethod
    def clear_old_logs(days=15):
        from frappe.query_builder import Interval
        from frappe.query_builder.functions import Now

        table = frappe.qb.DocType("CRM Notification")
        frappe.db.delete(
            table, filters={"modified": ("<", (Now() - Interval(days=days))), "read": 1}
        )


def notify_user(args):
    """
    Notify the assigned user
    """
    args = frappe._dict(args)
    if args.owner == args.assigned_to:
        return

    values = frappe._dict(
        doctype="CRM Notification",
        from_user=args.owner,
        to_user=args.assigned_to,
        type=args.notification_type,
        message=args.message,
        notification_text=args.notification_text,
        notification_type_doctype=args.reference_doctype,
        notification_type_doc=args.reference_docname,
        reference_doctype=args.redirect_to_doctype,
        reference_name=args.redirect_to_docname,
    )

    if frappe.db.exists("CRM Notification", values):
        return
    frappe.get_doc(values).insert(ignore_permissions=True)
