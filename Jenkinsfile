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
        EC2_IP = "${env.EC2_IP}" // configured in jenkins ui
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
                sh 'docker-compose up -d'
            }
        }

        stage('Test'){
            steps {
                retry(15) {
                sleep(time: 3, unit: 'SECONDS')
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

        stage('Calculate Version'){
            when {
                // branch "main"
                branch "jenkins" // switch
            }
            steps {
                script {
                    try {
                        // Fetch tags from the remote repo
                        sh 'git fetch --tags'
                        
                        // Get the latest version tag on the current branch (local repo)
                        def latestTag = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                        sh 'echo ${latestTag}'
                        
                        // Initialize major, minor, and patch components
                        def major = 0
                        def minor = 0
                        def patch = 0
                        
                        // Extract version components from the latest tag
                        def versionTokens = latestTag.tokenize('.')
                        major = versionTokens[0].toInteger()
                        minor = versionTokens[1].toInteger()
                        patch = versionTokens[2].toInteger()
                        
                        // Calculate the new version
                        def newVersion = "${major}.${minor}.${patch + 1}"
                        
                        // Set the new version as an environment variable for later stages
                        env.NEW_VERSION = newVersion
                        
                        echo "Latest Tag: ${latestTag}"
                        echo "New Version: ${newVersion}"

                    } catch (Exception e) {
                        // No tags found (edge case)
                        echo "No tags found. Please contact the Admin"
                    }
                }
            }
        }


        ////////
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