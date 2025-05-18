import tempfile
import shutil
import subprocess
from scanners.trivy_scan import run_trivy_scan, simplify_trivy_results
from scanners.bandit_scan import run_bandit_scan
from utils.report_generator import generate_report
from alerts.github_alert import create_github_issue

GITHUB_REPO = "https://github.com/qxresearch/qxresearch-event-1.git"

def extract_critical_vulns(simplified_trivy_result):
    return [v for v in simplified_trivy_result if v.get("Severity") == "CRITICAL"]

def clone_repo(repo_url):
    tmp_dir = tempfile.mkdtemp()
    print(f"📂 Cloning {repo_url} into {tmp_dir} ...")
    subprocess.run(["git", "clone", repo_url, tmp_dir], check=True)
    return tmp_dir

def main():
    print("🔍 Starting SecureScan...")

    repo_path = clone_repo(GITHUB_REPO)

    # Run scanners
    raw_trivy_results = run_trivy_scan(repo_path)
    simplified_trivy_results = simplify_trivy_results(raw_trivy_results)
    bandit_results = run_bandit_scan(repo_path)

    # Generate report with simplified results
    generate_report(simplified_trivy_results, bandit_results)

    # Create GitHub issue for criticals
    criticals = extract_critical_vulns(simplified_trivy_results)
    if criticals:
        print(f"🚨 {len(criticals)} Critical issues found. Creating GitHub issue.")
        issue_title = "⚠️ Critical Vulnerabilities Detected in Latest Scan"
        issue_body = "\n".join(
            f"- {v['VulnerabilityID']} in {v['PkgName']} ({v['Severity']})"
            for v in criticals[:10]  # limit for display
        )
        create_github_issue(GITHUB_REPO, issue_title, issue_body)

    shutil.rmtree(repo_path)
    print("✅ Scan finished.")

if __name__ == "__main__":
    main()
