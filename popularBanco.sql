-- popular banco
USE gestao_academica;

-- Administradores puros
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Maria Administradora', 'maria.admin@universidade.edu.br', 'admin123', TRUE, FALSE, FALSE),
('Carlos Coordenador', 'carlos.coord@universidade.edu.br', 'admin123', TRUE, FALSE, FALSE);

-- Professores puros
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Dr. João Silva', 'joao.silva@universidade.edu.br', 'prof123', FALSE, TRUE, FALSE),
('Dra. Ana Santos', 'ana.santos@universidade.edu.br', 'prof123', FALSE, TRUE, FALSE),
('Prof. Carlos Oliveira', 'carlos.oliveira@universidade.edu.br', 'prof123', FALSE, TRUE, FALSE),
('Dra. Mariana Costa', 'mariana.costa@universidade.edu.br', 'prof123', FALSE, TRUE, FALSE);

-- Alunos puros (primeiros 20)
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Aluno Teste 01', 'aluno01@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 02', 'aluno02@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 03', 'aluno03@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 04', 'aluno04@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 05', 'aluno05@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 06', 'aluno06@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 07', 'aluno07@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 08', 'aluno08@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 09', 'aluno09@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 10', 'aluno10@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 11', 'aluno11@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 12', 'aluno12@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 13', 'aluno13@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 14', 'aluno14@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 15', 'aluno15@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 16', 'aluno16@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 17', 'aluno17@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 18', 'aluno18@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 19', 'aluno19@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 20', 'aluno20@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE);

-- PROFESSORES QUE TAMBÉM SÃO ALUNOS (5 usuários)
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Prof. Dr. Pedro Almeida', 'pedro.almeida@universidade.edu.br', 'senha123', FALSE, TRUE, TRUE),
('Dra. Sofia Martins', 'sofia.martins@universidade.edu.br', 'senha123', FALSE, TRUE, TRUE),
('Prof. Lucas Fernandes', 'lucas.fernandes@universidade.edu.br', 'senha123', FALSE, TRUE, TRUE),
('Dra. Beatriz Ramos', 'beatriz.ramos@universidade.edu.br', 'senha123', FALSE, TRUE, TRUE),
('Prof. Gabriel Costa', 'gabriel.costa@universidade.edu.br', 'senha123', FALSE, TRUE, TRUE);

-- Mais alunos puros
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Aluno Teste 21', 'aluno21@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 22', 'aluno22@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 23', 'aluno23@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 24', 'aluno24@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 25', 'aluno25@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 26', 'aluno26@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 27', 'aluno27@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 28', 'aluno28@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 29', 'aluno29@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 30', 'aluno30@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 31', 'aluno31@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 32', 'aluno32@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 33', 'aluno33@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 34', 'aluno34@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE),
('Aluno Teste 35', 'aluno35@universidade.edu.br', 'aluno123', FALSE, FALSE, TRUE);

-- ADMINISTRADOR QUE TAMBÉM É PROFESSOR
INSERT INTO usuario (nome, email, senha, is_admin, is_professor, is_aluno) VALUES
('Prof. Admin Roberto', 'roberto.admin@universidade.edu.br', 'senha123', TRUE, TRUE, FALSE);

-- Populando tabelas específicas
-- Administradores
INSERT INTO administrador (id_administrador, departamento, nivel_acesso) VALUES
(1, 'TI', 'total'),
(2, 'Acadêmico', 'total'),
(33, 'Administrativo', 'total');

-- Professores (incluindo os que também são alunos)
INSERT INTO professor (id_professor, especialidade, data_contratacao, formacao, regime_trabalho) VALUES
(3, 'Matemática Aplicada', '2018-03-15', 'Doutor em Matemática', 'integral'),
(4, 'Literatura Brasileira', '2019-08-01', 'Doutora em Letras', 'integral'),
(5, 'Banco de Dados', '2020-02-10', 'Mestre em Ciência da Computação', 'integral'),
(6, 'Física Quântica', '2017-11-20', 'Doutor em Física', 'integral'),
(33, 'Gestão Acadêmica', '2020-01-15', 'Doutor em Administração', 'integral'), -- Roberto
-- Professores que também são alunos:
(23, 'Educação a Distância', '2022-01-10', 'Mestre em Educação', 'parcial'),
(24, 'Psicologia Educacional', '2021-03-20', 'Doutora em Psicologia', 'parcial'),
(25, 'Tecnologia Educacional', '2023-02-15', 'Mestre em Computação', 'parcial'),
(26, 'Metodologia Científica', '2022-08-01', 'Doutor em Educação', 'parcial'),
(27, 'Didática', '2021-11-30', 'Mestre em Pedagogia', 'parcial');

