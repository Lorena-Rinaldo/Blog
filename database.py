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
                "SELECT p.*,u.user, u.fotoUsuario FROM post p INNER JOIN usuario u ON u.idUsuario = p.idUsuario WHERE u.ativo = 1 ORDER BY idPost DESC"
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
        conexao.rollback()
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


def adicionar_usuario(nome, user, senha, foto):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # O trecho '(%s, %s, %s)' significa injeção de SQL
            sql = "INSERT INTO usuario (nomeUsuario,user,senha,fotoUsuario) VALUES (%s, %s, %s,%s)"
            cursor.execute(sql, (nome, user, senha,foto))
            conexao.commit()
            return True, "ok"
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return False, erro


def verificar_usuario(usuario, senha):
    try:
        with conectar() as conexao:
            # O dictionary True, se não ativado, pegaria os atributo do BD por números, e não pelo nome( ex: idUsuario )
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT * FROM usuario WHERE user = %s;"
            # A vírgula sozinha é uma tupla, pois sem ela, o programa entende que é uma variável
            cursor.execute(sql, (usuario,))
            usuario_encontrado = cursor.fetchone()
            if usuario_encontrado:
                if usuario_encontrado['senha'] == '1234' and senha == '1234': 
                    return True, usuario_encontrado
                if check_password_hash(usuario_encontrado["senha"], senha):
                    return True, usuario_encontrado
            return False, None
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return False, None


def alterar_status(idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            sql = "SELECT ativo FROM usuario WHERE idUsuario = %s;"
            cursor.execute(sql, (idUsuario,))
            status = cursor.fetchone()

            if status["ativo"]:
                sql = "UPDATE usuario SET ativo = 0 WHERE idUsuario = %s;"
            else:
                sql = "UPDATE usuario SET ativo = 1 WHERE idUsuario = %s;"

            cursor.execute(sql, (idUsuario,))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro de BD! \n Erro: {erro}")
        return False, None


def delete_usuario(idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            sql = "DELETE FROM usuario WHERE idUsuario = %s;"
            cursor.execute(sql, (idUsuario,))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro de BD! \n Erro: {erro}")
        return False, None


def listar_posts_por_usuario(idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            sql = """
                SELECT p.*, u.user 
                FROM post p
                INNER JOIN usuario u ON u.idUsuario = p.idUsuario
                WHERE p.idUsuario = %s
                ORDER BY p.idPost DESC
            """
            cursor.execute(sql, (idUsuario,))
            return cursor.fetchall()
    except mysql.connector.Error as erro:
        print(f"Erro ao listar posts do usuário {idUsuario}: {erro}")
        return []


def atualizar_post(titulo, conteudo, idPost):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            # O trecho '(%s, %s, %s)' significa injeção de SQL
            sql = "UPDATE post SET titulo=%s,conteudo=%s WHERE idPost = %s"
            cursor.execute(sql, (titulo, conteudo, idPost))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        conexao.rollback()
        print(f"Erro de BD! \n Erro: {erro}")
        return False


def totais():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM vw_total_posts")
            total_posts = cursor.fetchone()

            cursor.execute("SELECT * FROM vw_total_usuarios")
            total_usuarios = cursor.fetchone()

            return total_posts, total_usuarios

    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return None, None
    
def reset_senha(idUsuario):
    print("Entrou na função reset senha")
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            sql = "UPDATE usuario SET senha = '1234' WHERE idUsuario = %s"
            print(f"Sql: {sql} - {idUsuario}")
            cursor.execute(sql, (idUsuario,))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        conexao.rollback()
        return False
    
def alterar_senha(senha_hash, idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            sql = "UPDATE usuario SET senha = %s WHERE idUsuario = %s"
            print(f"Sql: {sql} - {idUsuario}")
            cursor.execute(sql, (senha_hash, idUsuario))
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        conexao.rollback()
        return False
    
def editar_perfil(nome, user, nome_foto, idUsuario):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary=True)
            if nome_foto:
                sql = "UPDATE usuario SET nomeUsuario = %s, user = %s, fotoUsuario = %s WHERE idUsuario = %s"
                cursor.execute(sql, (nome, user, nome_foto, idUsuario))
            else:
                sql = "UPDATE usuario SET nomeUsuario = %s, user = %s WHERE idUsuario = %s"
            conexao.commit()
            return True
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        conexao.rollback()
        return False
        

# def buscar_curtidas(idPost):
#     try:
#         with conectar() as conexao:
#             cursor = conexao.cursor(dictionary=True)
#             sql = "SELECT curtidas FROM post WHERE idPost = %s"
#             cursor.execute(sql, (idPost,))
#             resultado = cursor.fetchone()
#             if resultado:
#                 return resultado['curtidas']
#             else:
#                 return 0
#     except mysql.connector.Error as erro:
#         print(f"Erro ao buscar curtidas: {erro}")
#         return 0


# def curtir_post(idPost):
#     try:
#         with conectar() as conexao:
#             cursor = conexao.cursor()
#             sql = "UPDATE post SET curtidas = curtidas + 1 WHERE idPost = %s"
#             cursor.execute(sql, (idPost,))
#             conexao.commit()
#             return True
#     except mysql.connector.Error as erro:
#         conexao.rollback()
#         print(f"Erro ao curtir post: {erro}")
#         return False
