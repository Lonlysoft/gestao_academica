-- popular banco

-- Script de População do Banco de Dados - Gestão Acadêmica
USE gestao_academica;

-- Inserir Administradores
INSERT INTO usuario (nome, email, senha, tipo) VALUES
('Maria Administradora', 'maria.admin@universidade.edu.br', 'admin123', 'admin'),
('Carlos Coordenador', 'carlos.coord@universidade.edu.br', 'admin123', 'admin');

INSERT INTO administrador (id_administrador, departamento, nivel_acesso) VALUES
(1, 'TI', 'total'),
(2, 'Acadêmico', 'total');

-- Inserir Professores
INSERT INTO usuario (nome, email, senha, tipo) VALUES
('Dr. João Silva', 'joao.silva@universidade.edu.br', 'prof123', 'professor'),
('Dra. Ana Santos', 'ana.santos@universidade.edu.br', 'prof123', 'professor'),
('Prof. Carlos Oliveira', 'carlos.oliveira@universidade.edu.br', 'prof123', 'professor'),
('Dra. Mariana Costa', 'mariana.costa@universidade.edu.br', 'prof123', 'professor'),
('Dr. Pedro Alves', 'pedro.alves@universidade.edu.br', 'prof123', 'professor'),
('Prof. Fernando Lima', 'fernando.lima@universidade.edu.br', 'prof123', 'professor'),
('Dra. Juliana Pereira', 'juliana.pereira@universidade.edu.br', 'prof123', 'professor'),
('Dr. Roberto Martins', 'roberto.martins@universidade.edu.br', 'prof123', 'professor'),
('Dra. Patricia Rocha', 'patricia.rocha@universidade.edu.br', 'prof123', 'professor'),
('Prof. Ricardo Ferreira', 'ricardo.ferreira@universidade.edu.br', 'prof123', 'professor');

INSERT INTO professor (id_professor, especialidade, data_contratacao, formacao, regime_trabalho) VALUES
(3, 'Matemática Aplicada', '2018-03-15', 'Doutor em Matemática', 'integral'),
(4, 'Literatura Brasileira', '2019-08-01', 'Doutora em Letras', 'integral'),
(5, 'Banco de Dados', '2020-02-10', 'Mestre em Ciência da Computação', 'integral'),
(6, 'Física Quântica', '2017-11-20', 'Doutor em Física', 'integral'),
(7, 'Engenharia de Software', '2021-01-15', 'Doutora em Computação', 'integral'),
(8, 'Algoritmos', '2019-06-01', 'Mestre em Ciência da Computação', 'parcial'),
(9, 'Estruturas de Dados', '2018-09-10', 'Doutor em Computação', 'integral'),
(10, 'Redes de Computadores', '2020-03-22', 'Mestre em Engenharia de Telecom', 'integral'),
(11, 'Inteligência Artificial', '2022-01-08', 'Doutor em IA', 'integral'),
(12, 'Estatística', '2019-04-15', 'Doutor em Estatística', 'parcial');

-- Inserir Alunos
INSERT INTO usuario (nome, email, senha, tipo) VALUES
('Aluno Teste 01', 'aluno01@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 02', 'aluno02@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 03', 'aluno03@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 04', 'aluno04@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 05', 'aluno05@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 06', 'aluno06@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 07', 'aluno07@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 08', 'aluno08@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 09', 'aluno09@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 10', 'aluno10@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 11', 'aluno11@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 12', 'aluno12@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 13', 'aluno13@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 14', 'aluno14@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 15', 'aluno15@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 16', 'aluno16@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 17', 'aluno17@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 18', 'aluno18@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 19', 'aluno19@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 20', 'aluno20@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 21', 'aluno21@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 22', 'aluno22@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 23', 'aluno23@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 24', 'aluno24@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 25', 'aluno25@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 26', 'aluno26@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 27', 'aluno27@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 28', 'aluno28@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 29', 'aluno29@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 30', 'aluno30@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 31', 'aluno31@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 32', 'aluno32@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 33', 'aluno33@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 34', 'aluno34@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 35', 'aluno35@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 36', 'aluno36@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 37', 'aluno37@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 38', 'aluno38@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 39', 'aluno39@universidade.edu.br', 'aluno123', 'aluno'),
('Aluno Teste 40', 'aluno40@universidade.edu.br', 'aluno123', 'aluno');

