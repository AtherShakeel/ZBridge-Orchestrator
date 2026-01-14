pipeline {
    agent any

    options {
        timeout(time: 5, unit: 'MINUTES')
        ansiColor('xterm')
    }

    stages {
        stage('Pull from GitHub') {
            steps {
                echo 'Pulling fresh zBridge-Orchestrator code...'
                git branch: 'main',
                    credentialsId: 'github-auth',
                    url: 'https://github.com/AtherShakeel/zBridge-Orchestrator'
            }
        }

        stage('Execute ZBridge-Orchestrator') {
            steps {
                echo 'Starting Mainframe Build, Run, and VSAM Validation...'

                // Securely pass credentials to the script
                withCredentials([usernamePassword(
                    credentialsId: 'mainframe-auth',
                    usernameVariable: 'MF_USER',
                    passwordVariable: 'MF_PASS'
                )]) {
                    script {
                        if (isUnix()) {
                            // Linux / macOS
                            try {
                                sh 'python3 scripts/build_and_run.py'
                            } catch (err) {
                                error "Python script failed on Unix: ${err}"
                            }
                        } else {
                            // Windows
                            try {
                                bat 'python scripts\\build_and_run.py'
                            } catch (err) {
                                error "Python script failed on Windows: ${err}"
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'zBridge-Orchestrator pipeline finished. Archiving logs...'
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
        }
        failure {
            echo 'FAILURE: Check the archived logs in the Build Artifacts section.'
        }
    }
}
