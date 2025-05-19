import json

import frappe
from frappe.utils import update_progress_bar


def execute():
    # Get all CRM View Settings documents
    crm_view_settings_list = frappe.get_all(
        "CRM View Settings", fields=["name", "filters"]
    )
    total_settings = len(crm_view_settings_list)
    for index, setting in enumerate(crm_view_settings_list):
        name = setting.name
        filters_str = setting.filters

        if not filters_str or filters_str == "{}":
            update_progress_bar("Updating CRM Views filters", index, total_settings)
            continue

        try:
            filters = json.loads(filters_str)
        except Exception as e:
            frappe.log_error(
                f"Failed to parse filters JSON in CRM View Settings {name}: {e}"
            )
            update_progress_bar("Updating CRM Views filters", index, total_settings)
            continue

        # Iterate through filters keys
        for key, val in filters.items():
            # Check if val is a list with operator "in"
            if isinstance(val, list) and len(val) == 2 and val[0] == "in":
                raw_values = val[1]

                # Convert comma separated string to list, if necessary
                if isinstance(raw_values, str):
                    # Split by comma, strip spaces
                    values_list = [v.strip() for v in raw_values.split(",")]
                elif isinstance(raw_values, list):
                    values_list = raw_values
                else:
                    # Unexpected format, skip
                    update_progress_bar(
                        "Updating CRM Views filters", index, total_settings
                    )
                    continue

                # Update filter with corrected list
                filters[key] = ["in", values_list]

            # Save the updated filters back as JSON string
            frappe.db.set_value(
                "CRM View Settings", name, "filters", json.dumps(filters)
            )
        update_progress_bar("Updating CRM Views filters", index, total_settings)
