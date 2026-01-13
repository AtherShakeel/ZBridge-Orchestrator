pipeline {
    agent any

    options {
        timeout(time: 5, unit: 'MINUTES') // Slightly longer for ZBridge-Orchestrator
        ansiColor('xterm')               // MUST HAVE: Makes Zowe/Python logs readable
    }

    environment {
        // Reusing your existing credential IDs
        MF_CREDS = credentials('mainframe-auth')
        GIT_CREDS = credentials('github-auth')
    }

    stages {
        stage('Pull from GitHub') {
            steps {
                echo 'Pulling fresh ZBridge-Orchestrator Code...'
                git branch: 'main',
                    credentialsId: 'github-auth',
                    url: 'https://github.com/AtherShakeel/zBridge-Orchestrator'
            }
        }

        stage('Execute ZBridge-Orchestrator') {
            steps {
                echo 'Starting Mainframe Build, Run, and VSAM Validation...'
                // Using 'sh' because you are now a Git Bash / Linux-style pro!
                sh """
                export MF_USER=${MF_CREDS_USR}
                export MF_PASS=${MF_CREDS_PSW}
                python scripts/build_and_run.py
                """
            }
        }
    }

    post {
        always {
            echo 'ZBridge-Orchestrator Pipeline finished. Archiving Logs...'
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
        }
        success {
            echo 'SUCCESS: ZBridge-Orchestrator is healthy and VSAM data is verified!'
        }
        failure {
            echo 'FAILURE: Check the Console Output. Mainframe or Validation error.'
        }
    }
}