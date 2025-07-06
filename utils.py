# utils.py

from bs4 import BeautifulSoup

def extract_forms(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        name = input_tag.attrs.get("name")
        value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": name, "value": value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details
