pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                // Checkout the repository
                git 'https://github.com/cerform/project-int.git'
                
                // Install dependencies (if needed)
                sh 'python -m pip install --upgrade pip setuptools wheel'
                sh 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Activate Virtual Environment') {
            steps {
                // Replace '/path/to/your/venv' with the actual path to your venv directory
                sh 'source /path/to/your/venv/bin/activate'
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
