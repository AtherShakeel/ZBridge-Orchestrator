# ZBridge-Orchestrator

<!-- Badges -->

![Python](https://img.shields.io/badge/Python-3.x-blue)
![z/OS](https://img.shields.io/badge/IBM%20z%2FOS-Mainframe-informational)
![COBOL](https://img.shields.io/badge/COBOL-Application-orange)
![JCL](https://img.shields.io/badge/JCL-Automation-yellow)
![Zowe CLI](https://img.shields.io/badge/Zowe-CLI-brightgreen)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-red)
![VSAM](https://img.shields.io/badge/VSAM-Validation-purple)
![Repo size](https://img.shields.io/github/repo-size/AtherShakeel/ZBridge-Orchestrator)
![Contributors](https://img.shields.io/github/contributors/AtherShakeel/ZBridge-Orchestrator)
![Issues](https://img.shields.io/github/issues/AtherShakeel/ZBridge-Orchestrator)
![Last commit](https://img.shields.io/github/last-commit/AtherShakeel/ZBridge-Orchestrator)
![Stars](https://img.shields.io/github/stars/AtherShakeel/ZBridge-Orchestrator?style=social)
![Forks](https://img.shields.io/github/forks/AtherShakeel/ZBridge-Orchestrator?style=social)

ZBridge-Orchestrator is a Python-based automation suite for mainframe DevOps. It manages the end-to-end lifecycle of COBOL applications on IBM z/OS — from environment setup and source code deployment to compilation, execution, and final VSAM data validation.

---

## Project Structure

```text
ZBridge-Orchestrator/
├── cobol/                 # Main COBOL Source
├── copy/                  # COBOL Copybooks
├── subprogs/              # Static and Dynamic Subprograms
├── jcl/                   # Mainframe JCL templates
│   ├── setup_env.jcl      # Cleanup and Allocation
│   ├── compile_*.jcl      # Compilation Pipeline
│   └── run_main.jcl       # Main Execution Job
├── scripts/               # Python Automation Layer
│   ├── build_and_run.py   # Main Pipeline Logic
│   └── check_vsam.py      # Data Verification Utility
├── logs/                  # Spool Audit Logs (Ignored by Git)
├── .gitignore             # Git exclusion rules
└── README.md              # Documentation
Pipeline Workflow
Environment Setup: Runs setup_env.jcl to ensure PDS members and VSAM clusters are allocated.

Source Deployment: Uploads COBOL source, copybooks, and subprograms using Zowe CLI.

Compilation Chain: Executes a sequence of compile jobs, checking for RC <= 4 and parsing for IGYPS compiler errors.

Main Execution: Runs the final load module and captures runtime VSAM status codes.

Automated Validation: Invokes check_vsam.py to verify that records were correctly written to the VSAM master file.

Usage
Local Development
Run the orchestrator from the project root directory:

bash
Copy code
python scripts/build_and_run.py
CI/CD Integration (Jenkins)
The orchestrator automatically detects the following environment variables for secure mainframe access:

MF_USER — Mainframe Username

MF_PASS — Mainframe Password

MF_HOST — Mainframe Host Address

Logging & Audit
Every step generates a detailed log file in the /logs directory containing the full JES spool output. This ensures that even if a job fails on the mainframe, the developer can debug the issue directly from their local IDE.

CI/CD Automation
This project includes a Jenkinsfile for automated mainframe orchestration. It triggers the build_and_run.py script to compile COBOL, deploy to z/OS, and perform VSAM data validation.
```
