pipeline {
    agent any
    parameters {
        choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Deployment environment')
        string(name: 'TAG', defaultValue: 'latest', description: 'Docker image tag')
    }
    triggers {
        pollSCM('*/5 * * * *') // Poll Git every 5 minutes
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/koakko/lab13-input.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("my-app:${params.TAG}")
                }
            }
        }
        stage('Test Container!') {
            steps {
                script {
                    dockerImage.inside {
                        sh 'curl -f http://192.168.0.180:3000 || exit 1'
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                expression { params.ENV == 'prod' }
            }
            input {
                message "Deploy to production with tag ${params.TAG}?"
                ok 'Deploy'
                parameters {
                    choice(name: 'SERVER', choices: ['server1', 'server2'], description: 'Target server')
                }
            }
            steps {
                script {
                    echo "Deploying to ${params.ENV} on ${SERVER} with tag ${params.TAG}"
                    sh "docker run -d -p 3000:3000 --name my-app-${params.ENV} my-app:${params.TAG}"
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}