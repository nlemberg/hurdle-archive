pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }
        stage('Build+Run'){
            steps {
                sh "echo 'building and running'"
                sh 'docker-compose up -d --build'
                sh 'sleep 30'
            }
        }
        stage('Destroy'){
            steps {
                sh "echo 'spinning down'"
                sh 'docker-compose down -v'
            }
        }
    }
    post {
        always {
            cleanWs(deleteDirs: true)
            sh '''
                docker image prune -af
                docker volume prune -af
                docker container prune -f
                docker network prune -f
            '''
        }
    }
}