CREATE DATABASE blog_lorena;

USE blog_lorena;

CREATE TABLE usuario(
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nomeUsuario VARCHAR(50) NOT NULL,
    user VARCHAR(15) NOT NULL UNIQUE,
    senha VARCHAR(60) NOT NULL,
    fotoUsuario VARCHAR(100),
    dataCadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE post(
    idPost INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(50) NOT NULL,
    conteudo TEXT NOT NULL,
    dataPost TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);
