#!/bin/bash
# 1. Upload Transaction Data (The Step I Missed!)
zowe zos-files upload file-to-data-set "data/transactions.txt" "Z88264.ZBRIDGE.TRANS"

# 2. Submit Setup (Allocate Files)
zowe zos-jobs submit local-file "jcl/setup_env.jcl"

# 3. Compile Static Utility first (Required for Main Link-edit)
zowe zos-jobs submit local-file "jcl/compile_static.jcl"

# 4. Compile Dynamic Subprogram
zowe zos-jobs submit local-file "jcl/compile_calc.jcl"

# 5. Compile and Link Main Orchestrator
zowe zos-jobs submit local-file "jcl/compile_main.jcl"

# 6. Run the Test
zowe zos-jobs submit local-file "jcl/run_main.jcl"