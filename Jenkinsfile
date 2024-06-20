pipeline {
    agent {
        docker {
            image 'etcsys/jenkins-agent:latest'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Build and Test') {
            steps {
                script {
                    docker.build('project-int-app', '-f Dockerfile.app .')
                    docker.build('project-int-nginx', '-f Dockerfile.nginx .')
                }
                sh 'docker-compose up -d'
            }
        }
    }
    post {
        always {
            sh 'docker-compose down'
        }
    }
}
