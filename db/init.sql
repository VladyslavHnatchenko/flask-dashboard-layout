CREATE DATABASE game;
use game;

CREATE TABLE IF NOT EXISTS admins (
    id int NOT NULL AUTO_INCREMENT,
    username varchar(50) NOT NULL,
    password varchar(255),
    date_created DATE, PRIMARY KEY(id)
);