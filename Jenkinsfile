pipeline {
    agent any

    options {
        timeout(time: 5, unit: 'MINUTES')
        ansiColor('xterm')
    }

    environment {
        // Mapping Jenkins Vault credentials to environment variables
        MF_CREDS = credentials('mainframe-auth')
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
                // Expose credentials to Python script
                withEnv(["MF_USER=${MF_CREDS_USR}", "MF_PASS=${MF_CREDS_PSW}"]) {
                    script {
                        if (isUnix()) {
                            // Linux / Mac
                            sh 'python3 scripts/build_and_run.py'
                        } else {
                            // Windows
                            bat 'python scripts\\build_and_run.py'
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'zBridge-Orchestrator Pipeline finished. Archiving Logs...'
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
        }
        failure {
            echo 'FAILURE: Check the archived logs in the Build Artifacts section.'
        }
    }
}
