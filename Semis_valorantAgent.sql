CREATE DATABASE SemisDB;

USE SemisDB;

CREATE TABLE Characters (
    char_id INT PRIMARY KEY,
    code_name VARCHAR(100),
    real_name VARCHAR(100),
    agent_type VARCHAR(100),
    country_orig VARCHAR(100)
);

DROP DATABASE SemisDB;