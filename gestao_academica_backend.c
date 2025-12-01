#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql/mysql.h>

#define MAX_STRING 500
#define MAX_QUERY 2000

// Estruturas de dados
typedef struct {
	int id;
	char nome[MAX_STRING];
	char email[MAX_STRING];
	char tipo[20];
	int ativo;
} Usuario;

typedef struct {
	int id;
	char codigo[20];
	char periodo[10];
	int vagas_totais;
	int vagas_ocupadas;
	int id_curso;
	int id_professor;
	char nome_curso[MAX_STRING];
	char nome_professor[MAX_STRING];
} Turma;

typedef struct {
	int id;
	char titulo[MAX_STRING];
	char tipo[20];
	char data_avaliacao[20];
	float peso;
} Avaliacao;

// Variável global para conexão com o banco
MYSQL *conn;

// Funções de utilidade
void limpar_buffer() {
	int c;
	while ((c = getchar()) != '\n' && c != EOF);
}

void pressione_para_continuar() {
	printf("\nPressione Enter para continuar...");
	limpar_buffer();
	getchar();
}

// Funções de conexão com o banco
int conectar_banco() {
	conn = mysql_init(NULL);
	if (conn == NULL) {
		fprintf(stderr, "Erro ao inicializar conexão: %s\n", mysql_error(conn));
		return 0;
	}

	if (mysql_real_connect(conn, "localhost", "root", "sql123", "gestao_academica", 0, NULL, 0) == NULL) {
		fprintf(stderr, "Erro ao conectar: %s\n", mysql_error(conn));
		mysql_close(conn);
		return 0;
	}
	return 1;
}

// Funções de autenticação
Usuario* fazer_login() {
	char email[MAX_STRING], senha[MAX_STRING];
	static Usuario usuario;
	
	printf("=== LOGIN ===\n");
	printf("Email: ");
	scanf("%s", email);
	printf("Senha: ");
	scanf("%s", senha);

	char query[MAX_QUERY];
	snprintf(query, sizeof(query), 
			 "SELECT id_usuario, nome, email, tipo FROM usuario WHERE email = '%s' AND senha = '%s' AND ativo = 1", 
			 email, senha);

	if (mysql_query(conn, query)) {
		fprintf(stderr, "Erro na query: %s\n", mysql_error(conn));
		return NULL;
	}

	MYSQL_RES *result = mysql_store_result(conn);
	if (result == NULL) {
		fprintf(stderr, "Erro ao armazenar resultado: %s\n", mysql_error(conn));
		return NULL;
	}

	MYSQL_ROW row = mysql_fetch_row(result);
	if (row) {
		usuario.id = atoi(row[0]);
		strcpy(usuario.nome, row[1]);
		strcpy(usuario.email, row[2]);
		strcpy(usuario.tipo, row[3]);
		usuario.ativo = 1;
		mysql_free_result(result);
		return &usuario;
	}

	mysql_free_result(result);
	printf("Email ou senha inválidos!\n");
	return NULL;
}

// Funções do Administrador
void cadastrar_usuario() {
	char nome[MAX_STRING], email[MAX_STRING], senha[MAX_STRING], tipo[20];
	
	printf("=== CADASTRAR USUÁRIO ===\n");
	printf("Nome: ");
	scanf(" %[^\n]", nome);
	printf("Email: ");
	scanf("%s", email);
	printf("Senha: ");
	scanf("%s", senha);
	printf("Tipo (admin/professor/aluno): ");
	scanf("%s", tipo);

	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "INSERT INTO usuario (nome, email, senha, tipo) VALUES ('%s', '%s', '%s', '%s')",
			 nome, email, senha, tipo);

	if (mysql_query(conn, query)) {
		printf("Erro ao cadastrar usuário: %s\n", mysql_error(conn));
	} else {
		printf("Usuário cadastrado com sucesso!\n");
		
		// Se for aluno, cadastrar na tabela aluno
		if (strcmp(tipo, "aluno") == 0) {
			int id_usuario = mysql_insert_id(conn);
			char ra[20];
			snprintf(ra, sizeof(ra), "2024%05d", id_usuario);
			
			snprintf(query, sizeof(query),
					 "INSERT INTO aluno (id_aluno, data_ingresso, status, ra) VALUES (%d, CURDATE(), 'ativo', '%s')",
					 id_usuario, ra);
			mysql_query(conn, query);
		}
		// Se for professor, cadastrar na tabela professor
		else if (strcmp(tipo, "professor") == 0) {
			int id_usuario = mysql_insert_id(conn);
			snprintf(query, sizeof(query),
					 "INSERT INTO professor (id_professor, data_contratacao) VALUES (%d, CURDATE())",
					 id_usuario);
			mysql_query(conn, query);
		}
	}
}

