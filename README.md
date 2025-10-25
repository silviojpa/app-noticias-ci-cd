# 🚀 App de Notícias Python - Pipeline CI/CD com Jenkins e Docker

Este projeto demonstra uma pipeline de Integração Contínua e Entrega Contínua (CI/CD) completa para uma aplicação web simples desenvolvida em **Python** (Flask).

O objetivo principal é automatizar todo o fluxo de trabalho, desde a codificação até o deploy final em ambiente local (simulando um servidor de produção/staging), utilizando **Jenkins** como orquestrador, **Docker** para empacotamento, e **Docker Hub** como repositório de artefatos.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Função |
| :--- | :--- | :--- |
| **Aplicação** | Python 3.x, Flask | Servidor Web simples que exibe um feed de notícias (App Notícias). |
| **Containerização** | Docker | Empacota a aplicação Python e suas dependências. |
| **Orquestração CI/CD** | Jenkins | Automatiza e executa todos os estágios do pipeline (Testes, Build, Push, Deploy). |
| **Testes/Qualidade** | Pytest, Flake8 | Garante a qualidade do código e a funcionalidade da aplicação. |
| **Registro de Imagens**| Docker Hub | Repositório público para armazenar a imagem Docker final (`silvio69luiz/app-noticias`). |

---

## ⚙️ Pipeline Jenkins (Jenkinsfile)

O pipeline segue um modelo Declarativo e possui os seguintes estágios automatizados:

| Estágio | Descrição |
| :--- | :--- |
| 1. `Checkout Code` | Clona o repositório do GitHub (`https://github.com/silviojpa/app-noticias-ci-cd.git`). |
| 2. `Test and Lint` | Cria um ambiente virtual, instala dependências, executa testes de unidade (`pytest`) e verifica a qualidade do código (`flake8`). |
| 3. `Build Docker Image` | Constrói a imagem Docker da aplicação, taggeando-a como `silvio69luiz/app-noticias:latest`. |
| 4. `Push to Docker Hub` | **Autentica** de forma segura no Docker Hub (usando o método `withCredentials` com Token) e envia a imagem Docker construída para o repositório remoto. |
| 5. `Deploy to Localhost` | Para e remove qualquer container antigo, e inicia um novo container Docker, mapeando a porta **8083** do host para a porta **5000** do container, expondo a aplicação. |

### 🔑 Detalhe da Autenticação do Docker Hub

O pipeline utiliza uma abordagem robusta para autenticação no Docker Hub, contornando falhas comuns em plugins do Jenkins.

- **Tipo de Credencial:** Username with password (`dockerhub-credentials`).
- **Método:** `withCredentials` para injetar o Token de Acesso (password) e o nome de usuário (`silvio69luiz`) como variáveis de ambiente temporárias.
- **Login Seguro:** O login é forçado via `sh` e `stdin` (Standard Input), garantindo que a autorização de push seja estabelecida corretamente:
  ```groovy
  sh "echo \"$DOCKER_PASSWORD\" | docker login -u $DOCKER_USERNAME --password-stdin docker.io"
_____________________________________________________________________

💻 Acesso à Aplicação
Após a conclusão bem-sucedida do pipeline, a aplicação está acessível no ambiente local.

URL de Acesso:
``http://localhost:8083``

- A tela da aplicação exibirá o "Feed de Notícias DevOps".

📝 Como Replicar este Pipeline

-- Para replicar este projeto em seu próprio ambiente Jenkins:

- Credenciais do Docker Hub: Crie uma credencial do tipo "Username with password" no Jenkins com o ID dockerhub-credentials, usando seu nome de usuário e um Token de Acesso gerado no Docker Hub.

- Repo do Código: Configure um novo Pipeline no Jenkins, apontando para o arquivo Jenkinsfile deste repositório.

- Execução: Inicie o Build!
  
