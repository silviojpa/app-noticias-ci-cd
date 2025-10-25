// Jenkinsfile (Declarative Pipeline)

pipeline {
    agent any // Ou agent { docker 'python:3.9-slim' } 

    // Variáveis de ambiente
    environment {
        // ID da credencial 
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        // Nome do repositório no Docker Hub (ex: meu-usuario/app-noticias)
        DOCKER_IMAGE_NAME = "silvio69luiz/app-noticias" 
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clona o código do Git
                git branch: 'main', url: 'URL_DO_SEU_REPOSITORIO_GIT' 
            }
        }

        stage('Test and Lint') {
            steps {
                // Cria e ativa um virtual environment
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
                
                // Exemplo de execução de testes (assumindo Pytest instalado)
                sh 'pytest'
                
                // Exemplo de Linting (assumindo flake8 instalado)
                sh 'flake8 --max-complexity=10 --max-line-length=120 .'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Usa a função 'docker.build' do plugin Docker Pipeline
                    // A tag é o ID do build do Jenkins para versionamento único
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
    }

    post {
        // Notificação de sucesso/falha
        success {
            echo "Pipeline concluído com SUCESSO! Imagem: ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline FALHOU!"
        }
    }
}