void gerenciar_cursos() {
	int opcao;
	do {
		printf("\n=== GERENCIAR CURSOS ===\n");
		printf("1. Listar cursos\n");
		printf("2. Cadastrar curso\n");
		printf("3. Voltar\n");
		printf("Escolha: ");
		scanf("%d", &opcao);

		if (opcao == 1) {
			// Listar cursos
			char query[] = "SELECT c.id_curso, c.nome, c.carga_horaria_total, u.nome FROM curso c LEFT JOIN professor u ON c.coordenador_id = u.id_professor";
			mysql_query(conn, query);
			MYSQL_RES *result = mysql_store_result(conn);
			printf("\n--- CURSOS ---\n");
			while (mysql_fetch_row(result)) {
				MYSQL_ROW row = mysql_fetch_row(result);
				printf("ID: %s | Nome: %s | Carga: %sh | Coordenador: %s\n", 
					   row[0], row[1], row[2], row[3] ? row[3] : "N/A");
			}
			mysql_free_result(result);
		} else if (opcao == 2) {
			// Cadastrar curso
			char nome[MAX_STRING], descricao[MAX_STRING];
			int carga_horaria;
			
			printf("Nome do curso: ");
			scanf(" %[^\n]", nome);
			printf("Descrição: ");
			scanf(" %[^\n]", descricao);
			printf("Carga horária total: ");
			scanf("%d", &carga_horaria);
			
			char query[MAX_QUERY];
			snprintf(query, sizeof(query),
					 "INSERT INTO curso (nome, descricao, carga_horaria_total, data_criacao) VALUES ('%s', '%s', %d, CURDATE())",
					 nome, descricao, carga_horaria);
			
			if (mysql_query(conn, query)) {
				printf("Erro ao cadastrar curso: %s\n", mysql_error(conn));
			} else {
				printf("Curso cadastrado com sucesso!\n");
			}
		}
	} while (opcao != 3);
}

void criar_turma() {
	printf("\n=== CRIAR TURMA ===\n");
	
	// Listar cursos
	printf("Cursos disponíveis:\n");
	mysql_query(conn, "SELECT id_curso, nome FROM curso WHERE ativo = 1");
	MYSQL_RES *result = mysql_store_result(conn);
	while (mysql_fetch_row(result)) {
		MYSQL_ROW row = mysql_fetch_row(result);
		printf("ID: %s - %s\n", row[0], row[1]);
	}
	mysql_free_result(result);
	
	// Listar professores
	printf("\nProfessores disponíveis:\n");
	mysql_query(conn, "SELECT u.id_usuario, u.nome FROM usuario u JOIN professor p ON u.id_usuario = p.id_professor WHERE u.ativo = 1");
	result = mysql_store_result(conn);
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("ID: %s - %s\n", row[0], row[1]);
	}
	mysql_free_result(result);
	
	// Listar disciplinas
	printf("\nDisciplinas disponíveis:\n");
	mysql_query(conn, "SELECT id_disciplina, nome FROM disciplina WHERE ativo = 1");
	result = mysql_store_result(conn);
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("ID: %s - %s\n", row[0], row[1]);
	}
	mysql_free_result(result);
	
	char codigo[20], periodo[10], horario[50];
	int vagas, id_curso, id_professor, id_disciplina;
	
	printf("\nCódigo da turma: ");
	scanf("%s", codigo);
	printf("Período (ex: 2024.1): ");
	scanf("%s", periodo);
	printf("Horário: ");
	scanf(" %[^\n]", horario);
	printf("Vagas totais: ");
	scanf("%d", &vagas);
	printf("ID do curso: ");
	scanf("%d", &id_curso);
	printf("ID do professor: ");
	scanf("%d", &id_professor);
	printf("ID da disciplina: ");
	scanf("%d", &id_disciplina);
	
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "INSERT INTO turma (codigo_turma, periodo, horario, vagas_totais, id_curso, id_professor, id_disciplina, data_inicio) VALUES ('%s', '%s', '%s', %d, %d, %d, %d, CURDATE())",
			 codigo, periodo, horario, vagas, id_curso, id_professor, id_disciplina);
	
	if (mysql_query(conn, query)) {
		printf("Erro ao criar turma: %s\n", mysql_error(conn));
	} else {
		printf("Turma criada com sucesso!\n");
	}
}

