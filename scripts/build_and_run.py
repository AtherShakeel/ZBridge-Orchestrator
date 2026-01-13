import os
import subprocess
import datetime
import time
import re
import argparse
import sys
from check_vsam import verify_vsam_content

# ==============================================================================
# 1. CREDENTIAL GATEKEEPER (The "Piece" you asked about)
# ==============================================================================
# Looks for variables set by Jenkins. If they don't exist, it stays empty for local.
Z_USER = os.getenv('MF_USER')
Z_PASS = os.getenv('MF_PASS')

def get_auth():
    """Builds the credential string for Zowe commands."""
    if Z_USER and Z_PASS:
        return f" --user {Z_USER} --pass {Z_PASS} --reject-unauthorized false"
    return ""

AUTH_TOKEN = get_auth()
#=======================================================================================

# Project Config
HLQ = "Z88264"
LOG_DIR = "logs"
JCL_DIR = "jcl"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def parse_cobol_errors(spool_text):
    # Scans spool for IGY messages (COBOL Compiler)
    errors = re.findall(r"IGYPS\d{4}-[USE].*", spool_text)
    return errors

def parse_runtime_status(spool_text):
    # Scans for VSAM File Status or logic displays
    status_codes = re.findall(r"STATUS CODE: \d{2}", spool_text)
    return status_codes

def run_zos_job(jcl_file, step_name):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    log_name = f"{LOG_DIR}/{step_name}_{timestamp}.log"

    print(f"--- Submitting {step_name} ---")

    # Execute via Zowe CLI, We append the AUTH_TOKEN here so it works in Jenkins
    cmd = f"zowe zos-jobs submit local-file \"{jcl_file}\" --wait-for-output --view-all-spool-content {AUTH_TOKEN}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # Save Full Spool to Log File
    with open(log_name, "w") as f:
        f.write(result.stdout)

    # Check for Return Code
    match = re.search(r"RC=(\d{4})", result.stdout)
    rc = int(match.group(1)) if match else 999

    if rc > 4:
        print(f"ERROR: {step_name} FAILED WITH RC {rc}")

        # Parse COBOL errors if applicable
        cobol_errs = parse_cobol_errors(result.stdout)
        if cobol_errs:
            print("--- COBOL COMPILER ERRORS ---")
            for err in cobol_errs[:5]:
                print(f"  {err}")

        print(f"Check full log: {log_name}")
        return False

    print(f"SUCCESS: {step_name} (RC {rc})")

    # Runtime verification for the EXEC step
    if "run_main" in jcl_file:
        runtime_codes = parse_runtime_status(result.stdout)
        for code in runtime_codes:
            print(f"  VSAM {code}")

    return True

# ==============================================================================
# 3. MAIN ORCHESTRATION
# ==============================================================================

def main():
    print(f"Starting ZBridge Deployment for {HLQ}")

    # --- STEP 1: CLEANUP FIRST ---
    # Call this manually BEFORE the uploads
    if not run_zos_job(f"{JCL_DIR}/setup_env.jcl", "SETUP_ENV"):
        print("Setup failed. Aborting.")
        return

    # Data Push
    print("Uploading transaction data...")
    subprocess.run(f"zowe zos-files upload file-to-data-set \"data/transactions.txt\" \"{HLQ}.ZBRIDGE.TRANS\" {AUTH_TOKEN}", shell=True, capture_output=True)
     # Copybook Push
    print("Uploading copybook...")
    subprocess.run(f"zowe zos-files upload dir-to-pds \"copy\" \"{HLQ}.ZBRIDGE.COPYLIB\" {AUTH_TOKEN}", shell=True, capture_output=True)
     # Subprograms Push
    print("Uploading subprograms...")
    subprocess.run(f"zowe zos-files upload dir-to-pds \"subprogs\" \"{HLQ}.ZBRIDGE.SUBSRC\" {AUTH_TOKEN}", shell=True, capture_output=True)
     # Main Program Push
    print("Uploading main program LNVAL01...")
    subprocess.run(f"zowe zos-files upload dir-to-pds \"cobol\" \"{HLQ}.ZBRIDGE.SOURCE\" {AUTH_TOKEN}", shell=True, capture_output=True)

    print("Waiting for mainframe catalog to sync...")
    time.sleep(2)

    # JCL Execution Pipeline
    pipeline = [
        (f"{JCL_DIR}/compile_static.jcl", "BUILD_STATIC"),
        (f"{JCL_DIR}/compile_calc.jcl", "BUILD_DYNAMIC"),
        (f"{JCL_DIR}/compile_alert.jcl", "BUILD_ALERT"),
        (f"{JCL_DIR}/compile_main.jcl", "BUILD_MAIN"),
        (f"{JCL_DIR}/run_main.jcl", "EXEC_TEST")
    ]

    for jcl, name in pipeline:
        if not run_zos_job(jcl, name):
            print("DEPLOYMENT ABORTED DUE TO ERRORS.")
            sys.exit(1)

    # --- ADD THE SLEEP HERE ---
    print("\nWaiting 5 seconds for VSAM buffers to settle...")
    time.sleep(5)

    # ==========================================================================
    # STEP 4: THE LAST STEP - VSAM VALIDATION
    # ==========================================================================
    print("\n--- DEPLOYMENT FINISHED. STARTING FINAL VSAM CHECK ---")

    # This calls the script check_vsam.py we have under /scripts folder
    if verify_vsam_content(auth_token=AUTH_TOKEN, hlq=HLQ):
        print("\n[COMPLETE] ZBridge-Orchestrator: ALL STEPS AND DATA VERIFIED.")
        sys.exit(0) # Tells Jenkins: SUCCESS
    else:
        print("\n[COMPLETE] ZBridge-Orchestrator: DATA VALIDATION FAILED.")
        sys.exit(1) # Tells Jenkins: FAILURE


if __name__ == "__main__":
    main()