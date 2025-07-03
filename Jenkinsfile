pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gustavobarrera/miapp-web'
        DOCKER_TAG = "v${sh(script: 'git rev-list --count HEAD', returnStdout: true).trim()}" // Agrega secuencialidad x cada commit
        DOCKER_CREDENTIALS_ID = 'dockerhub_id' // Jenkins credentials ID
    }

    stages {
        stage('Clonar código') {
            steps {
                checkout scm
            }
        }

        stage('Construir imagen Docker') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Login en Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        echo 'Login exitoso en Docker Hub'
                    }
                }
            }
        }

        stage('Push a Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        image.push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Imagen publicada en Docker Hub: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo "Error en el pipeline"
        }
    }
}