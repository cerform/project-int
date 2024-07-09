pipeline {
    agent {
        docker {
            image 'your-docker-agent-image'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/etcsys_test']],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [],
                          submoduleCfg: [],
                          userRemoteConfigs: [[url: 'https://github.com/cerform/project-int.git']]])
            }
        }
        stage('Build') {
            steps {
                sh '''
                    docker build -t project-int-app:latest ./app
                    docker build -t project-int-web:latest ./web
                '''
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest'
            }
        }
        stage('Security Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    sh 'snyk container test project-int-app:latest'
                    sh 'snyk container test project-int-web:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker login -u <your-docker-username> -p <your-docker-password>
                    docker push project-int-app:latest
                    docker push project-int-web:latest
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
