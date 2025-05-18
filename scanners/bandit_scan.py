import subprocess
import shutil
import os

def run_bandit_scan(target_path):
    bandit_path = shutil.which("bandit")
    if not bandit_path:
        raise RuntimeError("❌ Bandit is not installed or not in PATH.")

    os.makedirs("reports", exist_ok=True)
    output_file = "reports/bandit_output.json"

    result = subprocess.run(
        [bandit_path, "-r", target_path, "-f", "json", "-o", output_file],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("⚠️ Bandit finished with warnings/errors:")
        print(result.stderr)

    return output_file
