from flask import Flask, render_template, request, redirect, flash, session, jsonify
from database import *
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

import os
import mysql.connector

# Carregar esse arquivo para o Python
load_dotenv()

# Acessar as variáveis
secret_key = os.getenv("SECRET_KEY")
usuario_admin = os.getenv("USUARIO_ADMIN")
senha_admin = os.getenv("SENHA_ADMIN")

# Informa o tipo do app
app = Flask(__name__)
app.secret_key = secret_key  # Chave secreta -> quando precisamos passar informações de forma oculta para o navegador, precisamos do secret_key -> usado no login e senha também


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
        titulo = request.form["titulo"].strip()
        conteudo = request.form["conteudo"].strip()
        idUsuario = session["idUsuario"]
        if not titulo or not conteudo:
            flash("Preencha todos os campos!")
            return redirect("/")
        post = adicionar_post(titulo, conteudo, idUsuario)

        # Se for verdadeiro(True):
        if post:
            flash("Post realizado com sucesso")
        else:
            flash("ERRO! Falha ao Postar!")

        # Encaminhar para a rota da página inicial
    return redirect("/")


# Rota para Editar posts
@app.route("/editarpost/<int:idPost>", methods=["GET", "POST"])
def editarpost(idPost):
    if "user" not in session or "admin" in session:
        return redirect("/")

    # Checa a autoria da postagem
    with conectar() as conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(f"SELECT idUsuario FROM post WHERE idPost = {idPost}")
        autor_post = cursor.fetchone()
        if not autor_post or autor_post["idUsuario"] != session.get("idUsuario"):
            print("Tentativa de edição inválida")
            return redirect("/")

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
        titulo = request.form["titulo"].strip()
        conteudo = request.form["conteudo"].strip()
        if not titulo or not conteudo:
            flash("Preencha todos os campos!")
            return redirect(f"/editarpost/{idPost}")

        sucesso = atualizar_post(titulo, conteudo, idPost)
        if sucesso:
            flash("Post Atualizado com Sucesso")
        else:
            flash("Erro! Tente mais tarde")
        return redirect("/")


# Rota para Excluir Post
@app.route("/excluirpost/<int:idPost>")
def excluirpost(idPost):
    if not session:
        print("Usuário não autorizado acessando a rota excluir")
        return redirect("/")
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            if "admin" not in session:
                cursor.execute(f"SELECT idUsuario FROM post WHERE idPost = {idPost}")
                autor_post = cursor.fetchone()
                if not autor_post or autor_post["idUsuario"] != session.get(
                    "idUsuario"
                ):
                    print("Tentativa de exclusão inválida")
                    return redirect("/")

            cursor.execute(f"DELETE FROM post WHERE idPost = {idPost}")
            conexao.commit()
            flash("Post Excluído com Sucesso!")
            if "admin" in session:
                return redirect("/dashboard")
            else:
                return redirect("/")

    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro de BD! \n Erro: {erro}")
        flash("Ops! Tente mais tarde!")
        return redirect("/")


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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        usuario = request.form["user"].lower().strip()
        senha = request.form["senha"].strip()
        # Verifica se todos os campos foram preenchidos
        if not usuario or not senha:
            flash("Preencha todos os campos")
            return redirect("/login")

        # 1°, verifica se o usuário é o admin
        if usuario == usuario_admin and senha == senha_admin:
            session["admin"] = True
            return redirect("/")

        # 2°, verifica se é um usuário cadastrado
        resultado, usuario_encontrado = verificar_usuario(usuario, senha)
        if resultado:
            if usuario_encontrado["ativo"] == 0:
                flash("Usuário Banido! Fale com o Suporte")
                return redirect("/login")
            session["idUsuario"] = usuario_encontrado["idUsuario"]
            session["user"] = usuario_encontrado["user"]
            return redirect("/")

        # 3° Nenhum usuário ou ADMIN foram encontrados
        else:
            flash("Usuário ou senhas incorretos")
            return redirect("/login")


