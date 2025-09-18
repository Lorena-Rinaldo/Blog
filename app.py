from flask import Flask, render_template

#Informa o tipo do app
app = Flask(__name__)

postagens = [
    {
        "id":1,
        "usuario": "Liz",
        "titulo": "Meu primeiro blog",
        "conteudo": "Esse blog é muito legal...",
        "data": "2025-09-11"
    },
    {
        "id":2,
        "usuario": "Igor",
        "titulo": "Blog Incrivel",
        "conteudo": "Esse blog é bacana...",
        "data": "2025-09-11"
    },
    {
        "id":3,
        "usuario": "Adriana",
        "titulo": "Flores",
        "conteudo": "Essa flor cheira muito bem",
        "data": "2025-09-11"
    },
    {
        "id":4,
        "usuario": "Daphne",
        "titulo": "Blog Paia",
        "conteudo": "Esse blog é bacana...",
        "data": "2025-09-11"
    },
    {
        "id":5,
        "usuario": "Raphael",
        "titulo": "Blog",
        "conteudo": "Esse blog é legal...",
        "data": "2025-09-11"
    },
]

#Rota Página Inicial
@app.route('/')

def index():
    return render_template('index.html', postagens=postagens) #O template lida com informações


#  ---Final do Arquivo---
if __name__ == "__main__":
    app.run(debug=True)