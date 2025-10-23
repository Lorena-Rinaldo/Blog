import mysql.connector

from werkzeug.security import check_password_hash

# Função para se conectar com o Banco de Dados SQL
def conectar():
    conexao = mysql.connector.connect(
        host="localhost", user="root", password="senai", database="blog_lorena"
    )

    if conexao.is_connected():
        print("Conexão com BD ok!")

    return conexao


# Função para listar todas as postagens
def listar_post():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute(
                "SELECT p.*,u.user, u.fotoUsuario FROM post p INNER JOIN usuario u ON u.idUsuario = p.idUsuario ORDER BY idPost DESC"
            )
            return cursor.fetchall()
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return []  # Lista vazia


def buscar_post_por_id(idPost):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            # A query busca o post pelo ID e faz o JOIN para pegar dados do usuário
            sql = "SELECT p.*,u.user, u.fotoUsuario FROM post p INNER JOIN usuario u ON u.idUsuario = p.idUsuario WHERE p.idPost = %s"
            cursor.execute(sql, (idPost,))
            return cursor.fetchone()  # Retorna um único dicionário (o post)
    except mysql.connector.Error as erro:
        print(f"Erro de BD ao buscar post: \n Erro: {erro}")
        return None  # Retorna None se der erro


def adicionar_post(titulo, conteudo, idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # O trecho '(%s, %s, %s)' significa injeção de SQL
            sql = "INSERT INTO post (titulo, conteudo, idUsuario) VALUES (%s, %s, %s)"
            cursor.execute(sql, (titulo, conteudo, idUsuario))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return False

def listar_usuarios():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuario")
            return cursor.fetchall()
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return []  # Lista vazia


def adicionar_usuario(nome, user, senha):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # O trecho '(%s, %s, %s)' significa injeção de SQL
            sql = "INSERT INTO usuario (nomeUsuario,user,senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, user, senha))
            conexao.commit()
            return True, "ok"
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return False, erro
    
def verificar_usuario(usuario,senha):
    try:
        with conectar() as conexao:
            # O dictionary True, se não ativado, pegaria os atributo do BD por números, e não pelo nome( ex: idUsuario )
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM usuario WHERE user = %s;"
            # A vírgula sozinha é uma tupla, pois sem ela, o programa entende que é uma variável
            cursor.execute(sql, (usuario,) )
            usuario_encontrado = cursor.fetchone()
            if usuario_encontrado:
                if check_password_hash(usuario_encontrado['senha'],senha):
                    return True, usuario_encontrado
            return False, None
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return False, erro
