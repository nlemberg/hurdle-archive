pipeline {

    agent any

    triggers {
        pollSCM('H/5 * * * *')  // polls every 5 minutes
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    
    environment {
        ECR_REPO="644435390668.dkr.ecr.us-east-1.amazonaws.com/nl-hurdle-archive"
        EC2_IP = sh(script: 'aws ec2 describe-instances --filters "Name=tag:Name,Values=nl-jenkins" --query "Reservations[0].Instances[0].PublicDnsName" --output text', returnStdout: true).trim()
        TEST_NET = 'jenkins-test-net'
    }
    
    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t hurdle-archive .'
            }
        }
        stage('Run'){
            steps {
                sh """
                    export TEST_NET=${TEST_NET}
                    docker-compose up -d
                """
            }
        }
        stage('Test Container'){
            steps {
                retry(15) {
                sleep(time: 3, unit: 'SECONDS')
                // sh """
                //     docker run --rm --network ${TEST_NET} \
                //         docker.io/curlimages/curl:latest \
                //         -fsSLI http://nginx:80
                // """
                sh "curl -fsSLI http://${EC2_IP}:80"
                }
            }
            post {
                always {
                    sh 'docker-compose down -v'
                }
                success {
                    sh "echo 'hurdle-archive is up and running on nginx'"
                }
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