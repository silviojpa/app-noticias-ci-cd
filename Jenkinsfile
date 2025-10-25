// Jenkinsfile (Declarative Pipeline)

pipeline {
    // Definimos o agente como 'any', o que usará o nó principal ou um agente disponível.
    agent any 

    // Variáveis de ambiente
    environment {
        // ID da credencial que você criou no Jenkins (MANTIDA como env, mas não será usada no push)
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        // Nome do repositório no Docker Hub 
        DOCKER_IMAGE_NAME = "silvio69luiz/app-noticias"
        
        // Variáveis para o Deploy Local
        HOST_PORT = 8083 // (Jenkins está na 8082)
        CONTAINER_NAME = "app-ci-cd-python"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clona o código do Git
                git branch: 'main', url: 'https://github.com/silviojpa/app-noticias-ci-cd.git' 
            }
        }

        stage('Test and Lint') {
            steps {
                // 1. Cria o virtual environment
                sh 'python3 -m venv venv'
                
                // 2. Instalação no venv
                sh './venv/bin/pip install --ignore-installed -r requirements.txt' 
                
                // 3. Chamamos o executável de teste do venv
                sh './venv/bin/pytest'
                
                // 4. Chamamos o executável de lint do venv
                sh './venv/bin/flake8 --max-complexity=10 --max-line-length=120 --exclude=venv . || true'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Construir a imagem diretamente com a tag :latest
                    docker.build("${DOCKER_IMAGE_NAME}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Usa withCredentials para injetar as variáveis de ambiente com segurança
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'dockerhub-credentials', // Seu ID de credencial
                            passwordVariable: 'DOCKER_PASSWORD', 
                            usernameVariable: 'DOCKER_USERNAME'
                        )
                    ]) 
                    {
                        // 1. Login explícito e seguro, injetando a senha via stdin
                        sh "echo \"$DOCKER_PASSWORD\" | docker login -u $DOCKER_USERNAME --password-stdin"
                        
                        // 2. Push da imagem :latest
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    }
                }
            }
        }
        
        stage('Deploy to Localhost') {
            steps {
                sh """
                echo "Iniciando o Deploy da imagem ${DOCKER_IMAGE_NAME}:latest"
                
                # 1. Parar e remover qualquer container antigo rodando com o mesmo nome
                if docker ps -a | grep -q ${CONTAINER_NAME}; then
                  echo "Removendo container antigo: ${CONTAINER_NAME}"
                  docker stop ${CONTAINER_NAME} || true
                  docker rm ${CONTAINER_NAME} || true
                fi
                
                echo "Iniciando novo container na porta ${HOST_PORT} do host."

                # 2. Rodar o novo container em modo detached (-d)
                # Mapeia a porta do host (8083) para a porta 5000 do container (onde o Flask está)
                docker run -d \\
                  --name ${CONTAINER_NAME} \\
                  -p ${HOST_PORT}:5000 \\
                  ${DOCKER_IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        always {
            sh 'rm -rf venv || true' 
        }
        success {
            echo "Pipeline concluído com SUCESSO!"
            echo "IMAGEM PUBLICADA: ${DOCKER_IMAGE_NAME}:latest"
            echo "APLICAÇÃO ACESSÍVEL EM: http://localhost:${HOST_PORT}"
        }
        failure {
            echo "Pipeline FALHOU! Verifique o log do estágio que falhou."
        }
    }
}


