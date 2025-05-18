# trivy_scan.py
import subprocess
import json

def run_trivy_scan(target_path):
    try:
        result = subprocess.run(
            ["trivy", "fs", "--format", "json", target_path],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Trivy scan failed:", e.stderr)
        return {}
def simplify_trivy_results(trivy_json):
    simplified = []
    for result in trivy_json.get("Results", []):
        for v in result.get("Vulnerabilities", []):
            simplified.append({
    "VulnerabilityID": v.get("VulnerabilityID"),
    "PkgName": v.get("PkgName"),
    "InstalledVersion": v.get("InstalledVersion"),
    "Severity": v.get("Severity"),
    "Title": v.get("Title"),
    "Description": v.get("Description"),
    "FixedVersion": v.get("FixedVersion"),
    "PrimaryURL": v.get("PrimaryURL"),
})

    return simplified

