import frappe

from next_crm.api.comment import notify_mentions


def on_update(doc, method=None):
    module = frappe.get_meta(doc.reference_doctype).module
    if (
        module == "NCRM"
        or module == "CRM"
        or doc.reference_doctype in ["Address", "Contact"]
    ):
        notify_mentions(doc)
