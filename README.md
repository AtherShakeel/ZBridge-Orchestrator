ZBridge-Orchestrator
ZBridge-Orchestrator is a Python-based automation suite for mainframe DevOps. It manages the end-to-end lifecycle of COBOL applications on IBM z/OS—from environment setup and source code deployment to compilation, execution, and final VSAM data validation.

📂 Project Structure
Plaintext

VibeGarden/
├── cobol/ # Main COBOL Source
├── copy/ # COBOL Copybooks
├── subprogs/ # Static and Dynamic Subprograms
├── jcl/ # Mainframe JCL templates
│ ├── setup*env.jcl # Cleanup and Allocation
│ ├── compile*\*.jcl # Compilation Pipeline
│ └── run_main.jcl # Main Execution Job
├── scripts/ # Python Automation Layer
│ ├── build_and_run.py # Main Pipeline Logic
│ └── check_vsam.py # Data Verification Utility
├── logs/ # Spool Audit Logs (Ignored by Git)
├── .gitignore # Git exclusion rules
└── README.md # Documentation

🚀 Pipeline Workflow
Environment Setup: Runs setup_env.jcl to ensure PDS members and VSAM clusters are allocated.

Source Deployment: Uploads COBOL source, copybooks, and subprograms using Zowe CLI.

Compilation Chain: Executes a sequence of compile jobs, checking for RC <= 4 and parsing for IGYPS compiler errors.

Main Execution: Runs the final load module and captures runtime VSAM status codes.

Automated Validation: Invokes check_vsam.py to verify that records were correctly written to the VSAM master file.

🛠 Usage
Local Development
Run the orchestrator from the project root directory:

Bash

python scripts/build_and_run.py
CI/CD Integration (Jenkins)
The orchestrator automatically detects the following Environment Variables for secure mainframe access:

MF_USER - Mainframe Username

MF_PASS - Mainframe Password

MF_HOST - Mainframe Host Address

📜 Logging & Audit
Every step generates a detailed log file in the /logs directory containing the full JES spool output. This ensures that even if a job fails on the mainframe, the developer can debug the issue directly from their local IDE.
