def execute():
    from frappe import enqueue

    enqueue(
        update_won_date,
        queue="long",
        timeout=3600,
        enqueue_after_commit=True,
    )


def update_won_date():
    from frappe import db, get_all
    from frappe.utils import getdate, update_progress_bar

    opportunity_list = get_all(
        "Opportunity",
        filters={"custom_won_date": ["is", "not set"], "status": "Won"},
        pluck="name",
    )
    count = len(opportunity_list)

    for index, opportunity in enumerate(opportunity_list):
        d = db.get_value(
            "CRM Status Change Log",
            {"to": "Won", "parent": opportunity, "to_date": ["is", "set"]},
            "to_date",
        )
        if not d:
            update_progress_bar("Updating Won Date", index, count)
            continue
        db.set_value(
            "Opportunity",
            opportunity,
            "custom_won_date",
            getdate(d),
            update_modified=False,
        )
        update_progress_bar("Updating Won Date", index, count)
