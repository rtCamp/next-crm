import frappe


def delete_attachments_from_crm_notes(doctype, docname):
    """
    Removes all files attached in custom_note_attachments from CRM Notes
    linked to the given parent document (e.g., Opportunity or Lead),
    and deletes the corresponding File documents.

    Args:
        doctype (str): The parent doctype (e.g., "Opportunity")
        docname (str): The name of the parent doc (e.g., "OPTY-0001")
    """
    file_names_to_delete = set()

    notes = frappe.get_all(
        "CRM Note", filters={"parenttype": doctype, "parent": docname}, fields=["name"]
    )

    for note in notes:
        note_doc = frappe.get_doc("CRM Note", note.name)

        for row in note_doc.custom_note_attachments:
            if row.filename:
                file_names_to_delete.add(row.filename)

        note_doc.set("custom_note_attachments", [])
        note_doc.save()

    for file_name in file_names_to_delete:
        try:
            frappe.delete_doc("File", file_name)
        except frappe.LinkExistsError:
            frappe.log_error(
                f"File {file_name} still linked to another document",
                "File Deletion Warning",
            )
        except Exception as e:
            frappe.log_error(
                f"Failed to delete file {file_name}: {e}", "File Deletion Error"
            )
