// Jenkinsfile (Declarative Pipeline)

pipeline {
    // Definimos o agente como 'any', o que usará o nó principal ou um agente disponível.
    agent any 

    // Variáveis de ambiente
    environment {
        // ID da credencial que você criou no Jenkins
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        // Nome do repositório no Docker Hub 
        DOCKER_IMAGE_NAME = "silvio69luiz/app-noticias"
        
        // NOVO: Variáveis para o Deploy Local
        HOST_PORT = 8083 //  (Jenkins está na 8082)
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
                
                // 2. Não ativamos o venv com o '. activate' para evitar problemas de PATH.
                // sh '. venv/bin/activate'
                // Em vez disso, chamamos os binários diretamente pelo caminho.
                
                // 3. Instalamos com o pip do venv, usando --ignore-installed 
                // para garantir que a instalação seja feita no venv.
                sh './venv/bin/pip install --ignore-installed -r requirements.txt' 
                
                // 4. Chamamos o executável de teste do venv
                sh './venv/bin/pytest'
                
                // 5. Chamamos o executável de lint do venv
                sh './venv/bin/flake8 --max-complexity=10 --max-line-length=120 --exclude=venv . || true'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Usa a função 'docker.build' do plugin Docker Pipeline
                    docker.build("${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Autentica com o Docker Hub usando as credenciais configuradas
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS) {
                        // Faz o push da imagem com o número do build
                        sh "docker push ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}" 
                        
                        // Opcional: Faz o push da tag 'latest' também
                        sh "docker tag ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ${DOCKER_IMAGE_NAME}:latest"
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    }
                }
            }
        }
        
        stage('Deploy to Localhost') {
            steps {
                sh """
                echo "Iniciando o Deploy da imagem ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                
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
                  ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}
                """
            }
        }
    }

    post {
        // Bloco executado no final, independente do resultado (SUCCESS ou FAILURE)
        always {
            // Boa prática: remove o ambiente virtual criado no estágio 'Test' para liberar espaço
            sh 'rm -rf venv || true' 
        }
        // Notificação de sucesso
        success {
            echo "Pipeline concluído com SUCESSO!"
            echo "IMAGEM PUBLICADA: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
            echo "APLICAÇÃO ACESSÍVEL EM: http://localhost:${HOST_PORT}"
        }
        // Notificação de falha
        failure {
            echo "Pipeline FALHOU! Verifique o log do estágio que falhou."
        }
    }
}










