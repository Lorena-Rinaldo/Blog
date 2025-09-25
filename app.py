from flask import Flask, render_template, request, redirect, flash
from database import listar_post, adicionar_post

# Informa o tipo do app
app = Flask(__name__)

app.secret_key = "blog"  # Chave secreta -> quando precisamos passar informações de forma oculta para o navegador, precisamos do secret_key -> usado no login e senha também


# Rota Página Inicial
@app.route("/")
def index():
    postagens = listar_post()
    return render_template(
        "index.html", postagens=postagens
    )  # O template lida com informações


# Rota do form de postagem


@app.route("/novopost", methods=["GET", "POST"])
def novopost():
    if request.method == "GET":
        return redirect("/")
    if request.method == "POST":
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]
        idUsuario = 1
        post = adicionar_post(titulo, conteudo, idUsuario)

        # Se for verdadeiro(True):
        if post:
            flash("Post realizado com sucesso")
        else:
            flash("ERRO! Falha ao Postar!")

        # Encaminhar para a rota da página iniciaç
        return redirect("/")


#  ---Final do Arquivo---
if __name__ == "__main__":
    app.run(debug=True)
