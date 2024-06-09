pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Check out the main branch
                git url: 'https://github.com/cerform/project-int', branch: 'main'
            }
        }
        stage('Setup') {
            steps {
                // Ensure Python and pip are installed, and install dependencies
                echo 'Setting up the environment...'
                bat 'python --version'
                bat 'pip --version'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Build') {
            steps {
                // Example build step
                echo 'Building the project...'
                // Add actual build commands here
            }
        }
        stage('Test') {
            steps {
                // Run tests using pytest
                echo 'Running tests...'
                bat 'pytest'
            }
        }
        stage('Deploy') {
            steps {
                // Deployment steps
                echo 'Deploying the application...'
                // Add actual deployment commands here
            }
        }
        stage('Run Application') {
            steps {
                // Run the application
                echo 'Running the application...'
                // Add commands to run the application here
            }
        }
    }

    post {
        always {
            // Clean up workspace
            echo 'Cleaning up...'
            cleanWs()
        }
        failure {
            // Log build failure
            echo 'Build failed!'
        }
        success {
            // Log build success
            echo 'Build succeeded!'
        }
    }
}
