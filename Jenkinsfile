pipeline {
    agent any

    options {
        timeout(time: 5, unit: 'MINUTES')
        ansiColor('xterm')
    }

    environment {
        MF_CREDS = credentials('mainframe-auth')
        GIT_CREDS = credentials('github-auth')
    }

    stages {
        stage('Pull from GitHub') {
            steps {
                echo 'Pulling fresh zBridge-Orchestrator Code...'
                git branch: 'main',
                    credentialsId: 'github-auth',
                    url: 'https://github.com/AtherShakeel/zBridge-Orchestrator'
            }
        }

        stage('Execute ZBridge-Orchestrator') {
            steps {
                echo 'Starting Mainframe Build, Run, and VSAM Validation...'
                // Use 'bat' for Windows and pass credentials as arguments just like your last project
                bat "python scripts/build_and_run.py --user %MF_CREDS_USR% --pass %MF_CREDS_PSW%"
            }
        }
    }

    post {
        always {
            echo 'zBridge-Orchestrator Pipeline finished. Archiving Logs...'
            // This ensures we can find those specific log files you asked about
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
        }
    }
}