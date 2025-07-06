pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gustavobarrera/miapp-web'
        DOCKER_TAG = "v${sh(script: 'git rev-list --count HEAD', returnStdout: true).trim()}" // Agrega secuencialidad x cada commit
        DOCKER_CREDENTIALS_ID = 'dockerhub_id' // Jenkins credentials ID
        COMPOSE_FILE = 'docker-compose.yaml'
        CONTAINER_NAME = 'miapp-test'
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

        stage('Iniciar contenedor con Docker Compose') {
            steps {
                script {
                    sh """
                    docker compose -f ${COMPOSE_FILE} up -d --force-recreate
                    """
                }
            }
        }

        stage('Verificar puerto del contenedor') {
            steps {
                script {
                    def puerto = sh(script: "docker inspect -f '{{.NetworkSettings.Ports}}' ${CONTAINER_NAME} | cut -c5-8", returnStdout: true).trim()

                    def estado = sh(script: "ss -tuln | grep ':$puerto ' | cut -c7-12 | tail -n 1", returnStdout: true).trim()

                    echo "Estado del puerto: $estado"

                    if (estado != "LISTEN") {
                        error("Revisión de puerto, fallida. Deteniendo el pipeline.")
                    } else {
                        echo "Revisión de puerto, correcta. Continuando el pipeline."
                    }
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