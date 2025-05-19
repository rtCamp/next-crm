import re
import urllib.parse

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
