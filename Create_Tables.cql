-- Usar o Keyspace
USE default_keyspace;

-- Criar as Tabelas
CREATE TABLE Alunos (
    id_aluno INT PRIMARY KEY,
    nome TEXT
);

CREATE TABLE Professores (
    id_professor INT PRIMARY KEY,
    nome TEXT
);

CREATE TABLE Disciplinas (
    id_disciplina INT PRIMARY KEY,
    nome TEXT,
    id_professor INT
);

CREATE TABLE Departamentos (
    id_departamento INT PRIMARY KEY,
    nome TEXT,
    id_chefe_professor INT
    chefe_professor_nome TEXT
);

CREATE TABLE Cursos (
    id_curso INT PRIMARY KEY,
    nome TEXT,
    id_departamento INT,
    chefe_professor_nome text
);

CREATE TABLE Matriz_Curricular (
    id_matriz INT PRIMARY KEY,
    id_curso INT
);

CREATE TABLE Historico_Escolar (
    id_aluno INT,
    id_disciplina INT,
    ano INT,
    semestre INT,
    nota_final FLOAT,
    PRIMARY KEY (id_aluno, ano, semestre, id_disciplina)
) WITH CLUSTERING ORDER BY (ano ASC, semestre ASC);

CREATE TABLE Grupo_de_TCC (
    id_grupo_tcc INT PRIMARY KEY,
    tema TEXT,
    id_aluno1 INT,
    id_aluno2 INT,
    id_professor INT
);

CREATE TABLE Notas (
    id_historico INT PRIMARY KEY,
    nota FLOAT
);

CREATE TABLE alunos_historico (
  id_aluno INT,
  nome TEXT,
  id_historico UUID,
  ano INT,
  semestre INT,
  nota_final FLOAT,
  id_disciplina INT,
  disciplina_nome TEXT,
  id_professor INT,
  professor_nome TEXT,
  PRIMARY KEY (id_aluno)
);

CREATE TABLE professores_disciplinas (
  id_professor INT,
  id_disciplina INT,
  disciplina_nome TEXT,
  professor_nome TEXT,
  semestre INT,
  ano INT,
  PRIMARY KEY (id_professor, id_disciplina)
);


CREATE TABLE departamentos_cursos (
  id_departamento INT,
  departamento_nome TEXT,
  id_chefe_professor INT,
  chefe_professor_nome TEXT,
  id_curso INT,
  curso_nome TEXT,
  PRIMARY KEY (id_departamento, id_curso)
);

CREATE TABLE matrizes_curriculares (
  id_curso INT,
  curso_nome TEXT,
  id_matriz INT,
  PRIMARY KEY (id_curso, id_matriz)
);

CREATE TABLE grupos_tcc (
  id_grupo_tcc UUID,
  tema TEXT,
  id_aluno1 INT,
  aluno1_nome TEXT,
  id_aluno2 INT,
  aluno2_nome TEXT,
  id_professor INT,
  professor_nome TEXT,
  PRIMARY KEY (id_grupo_tcc)
);