-- Alunos (incluindo os que também são professores)
INSERT INTO aluno (id_aluno, data_ingresso, status, registro) VALUES
-- Alunos puros
(7, '2024-01-15', 'ativo', '20240001'),
(8, '2024-01-15', 'ativo', '20240002'),
(9, '2024-01-15', 'ativo', '20240003'),
(10, '2024-01-15', 'ativo', '20240004'),
(11, '2024-01-15', 'ativo', '20240005'),
(12, '2024-01-15', 'ativo', '20240006'),
(13, '2024-01-15', 'ativo', '20240007'),
(14, '2024-01-15', 'ativo', '20240008'),
(15, '2024-01-15', 'ativo', '20240009'),
(16, '2024-01-15', 'ativo', '20240010'),
(17, '2024-01-15', 'ativo', '20240011'),
(18, '2024-01-15', 'ativo', '20240012'),
(19, '2024-01-15', 'ativo', '20240013'),
(20, '2024-01-15', 'ativo', '20240014'),
(21, '2024-01-15', 'ativo', '20240015'),
(22, '2024-01-15', 'ativo', '20240016'),
-- Professores que também são alunos
(23, '2024-01-15', 'ativo', '20240017'),
(24, '2024-01-15', 'ativo', '20240018'),
(25, '2024-01-15', 'ativo', '20240019'),
(26, '2024-01-15', 'ativo', '20240020'),
(27, '2024-01-15', 'ativo', '20240021'),
-- Mais alunos puros
(28, '2024-01-15', 'ativo', '20240022'),
(29, '2024-01-15', 'ativo', '20240023'),
(30, '2024-01-15', 'ativo', '20240024'),
(31, '2024-01-15', 'ativo', '20240025'),
(32, '2024-01-15', 'ativo', '20240026'),
(33, '2024-01-15', 'ativo', '20240027'),
(34, '2024-01-15', 'ativo', '20240028'),
(35, '2024-01-15', 'ativo', '20240029'),
(36, '2024-01-15', 'ativo', '20240030');
-- Cursos, disciplinas e turmas (mantendo do script anterior)
INSERT INTO curso (nome, descricao, carga_horaria_total, coordenador_id, data_criacao) VALUES
('Engenharia de Software', 'Curso de graduação em Engenharia de Software com foco em desenvolvimento de sistemas', 3600, 3, '2020-01-01'),
('Ciência da Computação', 'Curso de graduação em Ciência da Computação com ênfase em pesquisa e desenvolvimento', 3200, 5, '2019-01-01'),
('Sistemas de Informação', 'Curso de graduação em Sistemas de Informação com foco em gestão de TI', 3000, 5, '2021-01-01'),
('Letras - Português', 'Curso de graduação em Letras com habilitação em Língua Portuguesa', 2800, 4, '2018-01-01'),
('Pedagogia', 'Curso de graduação em Pedagogia para formação de professores', 3000, 23, '2022-01-01');

INSERT INTO disciplina (nome, ementa, carga_horaria) VALUES
('Algoritmos e Programação I', 'Introdução à lógica de programação e algoritmos. Linguagem C. Estruturas de controle. Funções.', 80),
('Banco de Dados I', 'Conceitos fundamentais de bancos de dados. Modelo relacional. SQL. Normalização.', 60),
('Engenharia de Software I', 'Processos de desenvolvimento de software. Metodologias ágeis. Requisitos.', 60),
('Didática Geral', 'Fundamentos da didática e práticas pedagógicas', 60),
('Psicologia da Educação', 'Estudo dos processos psicológicos envolvidos na educação', 60),
('Tecnologias Educacionais', 'Uso de tecnologias no processo de ensino-aprendizagem', 60),
('Cálculo I', 'Limites, derivadas e integrais. Aplicações em problemas reais', 80);