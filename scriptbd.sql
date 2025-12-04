DROP DATABASE IF EXISTS blog_lorena;

CREATE DATABASE blog_lorena;

USE blog_lorena;

CREATE TABLE usuario(
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nomeUsuario VARCHAR(50) NOT NULL,
    user VARCHAR(15) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    fotoUsuario VARCHAR(100),
    dataCadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE post(
    idPost INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(50) NOT NULL,
    conteudo TEXT NOT NULL,
    dataPost TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    curtidas INT DEFAULT 0,
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

-- Status de ativo(1) ou desativado(0)
ALTER TABLE usuario
ADD ativo BOOLEAN NOT NULL DEFAULT 1;

-- Vê a quantidade de posts de usuários ativos
CREATE VIEW vw_total_posts AS
SELECT
    COUNT(*) AS total_posts
FROM
    post p
JOIN 
    usuario u ON p.idUsuario = u.idUsuario
WHERE
    u.ativo = 1;

-- Vê a quantidade de usuários
CREATE VIEW vw_total_usuarios AS
SELECT
    COUNT(*) AS total_usuarios
FROM
    usuario
WHERE
    ativo = 1;

-- CREATE TABLE curtidas (
--     idUsuario INT NOT NULL,
--     idPost INT NOT NULL,
--     dataCurtida DATETIME DEFAULT CURRENT_TIMESTAMP,
--     PRIMARY KEY (idUsuario, idPost),
--     FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE,
--     FOREIGN KEY (idPost) REFERENCES post(idPost) ON DELETE CASCADE
-- );

