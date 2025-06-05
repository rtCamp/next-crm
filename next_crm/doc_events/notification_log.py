import re
import urllib.parse

import frappe
from frappe.utils.data import get_url_to_form

PATH_REPLACEMENTS = {
    r"^/app/lead/": "/next-crm/leads/",
    r"^/app/opportunity/": "/next-crm/opportunities/",
}

# also need to replace the # in the url (#comment-l51lc9ntpa => #comments)

FRAGMENT_REPLACEMENTS = {
    r"^comment-(\w+)": "comments",
}


def before_save(doc, method):
    if not doc.link:
        update_note_link(doc)

    if not doc.link:
        return
    url = urllib.parse.urlparse(doc.link)
    path = url.path
    for old_path, new_path in PATH_REPLACEMENTS.items():
        if re.search(old_path, path):
            path = re.sub(old_path, new_path, path)
            break
    fragment = url.fragment
    for old_fragment, new_fragment in FRAGMENT_REPLACEMENTS.items():
        if re.search(old_fragment, fragment):
            fragment = re.sub(old_fragment, new_fragment, fragment)
            break
    doc.link = url._replace(path=path, fragment=fragment).geturl()


def update_note_link(doc):
    """
    There is no direct link between the note and the notification log.
    We determine the note id by using the content of the email and the most recently created note, as the note is created before the notification log.
    """
    if not doc.document_type and not doc.document_name:
        return
    notes = frappe.get_all(
        "CRM Note",
        filters={
            "parenttype": doc.document_type,
            "parent": doc.document_name,
        },
        fields=["name", "note"],
        order_by="creation desc",
        limit_page_length=5,
    )

    note_name = None

    for note in notes:
        if note.note in doc.email_content:
            note_name = note.name
            break

    if note_name:
        doc.link = get_url_to_form(doc.document_type, doc.document_name)
