def on_update(doc, method=None):
    if not doc.title and doc.name:
        doc.db_set("title", doc.name)
