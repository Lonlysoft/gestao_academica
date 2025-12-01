/*
CREATE DATABASE IF NOT EXISTS gestao_academica;
USE gestao_academica;

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'professor', 'aluno') NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE administrador (
    id_administrador INT PRIMARY KEY,
    departamento VARCHAR(50),
    nivel_acesso ENUM('total', 'parcial') DEFAULT 'parcial',
    FOREIGN KEY (id_administrador) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE professor (
    id_professor INT PRIMARY KEY,
    especialidade VARCHAR(100),
    data_contratacao DATE NOT NULL,
    formacao VARCHAR(100),
    registro VARCHAR(20) UNIQUE NOT NULL,
    regime_trabalho ENUM('integral', 'parcial', 'horista') DEFAULT 'integral',
    FOREIGN KEY (id_professor) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE aluno (
    id_aluno INT PRIMARY KEY,
    data_ingresso DATE NOT NULL,
    status ENUM('ativo', 'inativo', 'trancado', 'formado') DEFAULT 'ativo',
    registro VARCHAR(20) UNIQUE NOT NULL, 
    FOREIGN KEY (id_aluno) REFERENCES usuario(id_usuario) ON DELETE CASCADE
);

CREATE TABLE disciplina (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ementa TEXT,
    carga_horaria INT NOT NULL,
    prerequisitos TEXT,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    carga_horaria_total INT NOT NULL,
    coordenador_id INT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao DATE NOT NULL DEFAULT (CURRENT_DATE)
);
*/

CREATE TABLE turma (
    id_turma INT AUTO_INCREMENT PRIMARY KEY,
    codigo_turma VARCHAR(20) UNIQUE NOT NULL,
    periodo VARCHAR(10) NOT NULL,
    horario VARCHAR(50),
    vagas_totais INT NOT NULL,
    vagas_ocupadas INT DEFAULT 0,
    id_curso INT NOT NULL,
    id_professor INT NOT NULL,
    id_disciplina INT NOT NULL,
    ativa BOOLEAN DEFAULT TRUE,
    data_inicio DATE,
    data_termino DATE
);

ALTER TABLE curso ADD FOREIGN KEY (coordenador_id) REFERENCES professor(id_professor);

-- ver se isso resolve o erro por ALTER TABLE
ALTER TABLE turma ADD FOREIGN KEY (id_curso) REFERENCES curso(id_curso);

ALTER TABLE turma ADD FOREIGN KEY (id_professor) REFERENCES professor(id_professor);

ALTER TABLE turma ADD FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina);

CREATE TABLE matricula (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    data_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('matriculado', 'trancado', 'cancelado', 'aprovado', 'reprovado') DEFAULT 'matriculado',
    nota_final DECIMAL(4,2), 
    frequencia DECIMAL(5,2) DEFAULT 0
);

ALTER TABLE matricula ADD UNIQUE KEY unique_aluno_turma (id_aluno, id_turma);

ALTER TABLE matricula ADD FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) ON DELETE CASCADE;

ALTER TABLE matricula ADD FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE CASCADE;

CREATE TABLE material_aula (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    arquivo_url VARCHAR(500) NOT NULL,
    tipo_arquivo VARCHAR(50),
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_turma INT NOT NULL,
    id_professor INT NOT NULL,
    visivel BOOLEAN DEFAULT TRUE
);

ALTER TABLE material_aula ADD FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE CASCADE;

ALTER TABLE material_aula ADD FOREIGN KEY (id_professor) REFERENCES professor(id_professor) ON DELETE CASCADE;

CREATE TABLE avaliacao (
    id_avaliacao INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    tipo ENUM('prova', 'trabalho', 'apresentacao', 'participacao') DEFAULT 'prova',
    data_avaliacao DATE NOT NULL,
    peso DECIMAL(3,2) NOT NULL,
    id_turma INT NOT NULL,
    valor_maximo DECIMAL(5,2) DEFAULT 10.00
);

ALTER TABLE avaliacao ADD FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE CASCADE;

CREATE TABLE nota (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_avaliacao INT NOT NULL,
    valor_nota DECIMAL(5,2) NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT
);

ALTER TABLE nota ADD UNIQUE KEY unique_aluno_avaliacao (id_aluno, id_avaliacao);

ALTER TABLE nota ADD FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) ON DELETE CASCADE;

ALTER TABLE nota ADD FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id_avaliacao) ON DELETE CASCADE;

CREATE TABLE grade_curricular (
    id_grade INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    id_disciplina INT NOT NULL,
    semestre_ideal INT NOT NULL,
    obrigatoria BOOLEAN DEFAULT TRUE,
    carga_horaria_semestral INT
);

ALTER TABLE grade_curricular ADD UNIQUE KEY unique_curso_disciplina (id_curso, id_disciplina);

ALTER TABLE grade_curricular ADD FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE;

ALTER TABLE grade_curricular ADD FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina) ON DELETE CASCADE;

CREATE TABLE frequencia (
    id_frequencia INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    data_aula DATE NOT NULL,
    presente BOOLEAN DEFAULT FALSE,
    observacao TEXT
);

ALTER TABLE frequencia ADD UNIQUE KEY unique_aluno_turma_data (id_aluno, id_turma, data_aula);

ALTER TABLE frequencia ADD FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) ON DELETE CASCADE;

ALTER TABLE frequencia ADD FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE CASCADE;

-- Adicionar coluna para controle de vagas e prioridade
ALTER TABLE matricula ADD COLUMN prioridade ENUM('normal', 'reprovado') DEFAULT 'normal';

-- solicitações de vagas caso a turma esteja cheia
CREATE TABLE solicitacao_vagas (
    id_solicitacao INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    mensagem TEXT,
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pendente', 'aprovada', 'rejeitada') DEFAULT 'pendente',
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) ON DELETE CASCADE,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE CASCADE
);

-- atividades/respostas dos alunos
CREATE TABLE resposta_atividade (
    id_resposta INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_avaliacao INT NOT NULL,
    resposta TEXT,
    arquivo_url VARCHAR(500),
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_limite DATE,
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_aluno) ON DELETE CASCADE,
    FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id_avaliacao) ON DELETE CASCADE
);

-- indexação
CREATE INDEX idx_usuario_email ON usuario(email);
CREATE INDEX idx_usuario_tipo ON usuario(tipo);
CREATE INDEX idx_turma_curso ON turma(id_curso);
CREATE INDEX idx_turma_professor ON turma(id_professor);
CREATE INDEX idx_matricula_aluno ON matricula(id_aluno);
CREATE INDEX idx_matricula_turma ON matricula(id_turma);
CREATE INDEX idx_nota_aluno ON nota(id_aluno);
CREATE INDEX idx_nota_avaliacao ON nota(id_avaliacao);
CREATE INDEX idx_material_turma ON material_aula(id_turma);
CREATE INDEX idx_avaliacao_turma ON avaliacao(id_turma);