INSERT INTO aluno (id_aluno, data_ingresso, status, ra) VALUES
(13, '2024-01-15', 'ativo', '20240001'),
(14, '2024-01-15', 'ativo', '20240002'),
(15, '2024-01-15', 'ativo', '20240003'),
(16, '2024-01-15', 'ativo', '20240004'),
(17, '2024-01-15', 'ativo', '20240005'),
(18, '2024-01-15', 'ativo', '20240006'),
(19, '2024-01-15', 'ativo', '20240007'),
(20, '2024-01-15', 'ativo', '20240008'),
(21, '2024-01-15', 'ativo', '20240009'),
(22, '2024-01-15', 'ativo', '20240010'),
(23, '2024-01-15', 'ativo', '20240011'),
(24, '2024-01-15', 'ativo', '20240012'),
(25, '2024-01-15', 'ativo', '20240013'),
(26, '2024-01-15', 'ativo', '20240014'),
(27, '2024-01-15', 'ativo', '20240015'),
(28, '2024-01-15', 'ativo', '20240016'),
(29, '2024-01-15', 'ativo', '20240017'),
(30, '2024-01-15', 'ativo', '20240018'),
(31, '2024-01-15', 'ativo', '20240019'),
(32, '2024-01-15', 'ativo', '20240020'),
(33, '2024-01-15', 'ativo', '20240021'),
(34, '2024-01-15', 'ativo', '20240022'),
(35, '2024-01-15', 'ativo', '20240023'),
(36, '2024-01-15', 'ativo', '20240024'),
(37, '2024-01-15', 'ativo', '20240025'),
(38, '2024-01-15', 'ativo', '20240026'),
(39, '2024-01-15', 'ativo', '20240027'),
(40, '2024-01-15', 'ativo', '20240028'),
(41, '2024-01-15', 'ativo', '20240029'),
(42, '2024-01-15', 'ativo', '20240030'),
(43, '2024-01-15', 'ativo', '20240031'),
(44, '2024-01-15', 'ativo', '20240032'),
(45, '2024-01-15', 'ativo', '20240033'),
(46, '2024-01-15', 'ativo', '20240034'),
(47, '2024-01-15', 'ativo', '20240035'),
(48, '2024-01-15', 'ativo', '20240036'),
(49, '2024-01-15', 'ativo', '20240037'),
(50, '2024-01-15', 'ativo', '20240038'),
(51, '2024-01-15', 'ativo', '20240039'),
(52, '2024-01-15', 'ativo', '20240040');

-- Inserir Cursos
INSERT INTO curso (nome, descricao, carga_horaria_total, coordenador_id, data_criacao) VALUES
('Engenharia de Software', 'Curso de graduação em Engenharia de Software com foco em desenvolvimento de sistemas', 3600, 7, '2020-01-01'),
('Ciência da Computação', 'Curso de graduação em Ciência da Computação com ênfase em pesquisa e desenvolvimento', 3200, 9, '2019-01-01'),
('Sistemas de Informação', 'Curso de graduação em Sistemas de Informação com foco em gestão de TI', 3000, 5, '2021-01-01'),
('Letras - Português', 'Curso de graduação em Letras com habilitação em Língua Portuguesa', 2800, 4, '2018-01-01');

-- Inserir Disciplinas
INSERT INTO disciplina (nome, ementa, carga_horaria) VALUES
('Algoritmos e Programação I', 'Introdução à lógica de programação e algoritmos. Linguagem C. Estruturas de controle. Funções.', 80),
('Banco de Dados I', 'Conceitos fundamentais de bancos de dados. Modelo relacional. SQL. Normalização.', 60),
('Engenharia de Software I', 'Processos de desenvolvimento de software. Metodologias ágeis. Requisitos.', 60),
('Estruturas de Dados', 'Listas, pilhas, filas, árvores, grafos. Algoritmos de ordenação e busca.', 80),
('Redes de Computadores', 'Fundamentos de redes. Protocolos TCP/IP. Arquitetura de redes.', 60),
('Inteligência Artificial', 'Introdução à IA. Algoritmos de busca. Aprendizado de máquina.', 60),
('Literatura Brasileira I', 'Estudo da literatura brasileira desde o período colonial até o modernismo.', 60),
('Língua Portuguesa I', 'Estudo da gramática e produção textual em língua portuguesa.', 60),
('Cálculo I', 'Limites, derivadas e integrais. Aplicações em problemas reais.', 80),
('Estatística Básica', 'Conceitos fundamentais de estatística. Probabilidade. Análise de dados.', 60);

