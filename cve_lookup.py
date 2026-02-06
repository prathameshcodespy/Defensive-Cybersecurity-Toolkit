import requests

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_cves(keyword):
    try:
        params = {
            "keywordSearch": keyword,
            "resultsPerPage": 1
        }

        response = requests.get(NVD_API_URL, params=params, timeout=5)
        data = response.json()

        if "vulnerabilities" in data and data["vulnerabilities"]:
            cve = data["vulnerabilities"][0]["cve"]["id"]
            return cve

        return "No CVE found"

    except Exception:
        return "CVE lookup failed"
