import frappe
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import (
    enqueue_create_notification,
    get_title_html,
)
from frappe.utils import now

from next_crm.ncrm.doctype.crm_notification.crm_notification import notify_user


@frappe.whitelist()
def create_note(doctype, docname, title=None, note=None, parent_note=None):
    """
    Create a new CRM Note.
    """
    if not note and not title:
        raise frappe.ValidationError("Either note or title is required.")

    new_note = frappe.get_doc(
        {
            "doctype": "CRM Note",
            "custom_title": title,
            "note": note,
            "parenttype": doctype,
            "parent": docname or "",
            "parentfield": "notes",
            "owner": frappe.session.user,
            "added_by": frappe.session.user,
            "added_on": now(),
            "custom_parent_note": parent_note,
        }
    )

    new_note.insert()
    notify_mentions_ncrm(note, new_note.name, docname, doctype)
    return new_note


@frappe.whitelist()
def update_note(doctype, docname, note_name, note=None):
    """
    Update a CRM Note.
    """
    if not note.get("custom_title") and not note.get("note"):
        raise frappe.ValidationError("Either note or title is required.")

    frappe.set_value("CRM Note", note_name, note)
    notify_mentions_ncrm(note.get("note"), note_name, docname, doctype)

    updated_doc = frappe.get_doc("CRM Note", note_name)
    return updated_doc


def notify_mentions_ncrm(note, note_name, docname, doctype):
    from frappe.desk.notifications import extract_mentions

    mentions = set(extract_mentions(note))

    if not mentions:
        return

    for mention in mentions:
        owner = frappe.get_cached_value("User", frappe.session.user, "full_name")
        title = frappe.db.get_value(doctype, {"name": docname}, "title")
        name = title or docname or None
        notification_text = f"""
        <div class="mb-2 leading-5 text-ink-gray-5">
            <span class="font-medium text-ink-gray-9">{ owner}</span>
            <span>{ _('mentioned you in a Note in {0}').format(doctype) }</span>
            <span class="font-medium text-ink-gray-9">{ name }</span>
        </div>
        """
        notify_user(
            {
                "owner": frappe.session.user,
                "assigned_to": mention,
                "notification_type": "Mention",
                "message": note,
                "notification_text": notification_text,
                "reference_doctype": "CRM Note",
                "reference_docname": note_name,
                "redirect_to_doctype": doctype,
                "redirect_to_docname": docname,
            }
        )

    email_notification_message = _(
        """[Next CRM] {0} mentioned you in a Note in {1} {2}"""
    ).format(frappe.bold(owner), frappe.bold(doctype), get_title_html(title))

    recipients = [
        frappe.db.get_value(
            "User",
            {
                "enabled": 1,
                "name": name,
                "user_type": "System User",
                "allowed_in_mentions": 1,
            },
            "email",
        )
        for name in mentions
    ]

    notification_doc = {
        "type": "Mention",
        "document_type": doctype,
        "document_name": docname,
        "subject": email_notification_message,
        "from_user": frappe.session.user,
        "email_content": note,
    }

    enqueue_create_notification(recipients, notification_doc)


@frappe.whitelist()
def delete_note(note_name):
    """
    Delete CRM Note.
    """
    note = frappe.get_doc("CRM Note", note_name)
    if not note:
        raise frappe.ValidationError(_("Note not found."))

    parent_note = note.custom_parent_note
    if not parent_note:
        child_notes = frappe.get_all(
            "CRM Note",
            filters={"custom_parent_note": note_name},
            fields=["name"],
            pluck="name",
        )
        for child_note in child_notes:
            frappe.db.delete("CRM Notification", {"notification_type_doc": child_note})
            frappe.delete_doc("CRM Note", child_note)

    frappe.db.delete("CRM Notification", {"notification_type_doc": note_name})
    note.delete()
    return True