-- Inserir Grade Curricular
INSERT INTO grade_curricular (id_curso, id_disciplina, semestre_ideal, obrigatoria, carga_horaria_semestral) VALUES
-- Engenharia de Software
(1, 1, 1, TRUE, 80),
(1, 9, 1, TRUE, 80),
(1, 2, 2, TRUE, 60),
(1, 4, 2, TRUE, 80),
(1, 3, 3, TRUE, 60),
(1, 5, 3, TRUE, 60),
(1, 6, 4, TRUE, 60),
(1, 10, 4, TRUE, 60),

-- Ciência da Computação
(2, 1, 1, TRUE, 80),
(2, 9, 1, TRUE, 80),
(2, 4, 2, TRUE, 80),
(2, 6, 3, TRUE, 60),
(2, 10, 3, TRUE, 60),

-- Sistemas de Informação
(3, 1, 1, TRUE, 80),
(3, 2, 2, TRUE, 60),
(3, 3, 3, TRUE, 60),
(3, 5, 3, TRUE, 60),

-- Letras
(4, 7, 1, TRUE, 60),
(4, 8, 1, TRUE, 60);

-- Inserir Turmas
INSERT INTO turma (codigo_turma, periodo, horario, vagas_totais, vagas_ocupadas, id_curso, id_professor, id_disciplina, data_inicio, data_termino) VALUES
('ESW001', '2024.1', 'Segunda 14:00-16:00, Quarta 14:00-16:00', 30, 25, 1, 3, 1, '2024-02-01', '2024-06-30'),
('CC001', '2024.1', 'Terça 10:00-12:00, Quinta 10:00-12:00', 25, 20, 2, 5, 2, '2024-02-01', '2024-06-30'),
('LET001', '2024.1', 'Segunda 08:00-10:00, Sexta 08:00-10:00', 20, 15, 4, 4, 7, '2024-02-01', '2024-06-30');

-- Matricular 32 alunos
-- Turma 1: Engenharia de Software - Algoritmos (15 alunos)
INSERT INTO matricula (id_aluno, id_turma, status, prioridade) VALUES
(13, 1, 'matriculado', 'normal'),
(14, 1, 'matriculado', 'normal'),
(15, 1, 'matriculado', 'normal'),
(16, 1, 'matriculado', 'normal'),
(17, 1, 'matriculado', 'normal'),
(18, 1, 'matriculado', 'normal'),
(19, 1, 'matriculado', 'normal'),
(20, 1, 'matriculado', 'normal'),
(21, 1, 'matriculado', 'normal'),
(22, 1, 'matriculado', 'normal'),
(23, 1, 'matriculado', 'normal'),
(24, 1, 'matriculado', 'normal'),
(25, 1, 'matriculado', 'normal'),
(26, 1, 'matriculado', 'normal'),
(27, 1, 'matriculado', 'normal');

-- Turma 2: Ciência da Computação - Banco de Dados (12 alunos)
INSERT INTO matricula (id_aluno, id_turma, status, prioridade) VALUES
(28, 2, 'matriculado', 'normal'),
(29, 2, 'matriculado', 'normal'),
(30, 2, 'matriculado', 'normal'),
(31, 2, 'matriculado', 'normal'),
(32, 2, 'matriculado', 'normal'),
(33, 2, 'matriculado', 'normal'),
(34, 2, 'matriculado', 'normal'),
(35, 2, 'matriculado', 'normal'),
(36, 2, 'matriculado', 'normal'),
(37, 2, 'matriculado', 'normal'),
(38, 2, 'matriculado', 'normal'),
(39, 2, 'matriculado', 'normal');

-- Turma 3: Letras - Literatura Brasileira (5 alunos)
INSERT INTO matricula (id_aluno, id_turma, status, prioridade) VALUES
(40, 3, 'matriculado', 'normal'),
(41, 3, 'matriculado', 'normal'),
(42, 3, 'matriculado', 'normal'),
(43, 3, 'matriculado', 'normal'),
(44, 3, 'matriculado', 'normal');

