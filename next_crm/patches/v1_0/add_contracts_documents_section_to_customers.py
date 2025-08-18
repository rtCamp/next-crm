import json

import frappe


def execute():
    if not frappe.db.exists("CRM Fields Layout", "Customer-Side Panel"):
        return

    contracts_documents_section = {
        "label": "Contracts and Documents",
        "name": "contracts_documents",
        "opened": True,
        "fields": [
            "custom_msa_start_date",
            "custom_msa_end_date",
            "custom_msa_document_link",
            "custom_insurance_requested",
            "custom_insurance_start_date",
            "custom_insurance_end_date",
            "custom_insurance_document_link",
            "custom_contract_start_date",
            "custom_contract_end_date",
        ],
    }

    docpanel = frappe.get_doc("CRM Fields Layout", "Customer-Side Panel")
    parsed_layout = json.loads(docpanel.layout)
    if not any(item.get("name") == "contracts_documents" for item in parsed_layout):
        parsed_layout.append(contracts_documents_section)
    docpanel.layout = json.dumps(parsed_layout)
    docpanel.save()
