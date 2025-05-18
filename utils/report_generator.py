import os
from weasyprint import HTML

def generate_report(trivy_data, bandit_data, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)

    # Defensive check for Trivy data
    trivy_section = "\n".join(
        f"<li>{v.get('VulnerabilityID')} - {v.get('PkgName')} ({v.get('Severity')})</li>"
        for v in trivy_data if isinstance(v, dict)
    ) or "<li>No vulnerabilities found.</li>"

    # Defensive check for Bandit data
    bandit_section = "\n".join(
        f"<li>{issue.get('issue_text')} (Severity: {issue.get('issue_severity')})</li>"
        for issue in bandit_data if isinstance(issue, dict)
    ) or "<li>No issues found.</li>"

    html_content = f"""
    <html>
        <head>
            <title>SecureScan Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                h1 {{ color: #2c3e50; }}
                ul {{ background: #f9f9f9; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>🛡️ SecureScan Report</h1>
            <h2>Trivy Results</h2>
            <ul>{trivy_section}</ul>
            <h2>Bandit Results</h2>
            <ul>{bandit_section}</ul>
        </body>
    </html>
    """

    html_path = os.path.join(output_dir, "scan_report.html")
    pdf_path = os.path.join(output_dir, "scan_report.pdf")

    with open(html_path, "w") as f:
        f.write(html_content)

    try:
        HTML(html_path).write_pdf(pdf_path)
        print(f"📄 PDF Report saved at {pdf_path}")
    except Exception as e:
        print(f"⚠️ Failed to generate PDF: {e}")

    print(f"✅ HTML Report saved at {html_path}")
