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
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

ALTER TABLE usuario
ADD ativo BOOLEAN NOT NULL DEFAULT 1;


-- CREATE TABLE curtida (
--     idCurtida INT PRIMARY KEY AUTO_INCREMENT,
--     idUsuario INT,
--     idPost INT,
--     dataCurtida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
--     FOREIGN KEY (idPost) REFERENCES post(idPost)
-- );

