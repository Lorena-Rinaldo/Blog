from flask import Flask, render_template, request, redirect, flash
from database import listar_post, adicionar_post, conectar, buscar_post_por_id

import mysql.connector

# Informa o tipo do app
app = Flask(__name__)

app.secret_key = "blog"  # Chave secreta -> quando precisamos passar informações de forma oculta para o navegador, precisamos do secret_key -> usado no login e senha também


def truncar_conteudo(texto, limite=200):
    # Corta o texto e adiciona '...' se ele exceder o limite.
    if len(texto) > limite:
        return texto[:limite] + "..."
    return texto


# Rota Página Inicial
@app.route("/")
def index():
    postagens = listar_post()

    for post in postagens:
        post["conteudo_resumo"] = truncar_conteudo(post["conteudo"], limite=200)

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


# Rota para Editar posts
@app.route("/editarpost/<int:idPost>", methods=["GET", "POST"])
def editarpost(idPost):
    if request.method == "GET":
        try:
            with conectar() as conexao:
                cursor = conexao.cursor(dictionary=True)
                cursor.execute(f"SELECT * FROM post WHERE idPost = {idPost}")
                post = cursor.fetchone()
                postagens = listar_post()
                return render_template("index.html", postagens=postagens, post=post)
        except mysql.connector.Error as erro:
            print(f"Erro de BD! \n Erro: {erro}")
            flash("Houve um erro! Tente mais tarde!")
            return redirect("/")

    if request.method == "POST":
        # Pegando informações do formulário
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]
        try:
            with conectar() as conexao:
                cursor = conexao.cursor()
                # O trecho '(%s, %s, %s)' significa injeção de SQL
                sql = "UPDATE post SET titulo=%s,conteudo=%s WHERE idPost = %s"
                cursor.execute(sql, (titulo, conteudo, idPost))
                conexao.commit()
                return redirect("/")
        except mysql.connector.Error as erro:
            print(f"Erro de BD! \n Erro: {erro}")
            flash("Ops! Tente mais tarde!")
            redirect("/")


# Rota para Excluir Post
@app.route("/excluirpost/<int:idPost>")
def excluirpost(idPost):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # O trecho '(%s, %s, %s)' significa injeção de SQL
            sql = "DELETE FROM post WHERE idPost = %s"
            cursor.execute(sql, (idPost,))
            conexao.commit()
            flash("Post Excluído!")
            return redirect("/")
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        flash("Ops! Tente mais tarde!")
        redirect("/")


@app.route("/post/<int:idPost>")
def exibir_post(idPost):
    # O parâmetro agora é idPost, alinhado com o nome da rota.
    post = buscar_post_por_id(idPost)

    # Nota: Não é necessário truncar aqui, pois você está exibindo o post completo.
    # O conteúdo completo é passado para o template post.html
    if post:
        return render_template("post.html", post=post)
    else:
        flash("Post não encontrado!")
        return redirect("/")


@app.route('/login')
def login():
    return render_template('login.html')

#  ---Final do Arquivo---
if __name__ == "__main__":
    app.run(debug=True)
