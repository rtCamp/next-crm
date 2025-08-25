import frappe
from frappe import _

from next_crm.api.doc import get_assigned_users, get_fields_meta
from next_crm.ncrm.doctype.crm_form_script.crm_form_script import get_form_script


@frappe.whitelist()
def get_opportunity(name):
    opportunity = frappe.get_doc("Opportunity", name, for_update=False).as_dict()

    opportunity["doctype"] = "Opportunity"
    opportunity["fields_meta"] = get_fields_meta("Opportunity")
    opportunity["_form_script"] = get_form_script("Opportunity")
    opportunity["_assign"] = get_assigned_users("Opportunity", opportunity.name)
    hide_comments_tab = frappe.db.get_single_value("NCRM Settings", "hide_comments_tab")
    opportunity["hide_comments_tab"] = hide_comments_tab
    return opportunity


@frappe.whitelist()
def declare_enquiry_lost_api(
    name, lost_reasons_list, competitors, detailed_reason=None
):
    opportunity = frappe.get_doc("Opportunity", name)
    opportunity.declare_enquiry_lost(
        lost_reasons_list=lost_reasons_list,
        competitors=competitors,
        detailed_reason=detailed_reason,
    )
    return _("Opportunity updated successfully")


@frappe.whitelist()
def create_checklist(docname, status=None):
    if not status:
        return

    checklist_items = frappe.get_all(
        "Opportunity Status Checklist",
        filters={"parent": status, "parenttype": "CRM Deal Status"},
        fields=["checklist_item"],
        pluck="checklist_item",
    )

    if not checklist_items:
        return

    content = (
        '<div class="ql-editor read-mode"><ol>'
        + "".join(
            [
                f'<li data-list="unchecked"><span class="ql-ui" contenteditable="false"></span>{item}</li>'
                for item in checklist_items
            ]
        )
        + "</ol></div>"
    )

    opportunity_owner = (
        frappe.db.get_value("Opportunity", docname, "opportunity_owner")
        or frappe.session.user
    )

    todo = frappe.get_doc(
        {
            "doctype": "ToDo",
            "custom_title": _("Checklist for {0}").format(status),
            "description": content,
            "reference_type": "Opportunity",
            "reference_name": docname,
            "allocated_to": opportunity_owner,
        }
    )

    todo.insert()
    return todo.name
