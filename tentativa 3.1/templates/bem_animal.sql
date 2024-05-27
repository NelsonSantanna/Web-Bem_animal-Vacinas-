CREATE DATABASE bem_animal2;

USE bem_animal2;

CREATE TABLE responsavel (
    id int PRIMARY KEY AUTO_INCREMENT,
    nome varchar(50) not null,
    pet int not null,
    telefone varchar(14) unique,
    email varchar(50) unique,
    password varchar (20) not null,
    admin tinyint(1)

);

CREATE TABLE users (
    ID int,
    email varchar(50),
    password (255)
);