-- Atualizar contador de vagas ocupadas
UPDATE turma SET vagas_ocupadas = 15 WHERE id_turma = 1;
UPDATE turma SET vagas_ocupadas = 12 WHERE id_turma = 2;
UPDATE turma SET vagas_ocupadas = 5 WHERE id_turma = 3;

-- Inserir Materiais de Aula
INSERT INTO material_aula (titulo, descricao, arquivo_url, tipo_arquivo, id_turma, id_professor) VALUES
('Slides Aula 1 - Introdução a Algoritmos', 'Conceitos básicos de algoritmos e lógica de programação', '/materiais/algoritmos/aula1.pdf', 'pdf', 1, 3),
('Exercícios Aula 1', 'Lista de exercícios para prática dos conceitos aprendidos', '/materiais/algoritmos/exercicios1.pdf', 'pdf', 1, 3),
('Vídeo: Estruturas Condicionais', 'Vídeo explicativo sobre if/else e switch case', '/materiais/algoritmos/video_condicionais.mp4', 'video', 1, 3),
('Slides Banco de Dados - Modelo Relacional', 'Conceitos do modelo relacional e normalização', '/materiais/bd/modelo_relacional.pdf', 'pdf', 2, 5),
('Script SQL - Criação de Tabelas', 'Exemplos práticos de criação de tabelas em SQL', '/materiais/bd/script_tabelas.sql', 'sql', 2, 5),
('Artigo: História do SQL', 'Artigo sobre a evolução da linguagem SQL', '/materiais/bd/historia_sql.pdf', 'pdf', 2, 5),
('Slides Literatura Brasileira - Romantismo', 'Características do período romântico na literatura brasileira', '/materiais/literatura/romantismo.pdf', 'pdf', 3, 4),
('Textos: Poemas Românticos', 'Seleção de poemas representativos do romantismo', '/materiais/literatura/poemas_romanticos.pdf', 'pdf', 3, 4),
('Guia de Análise Literária', 'Metodologia para análise de textos literários', '/materiais/literatura/guia_analise.pdf', 'pdf', 3, 4),
('Exercícios Práticos - SQL', 'Exercícios para fixação dos comandos SQL', '/materiais/bd/exercicios_sql.pdf', 'pdf', 2, 5);

-- Inserir Avaliações
INSERT INTO avaliacao (titulo, descricao, tipo, data_avaliacao, peso, id_turma, valor_maximo) VALUES
('Prova 1 - Algoritmos', 'Primeira prova sobre conceitos básicos de algoritmos', 'prova', '2024-03-15', 0.3, 1, 10.0),
('Trabalho Prático - Sistema Bancário', 'Desenvolvimento de um sistema bancário simples em C', 'trabalho', '2024-04-20', 0.4, 1, 10.0),
('Prova 1 - Banco de Dados', 'Prova sobre modelo relacional e SQL básico', 'prova', '2024-03-20', 0.35, 2, 10.0),
('Trabalho - Modelagem de Dados', 'Modelagem de um sistema acadêmico com DER e modelo relacional', 'trabalho', '2024-04-25', 0.45, 2, 10.0);

-- Inserir Notas para as avaliações 
-- Notas para Prova 1 - Algoritmos (Turma 1)
INSERT INTO nota (id_aluno, id_avaliacao, valor_nota) VALUES
(13, 1, 8.5), (14, 1, 7.0), (15, 1, 9.2), (16, 1, 6.8), (17, 1, 8.0),
(18, 1, 4.5), (19, 1, 7.8), (20, 1, 9.5), (21, 1, 5.5), (22, 1, 8.2),
(23, 1, 7.5), (24, 1, 6.0), (25, 1, 8.8), (26, 1, 3.5), (27, 1, 9.0);

-- Notas para Prova 1 - Banco de Dados (Turma 2)
INSERT INTO nota (id_aluno, id_avaliacao, valor_nota) VALUES
(28, 3, 7.5), (29, 3, 8.0), (30, 3, 9.2), (31, 3, 6.5), (32, 3, 8.8),
(33, 3, 4.0), (34, 3, 7.0), (35, 3, 9.5), (36, 3, 5.8), (37, 3, 8.5),
(38, 3, 7.2), (39, 3, 6.8);

-- Inserir frequências
INSERT INTO frequencia (id_aluno, id_turma, data_aula, presente) VALUES

