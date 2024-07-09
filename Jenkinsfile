pipeline {
    agent any
 
    stages {
        stage('Setup') {
            steps {
                // Checkout the repository
                git 'https://github.com/cerform/project-int.git'
                
                // Create and activate virtual environment
                sh 'python -m venv venv' // Create virtual environment
                sh '. venv/bin/activate' // Activate virtual environment
                
                // Install dependencies
                sh 'python -m pip install --upgrade pip setuptools wheel'
                sh 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                // Run tests using pytest
                sh 'pytest'
            }
        }
        
        // Add more stages for other tasks like building Docker images, pushing to repositories, etc.
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}
