import frappe
from pypika import Criterion


@frappe.whitelist()
def get_views(doctype):
    View = frappe.qb.DocType("CRM View Settings")
    query = (
        frappe.qb.from_(View)
        .select("*")
        .where(Criterion.any([View.user == "", View.user == frappe.session.user]))
    )
    if doctype:
        query = query.where(View.dt == doctype)
    views = query.run(as_dict=True)
    return views


@frappe.whitelist()
def get_default_open_view():

    views = frappe.get_all(
        "CRM View Settings",
        fields=["dt", "type", "user", "is_default", "default_open_view"],
        filters={
            "user": frappe.session.user,
            "default_open_view": 1,
            "is_default": 1,
            "dt": ["is", "set"],
        },
    )

    default_view_object = {}
    for view in views:
        default_view_object[view.dt] = view.type

    if not default_view_object.get("Lead"):
        default_view_object["Lead"] = frappe.db.get_single_value(
            "NCRM Settings", "lead_view"
        )

    if not default_view_object.get("Opportunity"):
        default_view_object["Opportunity"] = frappe.db.get_single_value(
            "NCRM Settings", "opportunity_view"
        )

    return default_view_object