(13, 1, '2024-03-01', TRUE), (14, 1, '2024-03-01', TRUE), (15, 1, '2024-03-01', FALSE),
(13, 1, '2024-03-06', TRUE), (14, 1, '2024-03-06', TRUE), (15, 1, '2024-03-06', TRUE),
(13, 1, '2024-03-08', TRUE), (14, 1, '2024-03-08', FALSE), (15, 1, '2024-03-08', TRUE);

-- Inserir algumas respostas de atividades
INSERT INTO resposta_atividade (id_aluno, id_avaliacao, resposta, data_limite) VALUES
(13, 2, 'Sistema bancário implementado em C com funções de depósito, saque e saldo', '2024-04-20'),
(14, 2, 'Implementação do sistema bancário com menu interativo', '2024-04-20'),
(28, 4, 'Modelo DER para sistema acadêmico com entidades: aluno, professor, curso, disciplina', '2024-04-25');

-- Adicionar um usuário que é tanto professor quanto aluno (só para ter o exemplo multi papéis)
INSERT INTO usuario (nome, email, senha, tipo) VALUES
('Prof. Aluno Exemplo', 'prof.aluno@universidade.edu.br', 'senha123', 'professor');

INSERT INTO professor (id_professor, especialidade, data_contratacao, formacao) VALUES
(53, 'Educação', '2023-01-15', 'Mestre em Educação');

UPDATE usuario SET tipo = 'professor' WHERE id_usuario = 53;

INSERT INTO solicitacao_vagas (id_aluno, id_turma, mensagem, status) VALUES
(45, 1, 'Gostaria de me matricular na turma de Algoritmos, mesmo estando lotada', 'pendente'),
(46, 2, 'Necessito cursar Banco de Dados neste semestre', 'pendente');

UPDATE matricula SET status = 'reprovado', nota_final = 4.0 WHERE id_aluno IN (26, 33);

INSERT INTO avaliacao (titulo, descricao, tipo, data_avaliacao, peso, id_turma, valor_maximo) VALUES
('Prova 2 - Algoritmos', 'Segunda prova sobre estruturas de repetição e funções', 'prova', '2024-05-10', 0.3, 1, 10.0),
('Exercício Prático - SQL', 'Exercício avaliativo sobre consultas SQL avançadas', 'trabalho', '2024-04-15', 0.2, 2, 10.0);

INSERT INTO nota (id_aluno, id_avaliacao, valor_nota) VALUES
(13, 5, 9.0), (14, 5, 8.5), (15, 5, 7.8),
(28, 6, 8.0), (29, 6, 9.2), (30, 6, 7.5);

UPDATE matricula m 
SET nota_final = (
    SELECT AVG(n.valor_nota) 
    FROM nota n 
    JOIN avaliacao a ON n.id_avaliacao = a.id_avaliacao 
    WHERE n.id_aluno = m.id_aluno AND a.id_turma = m.id_turma
)
WHERE m.status = 'matriculado';

SELECT 
    (SELECT COUNT(*) FROM usuario WHERE tipo = 'admin') as total_admins,
    (SELECT COUNT(*) FROM usuario WHERE tipo = 'professor') as total_professores,
    (SELECT COUNT(*) FROM usuario WHERE tipo = 'aluno') as total_alunos,
    (SELECT COUNT(*) FROM curso) as total_cursos,
    (SELECT COUNT(*) FROM turma) as total_turmas,
    (SELECT COUNT(*) FROM matricula WHERE status = 'matriculado') as matriculas_ativas,
    (SELECT COUNT(*) FROM avaliacao) as total_avaliacoes,
    (SELECT COUNT(*) FROM material_aula) as total_materiais;

SELECT 
    t.codigo_turma,
    c.nome as curso,
    d.nome as disciplina,
    COUNT(m.id_matricula) as alunos_matriculados,
    t.vagas_totais,
    ROUND((COUNT(m.id_matricula) * 100.0 / t.vagas_totais), 2) as percentual_ocupacao
FROM turma t
JOIN curso c ON t.id_curso = c.id_curso
JOIN disciplina d ON t.id_disciplina = d.id_disciplina
LEFT JOIN matricula m ON t.id_turma = m.id_turma AND m.status = 'matriculado'
GROUP BY t.id_turma;