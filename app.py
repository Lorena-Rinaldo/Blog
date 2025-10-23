from flask import Flask, render_template, request, redirect, flash, session
from database import *
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        usuario = request.form["user"].lower()
        senha = request.form["senha"]
        # Verifica se todos os campos foram preenchidos
        if usuario is None or senha is None:
            flash("Preencha todos os campos")
            return redirect('/login')
        
        # 1°, verifica se o usuário é o admin
        if usuario == usuario_admin and senha == senha_admin:
            session["admin"] = True
            return redirect("/")
        
        # 2°, verifica se é um usuário cadastrado
        resultado, usuario_encontrado = verificar_usuario(usuario, senha)
        if resultado:
            session['idUsuario'] = usuario_encontrado['idUsuario']
            session['user'] = usuario_encontrado['user']
            return redirect('/')
        
        # 3° Nenhum usuário ou ADMIN foram encontrados
        else:
            flash("Usuário ou senhas incorretos")
            return redirect("/login")


# Área de Adminitração
@app.route("/dashboard")
def dashboard():
    # Bloqueio para acessos indevidos
    if not session or "admin" not in session:
        return redirect("/")

    usuarios = listar_usuarios()
    posts = listar_post()
    return render_template("dashboard.html", posts=posts, usuarios=usuarios)


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
        nome = request.form['nome']
        usuario = request.form['user'].lower()
        senha = request.form['senha']
        
        if nome is None or usuario is None or senha is None:
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


#  ---Final do Arquivo---
if __name__ == "__main__":
    app.run(debug=True)
