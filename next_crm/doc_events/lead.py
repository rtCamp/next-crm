from next_crm.doc_events.utils import delete_attachments_from_crm_notes


def on_update(doc, method=None):
    if not doc.title and doc.name:
        doc.db_set("title", doc.name)


def on_trash(doc, method=None):
    delete_attachments_from_crm_notes(doc.doctype, doc.name)
