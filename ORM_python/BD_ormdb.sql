CREATE DATABASE ormdb;


CREATE TABLE estudiantes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    grado VARCHAR(50),
    seccion VARCHAR(10),
    edad INTEGER
);

CREATE TABLE cursos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE estudiante_curso (
    estudiante_id INT REFERENCES estudiantes(id) ON DELETE CASCADE,
    curso_id INT REFERENCES cursos(id) ON DELETE CASCADE,
    PRIMARY KEY (estudiante_id, curso_id)
);


INSERT INTO cursos (nombre) VALUES ('Matemática'), ('Comunicación'), ('Física'); 