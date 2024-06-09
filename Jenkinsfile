pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the main branch from the GitHub repository
                git url: 'https://github.com/cerform/project-int', branch: 'main'
            }
        }
        stage('Push to Main Branch') {
            steps {
                // Add your push commands here
                echo 'Pushing changes to the main branch...'
                sh 'git add .'
                sh 'git commit -m "Commit message"'
                sh 'git push origin main'
            }
        }
        stage('Pull from Main Branch') {
            steps {
                // Pull changes from the main branch
                echo 'Pulling changes from the main branch...'
                sh 'git pull origin main'
            }
        }
    }

    post {
        always {
            // Clean up workspace
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