// Funções do Professor
void professor_turmas(Usuario *professor) {
	printf("\n=== MINHAS TURMAS ===\n");
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "SELECT t.id_turma, t.codigo_turma, c.nome, t.periodo, t.vagas_ocupadas, t.vagas_totais "
			 "FROM turma t JOIN curso c ON t.id_curso = c.id_curso "
			 "WHERE t.id_professor = %d AND t.ativa = 1", professor->id);
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("ID: %s | Código: %s | Curso: %s | Período: %s | Vagas: %s/%s\n",
			   row[0], row[1], row[2], row[3], row[4], row[5]);
	}
	mysql_free_result(result);
}

void cadastrar_avaliacao(Usuario *professor) {
	printf("\n=== CADASTRAR AVALIAÇÃO ===\n");
	
	// Listar turmas do professor
	professor_turmas(professor);
	
	int id_turma;
	char titulo[MAX_STRING], descricao[MAX_STRING], tipo[20], data[20];
	float peso;
	
	printf("ID da turma: ");
	scanf("%d", &id_turma);
	printf("Título: ");
	scanf(" %[^\n]", titulo);
	printf("Descrição: ");
	scanf(" %[^\n]", descricao);
	printf("Tipo (prova/trabalho/apresentacao/participacao): ");
	scanf("%s", tipo);
	printf("Data (YYYY-MM-DD): ");
	scanf("%s", data);
	printf("Peso (ex: 0.3 para 30%%): ");
	scanf("%f", &peso);
	
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "INSERT INTO avaliacao (titulo, descricao, tipo, data_avaliacao, peso, id_turma) "
			 "VALUES ('%s', '%s', '%s', '%s', %.2f, %d)",
			 titulo, descricao, tipo, data, peso, id_turma);
	
	if (mysql_query(conn, query)) {
		printf("Erro ao cadastrar avaliação: %s\n", mysql_error(conn));
	} else {
		printf("Avaliação cadastrada com sucesso!\n");
	}
}

void registrar_notas(Usuario *professor) {
	printf("\n=== REGISTRAR NOTAS ===\n");
	
	// Listar avaliações do professor
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "SELECT a.id_avaliacao, a.titulo, t.codigo_turma "
			 "FROM avaliacao a JOIN turma t ON a.id_turma = t.id_turma "
			 "WHERE t.id_professor = %d", professor->id);
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	printf("Avaliações:\n");
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("ID: %s | %s - Turma: %s\n", row[0], row[1], row[2]);
	}
	mysql_free_result(result);
	
	int id_avaliacao;
	printf("ID da avaliação: ");
	scanf("%d", &id_avaliacao);
	
	// Listar alunos da turma
	snprintf(query, sizeof(query),
			 "SELECT u.id_usuario, u.nome, m.id_matricula "
			 "FROM usuario u JOIN aluno a ON u.id_usuario = a.id_aluno "
			 "JOIN matricula m ON a.id_aluno = m.id_aluno "
			 "JOIN avaliacao av ON m.id_turma = av.id_turma "
			 "WHERE av.id_avaliacao = %d AND m.status = 'matriculado'", id_avaliacao);
	
	mysql_query(conn, query);
	result = mysql_store_result(conn);
	
	printf("\nAlunos para avaliação:\n");
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("ID: %s | Nome: %s\n", row[0], row[1]);
		
		float nota;
		printf("Nota para %s: ", row[1]);
		scanf("%f", &nota);
		
		char insert_query[MAX_QUERY];
		snprintf(insert_query, sizeof(insert_query),
				 "INSERT INTO nota (id_aluno, id_avaliacao, valor_nota) VALUES (%s, %d, %.2f) "
				 "ON DUPLICATE KEY UPDATE valor_nota = %.2f",
				 row[0], id_avaliacao, nota, nota);
		mysql_query(conn, insert_query);
	}
	mysql_free_result(result);
	printf("Notas registradas com sucesso!\n");
}

