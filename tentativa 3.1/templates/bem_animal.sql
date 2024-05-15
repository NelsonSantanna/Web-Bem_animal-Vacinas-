CREATE DATABASE bem_animal2;

USE bem_animal2;

CREATE TABLE responsavel (
    id int PRIMARY KEY AUTO_INCREMENT,
    pet int not null,
    nome varchar(50) not null,
    telefone varchar(14) unique,
    email varchar(50) unique,
    password varchar (20) not null
);

CREATE TABLE pet (
    id int PRIMARY KEY,
    nome varchar(50),
    data_nascimento date,
    raca varchar(50),
    ativo varchar(3)
);

CREATE TABLE vacinacao (
    id int PRIMARY KEY,
    data date
);

CREATE TABLE adota (
    fk_responsavel_id int,
    fk_pet_id int,
    FOREIGN KEY (fk_responsavel_id) REFERENCES responsavel(id) ON DELETE RESTRICT,
    FOREIGN KEY (fk_pet_id) REFERENCES pet(id) ON DELETE RESTRICT
);

CREATE TABLE recebe (
    fk_pet_id int,
    fk_vacinacao_id int,
    FOREIGN KEY (fk_pet_id) REFERENCES pet(id) ON DELETE RESTRICT,
    FOREIGN KEY (fk_vacinacao_id) REFERENCES vacinacao(id) ON DELETE RESTRICT
);

ALTER TABLE adota ADD CONSTRAINT FK_adota_1
    FOREIGN KEY (fk_responsavel_id)
    REFERENCES responsavel (id)
    ON DELETE RESTRICT;

ALTER TABLE adota ADD CONSTRAINT FK_adota_2
    FOREIGN KEY (fk_pet_id)
    REFERENCES pet (id)
    ON DELETE RESTRICT;

ALTER TABLE recebe ADD CONSTRAINT FK_recebe_1
    FOREIGN KEY (fk_pet_id)
    REFERENCES pet (id)
    ON DELETE RESTRICT;

ALTER TABLE recebe ADD CONSTRAINT FK_recebe_2
    FOREIGN KEY (fk_vacinacao_id)
    REFERENCES vacinacao (id)
    ON DELETE RESTRICT;