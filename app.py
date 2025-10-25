from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simula um banco de dados de notícias
NOTICIAS = [
    {"id": 1, "titulo": "Jenkins e Python: A Dupla Perfeita para DevOps", "conteudo": "A automação de CI/CD garante entregas mais rápidas e seguras."},
    {"id": 2, "titulo": "Ubuntu 22.04: Estabilidade para Servidores", "conteudo": "A nova versão LTS oferece melhorias na segurança e performance."},
    {"id": 3, "titulo": "Docker Hub: O Repositório do seu Artefato", "conteudo": "Empacotar a aplicação em um container facilita a implantação em qualquer ambiente."}
]

@app.route('/')
def home():
    # Retorna uma lista de títulos em HTML simples
    html_content = "<h1>Feed de Notícias DevOps</h1><ul>"
    for noticia in NOTICIAS:
        html_content += f"<li><a href='/noticia/{noticia['id']}'>{noticia['titulo']}</a></li>"
    html_content += "</ul><p>Versão: 1.0.0 (CI/CD)</p>"
    return render_template_string(html_content)

@app.route('/noticia/<int:noticia_id>')
def noticia_detail(noticia_id):
    noticia = next((n for n in NOTICIAS if n["id"] == noticia_id), None)
    if noticia:
        return render_template_string(
            "<h1>{{ titulo }}</h1><p>{{ conteudo }}</p><p><a href='/'>Voltar</a></p>",
            titulo=noticia['titulo'],
            conteudo=noticia['conteudo']
        )
    return "Notícia não encontrada", 404

if __name__ == '__main__':
    # Rodar a aplicação em 0.0.0.0 para que seja acessível dentro do Docker
    app.run(host='0.0.0.0', port=5000)