// Funções do Aluno
void matricular_turma(Usuario *aluno) {
	printf("\n=== MATRÍCULA EM TURMA ===\n");
	
	// Verificar se é reprovado para dar prioridade
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "SELECT COUNT(*) FROM matricula WHERE id_aluno = %d AND status = 'reprovado'", aluno->id);
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	MYSQL_ROW row = mysql_fetch_row(result);
	int eh_reprovado = atoi(row[0]) > 0;
	mysql_free_result(result);
	
	// Listar turmas disponíveis
	printf("Turmas disponíveis:\n");
	snprintf(query, sizeof(query),
			 "SELECT t.id_turma, t.codigo_turma, c.nome, d.nome, u.nome, t.vagas_ocupadas, t.vagas_totais "
			 "FROM turma t JOIN curso c ON t.id_curso = c.id_curso "
			 "JOIN disciplina d ON t.id_disciplina = d.id_disciplina "
			 "JOIN usuario u ON t.id_professor = u.id_usuario "
			 "WHERE t.ativa = 1 AND t.vagas_ocupadas < t.vagas_totais");
	
	mysql_query(conn, query);
	result = mysql_store_result(conn);
	
	while (row = mysql_fetch_row(result)) {
		printf("ID: %s | %s - %s (%s) | Prof: %s | Vagas: %s/%s\n",
			   row[0], row[1], row[2], row[3], row[4], row[5], row[6]);
	}
	mysql_free_result(result);
	
	int id_turma;
	printf("\nID da turma para matrícula: ");
	scanf("%d", &id_turma);
	
	// Tentar matricular
	snprintf(query, sizeof(query),
			 "INSERT INTO matricula (id_aluno, id_turma, status, prioridade) "
			 "VALUES (%d, %d, 'matriculado', '%s')",
			 aluno->id, id_turma, eh_reprovado ? "reprovado" : "normal");
	
	if (mysql_query(conn, query)) {
		printf("Erro na matrícula: %s\n", mysql_error(conn));
		
		// Se falhou por vagas, criar solicitação
		if (strstr(mysql_error(conn), "vagas")) {
			printf("Turma lotada! Criando solicitação de vaga...\n");
			snprintf(query, sizeof(query),
					 "INSERT INTO solicitacao_vagas (id_aluno, id_turma, mensagem) "
					 "VALUES (%d, %d, 'Solicitação automática: turma lotada')",
					 aluno->id, id_turma);
			mysql_query(conn, query);
			printf("Solicitação enviada ao professor!\n");
		}
	} else {
		// Atualizar contador de vagas
		snprintf(query, sizeof(query),
				 "UPDATE turma SET vagas_ocupadas = vagas_ocupadas + 1 WHERE id_turma = %d", id_turma);
		mysql_query(conn, query);
		printf("Matrícula realizada com sucesso!\n");
	}
}

void visualizar_notas(Usuario *aluno) {
	printf("\n=== MINHAS NOTAS ===\n");
	
	char query[MAX_QUERY];
	snprintf(query, sizeof(query),
			 "SELECT a.titulo, t.codigo_turma, n.valor_nota, a.data_avaliacao "
			 "FROM nota n JOIN avaliacao a ON n.id_avaliacao = a.id_avaliacao "
			 "JOIN turma t ON a.id_turma = t.id_turma "
			 "WHERE n.id_aluno = %d", aluno->id);
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	printf("Avaliação | Turma | Nota | Data\n");
	printf("--------------------------------\n");
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("%s | %s | %s | %s\n", row[0], row[1], row[2], row[3]);
	}
	mysql_free_result(result);
}

// Funções de Relatórios
void relatorio_alunos_por_turma() {
	printf("\n=== ALUNOS POR TURMA ===\n");
	
	char query[] = "SELECT c.nome, t.codigo_turma, COUNT(m.id_matricula) as total_alunos "
				   "FROM curso c JOIN turma t ON c.id_curso = t.id_curso "
				   "JOIN matricula m ON t.id_turma = m.id_turma "
				   "WHERE m.status = 'matriculado' "
				   "GROUP BY c.nome, t.codigo_turma";
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("Curso: %s | Turma: %s | Alunos: %s\n", row[0], row[1], row[2]);
	}
	mysql_free_result(result);
}

void relatorio_medias_turmas() {
	printf("\n=== MÉDIAS POR TURMA ===\n");
	
	char query[] = "SELECT t.codigo_turma, c.nome, AVG(n.valor_nota) as media "
				   "FROM turma t JOIN curso c ON t.id_curso = c.id_curso "
				   "JOIN avaliacao a ON t.id_turma = a.id_turma "
				   "JOIN nota n ON a.id_avaliacao = n.id_avaliacao "
				   "GROUP BY t.codigo_turma, c.nome";
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("Turma: %s | Curso: %s | Média: %s\n", row[0], row[1], row[2]);
	}
	mysql_free_result(result);
}

