pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/cerform/project-int'
            }
        }
        stage('Setup') {
            steps {
                echo 'Setting up the environment...'
                // Ensure Python and pip are installed
                bat 'python --version'
                bat 'pip --version'
                // Install dependencies
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
                // Add any build steps if necessary, for example:
                // bat 'python setup.py build'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                bat 'pytest'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Add the deploy command here if applicable
            }
        }
        stage('Run Application') {
            steps {
                echo 'Running the application...'
                // Add the run command here if applicable
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            cleanWs()
        }
        failure {
            echo 'Build failed!'
        }
        success {
            echo 'Build succeeded!'
        }
    }
}
