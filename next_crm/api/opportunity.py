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