void relatorio_alunos_abaixo_media() {
	printf("\n=== ALUNOS ABAIXO DA MÉDIA (<5) ===\n");
	
	char query[] = "SELECT u.nome, t.codigo_turma, AVG(n.valor_nota) as media "
				   "FROM usuario u JOIN nota n ON u.id_usuario = n.id_aluno "
				   "JOIN avaliacao a ON n.id_avaliacao = a.id_avaliacao "
				   "JOIN turma t ON a.id_turma = t.id_turma "
				   "GROUP BY u.nome, t.codigo_turma "
				   "HAVING media < 5.0";
	
	mysql_query(conn, query);
	MYSQL_RES *result = mysql_store_result(conn);
	
	while(mysql_fetch_row(result)){
		MYSQL_ROW row = mysql_fetch_result(result);
		printf("Aluno: %s | Turma: %s | Média: %s\n", row[0], row[1], row[2]);
	}
	mysql_free_result(result);
}

// Menu principal por tipo de usuário
void menu_administrador(Usuario *admin) {
	int opcao;
	do {
		printf("\n=== SISTEMA DE GESTÃO ACADÊMICA - ADMINISTRADOR ===\n");
		printf("1. Cadastrar usuário\n");
		printf("2. Gerenciar cursos\n");
		printf("3. Criar turma\n");
		printf("4. Relatório: Alunos por turma\n");
		printf("5. Relatório: Médias por turma\n");
		printf("6. Relatório: Alunos abaixo da média\n");
		printf("7. Sair\n");
		printf("Escolha: ");
		scanf("%d", &opcao);

		switch(opcao) {
			case 1: cadastrar_usuario(); break;
			case 2: gerenciar_cursos(); break;
			case 3: criar_turma(); break;
			case 4: relatorio_alunos_por_turma(); break;
			case 5: relatorio_medias_turmas(); break;
			case 6: relatorio_alunos_abaixo_media(); break;
			case 7: printf("Saindo...\n"); break;
			default: printf("Opção inválida!\n");
		}
		if (opcao != 7) pressione_para_continuar();
	} while (opcao != 7);
}

void menu_professor(Usuario *professor) {
	int opcao;
	do {
		printf("\n=== SISTEMA DE GESTÃO ACADÊMICA - PROFESSOR ===\n");
		printf("1. Minhas turmas\n");
		printf("2. Cadastrar avaliação\n");
		printf("3. Registrar notas\n");
		printf("4. Cadastrar material de aula\n");
		printf("5. Sair\n");
		printf("Escolha: ");
		scanf("%d", &opcao);

		switch(opcao) {
			case 1: professor_turmas(professor); break;
			case 2: cadastrar_avaliacao(professor); break;
			case 3: registrar_notas(professor); break;
			case 4: printf("Funcionalidade em desenvolvimento...\n"); break;
			case 5: printf("Saindo...\n"); break;
			default: printf("Opção inválida!\n");
		}
		if (opcao != 5) pressione_para_continuar();
	} while (opcao != 5);
}

void menu_aluno(Usuario *aluno) {
	int opcao;
	do {
		printf("\n=== SISTEMA DE GESTÃO ACADÊMICA - ALUNO ===\n");
		printf("1. Matricular em turma\n");
		printf("2. Visualizar minhas notas\n");
		printf("3. Ver turmas matriculadas\n");
		printf("4. Sair\n");
		printf("Escolha: ");
		scanf("%d", &opcao);

		switch(opcao) {
			case 1: matricular_turma(aluno); break;
			case 2: visualizar_notas(aluno); break;
			case 3: printf("Funcionalidade em desenvolvimento...\n"); break;
			case 4: printf("Saindo...\n"); break;
			default: printf("Opção inválida!\n");
		}
		if (opcao != 4) pressione_para_continuar();
	} while (opcao != 4);
}

int main() {
	printf("=== SISTEMA DE GESTÃO ACADÊMICA ===\n");
	
	if (!conectar_banco()) {
		printf("Erro ao conectar com o banco de dados!\n");
		return 1;
	}
	
	Usuario *usuario = fazer_login();
	if (usuario == NULL) {
		mysql_close(conn);
		return 1;
	}
	
	printf("\nBem-vindo, %s! (%s)\n", usuario->nome, usuario->tipo);
	
	// Direcionar para o menu apropriado
	if (strcmp(usuario->tipo, "admin") == 0) {
		menu_administrador(usuario);
	} else if (strcmp(usuario->tipo, "professor") == 0) {
		menu_professor(usuario);
	} else if (strcmp(usuario->tipo, "aluno") == 0) {
		menu_aluno(usuario);
	}
	
	mysql_close(conn);
	return 0;
}