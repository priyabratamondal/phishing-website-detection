import re
import tldextract
from urllib.parse import urlparse

def extract_features(url: str) -> dict:
    extracted = tldextract.extract(url)
    domain = extracted.domain
    subdomain = extracted.subdomain

    return {
        "SSLfinal_State": 1 if url.lower().startswith("https") else -1,
        "URL_of_Anchor": 0,
        "Prefix_Suffix": 1 if "-" in domain else -1,
        "web_traffic": 0,
        "having_Sub_Domain": 1 if subdomain else -1,
        "Request_URL": -1,
        "Links_in_tags": 0,
        "SFH": 0,
        "Google_Index": 1,
        "age_of_domain": -1,
        "Page_Rank": 1,
        "having_IP_Address": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else -1,
        "Statistical_report": -1,
        "DNSRecord": 1,
        "URL_Length": 1 if len(url) < 54 else 0 if len(url) <= 75 else -1,
        "having_At_Symbol": 1 if "@" in url else -1,
        "on_mouseover": 1,
        "port": 1 if urlparse(url).port in [80, 443, None] else -1,
        "Links_pointing_to_page": 0,
        "Redirect": 0,
        "double_slash_redirecting": 1 if url.count("//") > 1 else -1,
        "HTTPS_token": 1 if url.lower().startswith("https") else -1,
        "Abnormal_URL": 1 if domain not in url else -1,
        "Shortining_Service": 1 if any(shortener in url.lower() for shortener in ["bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co"]) else -1,
        "Domain_registeration_length": -1,
    }