# Rota Área de Adminitração (Dashboard)
@app.route("/dashboard")
def dashboard():
    if not session or "admin" not in session:
        flash("Acesso não autorizado!")
        return redirect("/")

    usuarios = listar_usuarios()
    posts = listar_post()  # Carrega todos os posts inicialmente para a coluna de posts
    total_posts, total_usuarios = totais()

    for post in posts:
        post["conteudo_resumo"] = truncar_conteudo(post["conteudo"], limite=50)

    return render_template(
        "dashboard.html",
        posts=posts,
        usuarios=usuarios,
        total_posts=total_posts,
        total_usuarios=total_usuarios,
    )


@app.route("/api/posts_por_usuario/<int:idUsuario>")
def api_posts_por_usuario(idUsuario):
    # 1. Checagem de segurança (apenas admin pode acessar)
    if not session or "admin" not in session:
        return jsonify({"erro": "Acesso não autorizado"}), 403

    # 2. Chama a nova função de BD
    posts_filtrados = listar_posts_por_usuario(idUsuario)

    posts_para_json = []
    for post in posts_filtrados:
        post_json = dict(post)

        # 3. CONVERSÃO DE DATA: transforma o objeto datetime em string
        if isinstance(post_json.get("dataPost"), (datetime, date)):
            post_json["dataPost"] = post_json["dataPost"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            post_json["dataPost"] = str(post_json.get("dataPost", ""))

        # 4. Adiciona o resumo para a visualização no Dashboard
        post_json["conteudo_resumo"] = truncar_conteudo(
            post_json["conteudo"], limite=50
        )
        posts_para_json.append(post_json)

    return jsonify({"posts": posts_para_json})


# Rota do Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# Rota para cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    elif request.method == "POST":
        nome = request.form["nome"].strip()
        usuario = request.form["user"].lower().strip()
        senha = request.form["senha"].strip()

        if not nome or not usuario or not senha:
            flash("Preencha todos os campos!")
            return redirect("/cadastro")

        senha_hash = generate_password_hash(senha)

        resultado, erro = adicionar_usuario(nome, usuario, senha_hash)

        if resultado:
            flash("Usuário Cadastrado com Sucesso")
            return redirect("/login")
        else:
            if erro.errno == 1062:
                flash("Usuário já existente.")
            else:
                flash("Erro ao cadastrar. Procure o suporte")
            return redirect("/cadastro")


@app.route("/usuario/status/<int:idUsuario>")
def status_usuario(idUsuario):
    if not session:
        return redirect("/")

    sucesso = alterar_status(idUsuario)
    if sucesso:
        flash("Status Alterado com Sucesso")
    else:
        flash("Erro na Alteração do Status")
    return redirect("/dashboard")


@app.route("/usuario/excluir/<int:idUsuario>")
def excluir_usuario(idUsuario):
    if not session or "admin" not in session:
        return redirect("/")

    sucesso = delete_usuario(idUsuario)

    if sucesso:
        flash("Usuário Excluído com Sucesso")
    else:
        flash("Erro na Exclusão do Usuário")
    return redirect("/dashboard")


@app.route("/usuario/reset/<int:idUsuario>")
def reset(idUsuario):
    if "admin" not in session:
        return redirect("/")
    sucesso = reset_senha(idUsuario)
    if sucesso:
        flash("Senha Resetada com Sucesso")
        return redirect('/dashboard')
    else:
        flash("Falha ao Resetar Senha")
        return redirect('/dashboard')

# @app.route('/curtir/<int:idPost>', methods=['POST'])
# def curtir(idPost):
#     if curtir_post(idPost):
#         print(f"Post {idPost} recebeu uma curtida!")
#     else:
#         print(f"Erro ao curtir o post {idPost}")
#     return redirect(url_for('index'))


# ERRO 404
@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("e404.html")


# ERRO 500
@app.errorhandler(500)
def erro_interno(error):
    return render_template("e500.html")


#  ---Final do Arquivo---
if __name__ == "__main__":
    app.run(debug=True)
