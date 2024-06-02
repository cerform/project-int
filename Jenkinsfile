pipeline {
    agent any

    environment {
        // Define any environment variables you need here
        GIT_REPO_URL = 'https://github.com/cerform/project-int'
        BRANCH_NAME = 'master'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO_URL}"
            }
        }

        stage('Build') {
            steps {
                // Commands to build your project
                echo 'Building the project...'
                sh 'your-build-command-here' // Replace with your actual build command
            }
        }

        stage('Test') {
            steps {
                // Commands to run tests
                echo 'Running tests...'
                sh 'your-test-command-here' // Replace with your actual test command
            }
        }

        stage('Deploy') {
            steps {
                // Commands to deploy your project
                echo 'Deploying the application...'
                sh 'your-deploy-command-here' // Replace with your actual deploy command
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            cleanWs() // Clean the workspace after the build
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
