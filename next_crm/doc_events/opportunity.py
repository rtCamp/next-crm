import frappe

from next_crm.doc_events.utils import delete_attachments_from_crm_notes


def before_save(doc, method=None):
    current_status = frappe.db.get_value("Opportunity", doc.name, "status")
    current_stage = frappe.db.get_value("Opportunity", doc.name, "sales_stage")
    if not current_status and not current_stage:
        return

    from next_crm.api.opportunity import create_checklist

    if doc.status != current_status:
        create_checklist(doc.name, field="status", value=doc.status)
    if doc.sales_stage != current_stage:
        create_checklist(doc.name, field="sales_stage", value=doc.sales_stage)


def on_trash(doc, method=None):
    frappe.db.delete("Prospect Opportunity", filters={"opportunity": doc.name})
    frappe.db.delete(
        "Dynamic Link",
        filters={"link_name": doc.name, "parenttype": ["in", ["Contact", "Address"]]},
    )
    delete_linked_event(doc.name)
    frappe.db.delete("CRM Notification", {"reference_name": doc.name})
    if "frappe_gmail_thread" in frappe.get_installed_apps():
        unlink_gmail_thread(doc.name)
    delete_attachments_from_crm_notes(doc.doctype, doc.name)


def delete_linked_event(docname):
    event_part = frappe.qb.DocType("Event Participants")
    event_participants_query = (
        frappe.qb.from_(event_part)
        .where(event_part.reference_doctype == "Opportunity")
        .where(event_part.reference_docname == docname)
        .select(event_part.parent)
    )

    event = frappe.qb.DocType("Event")
    event_delete_query = (
        frappe.qb.from_(event)
        .where(event.name.isin(event_participants_query))
        .delete()
        .get_sql()
    )

    event_participants_delete_query = (
        frappe.qb.from_(event_part)
        .where(event_part.parent.isin(event_participants_query))
        .delete()
        .get_sql()
    )

    frappe.db.sql(event_delete_query)
    frappe.db.sql(event_participants_delete_query)


def unlink_gmail_thread(docname):
    gmail_thread = frappe.qb.DocType("Gmail Thread")

    query = (
        frappe.qb.update(gmail_thread)
        .set(gmail_thread.reference_doctype, None)
        .set(gmail_thread.reference_name, None)
        .set(gmail_thread.status, "Open")
        .where(gmail_thread.reference_doctype == "Opportunity")
        .where(gmail_thread.reference_name == docname)
        .get_sql()
    )

    frappe.db.sql(query)
