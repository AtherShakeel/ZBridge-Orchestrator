import os
import subprocess
import datetime
import re

# Project Config
LOG_DIR = "logs"

def verify_vsam_content(auth_token="", hlq="Z88264"):
    # 1. Setup paths using our util_* naming convention
    cluster_name = f"{hlq}.ZBRIDGE.MASTER"
    jcl_path = "jcl/util_print_vsam.jcl"
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    log_name = f"{LOG_DIR}/util_verify_vsam_{timestamp}.log"

    os.makedirs(LOG_DIR, exist_ok=True)

    print(f"--- Verification: Checking {cluster_name} ---")

    # 2. Command to submit the local JCL utility
    cmd = f"zowe zos-jobs submit local-file \"{jcl_path}\" --wait-for-output --view-all-spool-content {auth_token}"

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # 3. Log the spool output for audit
        with open(log_name, "w") as f:
            f.write(result.stdout)

        # 4. Check IDCAMS output for records
        # 1. Look for 'LISTING' and 'DATA' regardless of dashes or spaces
        if "LISTING" in result.stdout.upper():

        # 2. Use \s* to handle the dash/space at the start
        # 3. Use \s+ to handle any number of spaces between the offset and data
            records = re.findall(r"\d{4}\s\s+(.*)", result.stdout)

            if records:
                print(f"Successfully extracted {len(records)} records.")
                print("Top ten records:")
                for i, record in enumerate(records[:10], 1):
                    print(f"{i}: {record}")
                return True
            else:
                print("DEBUG: Regex failed. Here is a sample line from stdout:")
                return False
        else:
            print(f"FAILURE: Could not read VSAM. See {log_name}")
            return False

    except Exception as e:
        print(f"SYSTEM ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    # This only runs if YOU run this file directly
    # Great for testing your regex without running the whole build!
    verify_vsam_content(hlq="Z88264")