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
                bat 'echo %PATH%' // Print the current PATH to the console for debugging
                bat '"E:\\Dev_Ops\\etcsys\\project-int\\python.exe" --version'
                bat '"E:\\Dev_Ops\\etcsys\\project-int\\Scripts\\pip.exe" --version'
                bat '"E:\\Dev_Ops\\etcsys\\project-int\\Scripts\\pip.exe" install -r requirements.txt'
            }
        }
        // Other stages...
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
