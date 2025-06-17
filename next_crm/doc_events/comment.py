from next_crm.api.comment import notify_mentions


def on_update(doc, method=None):
    allowed_doctypes = [
        "ToDo",
        "Opportunity",
        "Lead",
        "Prospect",
        "Customer",
        "Address",
        "Contact",
    ]
    if doc.reference_doctype in allowed_doctypes:
        notify_mentions(doc)
