import os
import subprocess
import datetime

# Project Config
LOG_DIR = "logs"

def verify_vsam_content(auth_token="", hlq="Z88264"):
    # 1. Setup paths
    cluster_name = f"{hlq}.ZBRIDGE.MASTER"
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    log_name = f"{LOG_DIR}/util_verify_vsam_{timestamp}.log"

    os.makedirs(LOG_DIR, exist_ok=True)

    print(f"--- Verification: Viewing {cluster_name} ---")

    # 2. Command to view the VSAM cluster
    # 'view' is often more reliable for VSAM content translation than 'read'
    cmd = f"zowe zos-files view data-set \"{cluster_name}\" {auth_token}"

    try:
        # Run the command and capture output
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # 3. Audit Logging (Saves what we saw for Jenkins artifacts)
        with open(log_name, "w") as f:
            f.write(result.stdout)

        # 4. Process Records
        # Split by lines and filter out any empty lines
        records = [line for line in result.stdout.splitlines() if line.strip()]

        if records:
            print(f"Successfully extracted {len(records)} records.")
            print("Top ten records:")

            # Print the first 10 records found in the VSAM
            for i, record in enumerate(records[:10], 1):
                print(f"{i}: {record}")

            return True
        else:
            # If stdout is empty, check if stderr has an error message
            if result.stderr:
                print(f"MAINFRAME ERROR: {result.stderr.strip()}")
            else:
                print(f"WARNING: The VSAM cluster {cluster_name} appears to be empty.")
            return False

    except Exception as e:
        print(f"SYSTEM ERROR during VSAM view: {str(e)}")
        return False

if __name__ == "__main__":
    # In ZBridge-Orchestrator, this can be run standalone to test the view
    verify_vsam_content(hlq="Z88264")