import mysql.connector

# Função para se conectar com o Banco de Dados SQL
def conectar():
    conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'senai',
    database = "blog_lorena"
    )

    if conexao.is_connected():
        print("Conexão com BD ok!")

    return conexao

# Função para listar todas as postagens
def listar_post():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor(dictionary = True)
            cursor.execute("SELECT * FROM post ORDER BY idPost DESC")
            return cursor.fetchall()
    except mysql.connector.Error as erro:
        print(f"Erro de BD! \n Erro: {erro}")
        return [] #Lista vazia
    
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