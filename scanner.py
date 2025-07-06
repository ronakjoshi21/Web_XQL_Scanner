# scanner.py

import requests
from urllib.parse import urljoin
from payloads import SQLI_PAYLOADS, XSS_PAYLOADS
from utils import extract_forms, get_form_details

def test_payloads(url, form, payloads, vuln_type):
    is_vulnerable = False
    for payload in payloads:
        data = {}
        for input in form["inputs"]:
            if input["type"] == "text" or input["type"] == "search":
                data[input["name"]] = payload
            else:
                data[input["name"]] = input["value"]

        target_url = urljoin(url, form["action"])
        try:
            if form["method"] == "post":
                response = requests.post(target_url, data=data)
            else:
                response = requests.get(target_url, params=data)

            if payload in response.text:
                print(f"[!] {vuln_type} Vulnerability detected with payload: {payload}")
                is_vulnerable = True
        except Exception as e:
            print(f"[Error while testing {vuln_type}] {e}")
    return is_vulnerable

def scan_url(url):
    print(f"\n[+] Scanning: {url}")
    vulnerabilities_found = False

    try:
        response = requests.get(url)
        forms = extract_forms(response.text)
        print(f"[+] Found {len(forms)} form(s)\n")

        for i, form in enumerate(forms):
            form_details = get_form_details(form)
            print(f"--- Testing form #{i+1} ---")
            
            print("[*] Testing SQL Injection...")
            if test_payloads(url, form_details, SQLI_PAYLOADS, "SQL Injection"):
                print("[!!] SQL Injection vulnerability found\n")
                vulnerabilities_found = True
            else:
                print("[OK] No SQL Injection vulnerability detected\n")
            
            print("[*] Testing XSS...")
            if test_payloads(url, form_details, XSS_PAYLOADS, "XSS"):
                print("[!!] XSS vulnerability found\n")
                vulnerabilities_found = True
            else:
                print("[OK] No XSS vulnerability detected\n")

        print("=== Scan Summary ===")
        if vulnerabilities_found:
            print("⚠️  One or more vulnerabilities were detected.")
        else:
            print("✅ Scan complete. No SQLi or XSS vulnerabilities detected.")

    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    target = input("Enter URL to scan: ").strip()
    scan_url(target)
