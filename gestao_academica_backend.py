import mysql.connector
from mysql.connector import Error
# import getpass # para senhas, isso melhora a segurança, mas...
import sys

# Constantes
MAX_STRING = 500
MAX_QUERY = 2000

# Classes para as estruturas
class Usuario:
	def __init__(self):
		self.id = 0
		self.nome = ""
		self.email = ""
		self.tipo = ""
		self.ativo = 0

class Turma:
	def __init__(self):
		self.id = 0
		self.codigo = ""
		self.periodo = ""
		self.vagas_totais = 0
		self.vagas_ocupadas = 0
		self.id_curso = 0
		self.id_professor = 0
		self.nome_curso = ""
		self.nome_professor = ""

class Avaliacao:
	def __init__(self):
		self.id = 0
		self.titulo = ""
		self.tipo = ""
		self.data_avaliacao = ""
		self.peso = 0.0

# Variável global para se conectar com o banco
conn = None

# Funções de utilidade
def pressione_para_continuar():
	input("\nPressione Enter para continuar...")

# Funções de conexão com o banco
def conectar_banco():
	global conn
	try:
		conn = mysql.connector.connect(
			host="localhost",
			user="root",
			port=3306,
			password="sql123",
			database="gestao_academica"
		)
		return True
	except Error as e:
		print(f"Erro ao conectar: {e}")
		return False

# Funções de autenticação
def fazer_login():
	print("=== LOGIN ===")
	email = input("Email: ")
	senha = input("Senha: ")

	query = f"SELECT id_usuario, nome, email, tipo FROM usuario WHERE email = '{email}' AND senha = '{senha}' AND ativo = 1"
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		
		if result:
			usuario = Usuario()
			usuario.id = result[0]
			usuario.nome = result[1]
			usuario.email = result[2]
			usuario.tipo = result[3]
			usuario.ativo = 1
			cursor.close()
			return usuario
		else:
			print("Email ou senha inválidos!")
			return None
	except Error as e:
		print(f"Erro na query: {e}")
		return None

# Funções do Administrador
def cadastrar_usuario():
	print("=== CADASTRAR USUÁRIO ===")
	nome = input("Nome: ")
	email = input("Email: ")
	senha = input("Senha: ")
	tipo = input("Tipo (admin/professor/aluno): ")

	query = f"INSERT INTO usuario (nome, email, senha, tipo) VALUES ('{nome}', '{email}', '{senha}', '{tipo}')"
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		
		print("Usuário cadastrado com sucesso!")
		
		# Se for aluno, cadastrar na tabela aluno
		if tipo == "aluno":
			id_usuario = cursor.lastrowid
			ra = f"2024{id_usuario:05d}"
			
			query = f"INSERT INTO aluno (id_aluno, data_ingresso, status, ra) VALUES ({id_usuario}, CURDATE(), 'ativo', '{ra}')"
			cursor.execute(query)
			conn.commit()
		
		# Se for professor, cadastrar na tabela professor
		elif tipo == "professor":
			id_usuario = cursor.lastrowid
			query = f"INSERT INTO professor (id_professor, data_contratacao) VALUES ({id_usuario}, CURDATE())"
			cursor.execute(query)
			conn.commit()
		
		cursor.close()
		
	except Error as e:
		print(f"Erro ao cadastrar usuário: {e}")

def gerenciar_cursos():
	while True:
		print("\n=== GERENCIAR CURSOS ===")
		print("1. Listar cursos")
		print("2. Cadastrar curso")
		print("3. Voltar")
		opcao = input("Escolha: ")
		
		if opcao == "1":
			# Listar cursos
			query = "SELECT c.id_curso, c.nome, c.carga_horaria_total, u.nome FROM curso c LEFT JOIN professor u ON c.coordenador_id = u.id_professor"
			
			try:
				cursor = conn.cursor()
				cursor.execute(query)
				results = cursor.fetchall()
				
				print("\n--- CURSOS ---")
				for row in results:
					print(f"ID: {row[0]} | Nome: {row[1]} | Carga: {row[2]}h | Coordenador: {row[3] if row[3] else 'N/A'}")
				
				cursor.close()
			except Error as e:
				print(f"Erro ao listar cursos: {e}")
				
		elif opcao == "2":
			# Cadastrar curso
			nome = input("Nome do curso: ")
			descricao = input("Descrição: ")
			carga_horaria = int(input("Carga horária total: "))
			
			query = f"INSERT INTO curso (nome, descricao, carga_horaria_total, data_criacao) VALUES ('{nome}', '{descricao}', {carga_horaria}, CURDATE())"
			
			try:
				cursor = conn.cursor()
				cursor.execute(query)
				conn.commit()
				print("Curso cadastrado com sucesso!")
				cursor.close()
			except Error as e:
				print(f"Erro ao cadastrar curso: {e}")
				
		elif opcao == "3":
			break
		else:
			print("Opção inválida!")

def criar_turma():
	print("\n=== CRIAR TURMA ===")
	
	# Listar cursos
	print("Cursos disponíveis:")
	try:
		cursor = conn.cursor()
		cursor.execute("SELECT id_curso, nome FROM curso WHERE ativo = 1")
		results = cursor.fetchall()
		for row in results:
			print(f"ID: {row[0]} - {row[1]}")
	except Error as e:
		print(f"Erro: {e}")
	
	# Listar professores
	print("\nProfessores disponíveis:")
	try:
		cursor.execute("SELECT u.id_usuario, u.nome FROM usuario u JOIN professor p ON u.id_usuario = p.id_professor WHERE u.ativo = 1")
		results = cursor.fetchall()
		for row in results:
			print(f"ID: {row[0]} - {row[1]}")
	except Error as e:
		print(f"Erro: {e}")
	
	# Listar disciplinas
	print("\nDisciplinas disponíveis:")
	try:
		cursor.execute("SELECT id_disciplina, nome FROM disciplina WHERE ativo = 1")
		results = cursor.fetchall()
		for row in results:
			print(f"ID: {row[0]} - {row[1]}")
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")
	
	codigo = input("\nCódigo da turma: ")
	periodo = input("Período (ex: 2024.1): ")
	horario = input("Horário: ")
	vagas = int(input("Vagas totais: "))
	id_curso = int(input("ID do curso: "))
	id_professor = int(input("ID do professor: "))
	id_disciplina = int(input("ID da disciplina: "))
	
	query = f"""INSERT INTO turma (codigo_turma, periodo, horario, vagas_totais, id_curso, id_professor, id_disciplina, data_inicio) 
				VALUES ('{codigo}', '{periodo}', '{horario}', {vagas}, {id_curso}, {id_professor}, {id_disciplina}, CURDATE())"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		print("Turma criada com sucesso!")
		cursor.close()
	except Error as e:
		print(f"Erro ao criar turma: {e}")

# Funções do Professor
def professor_turmas(professor):
	print("\n=== MINHAS TURMAS ===")
	query = f"""SELECT t.id_turma, t.codigo_turma, c.nome, t.periodo, t.vagas_ocupadas, t.vagas_totais 
				FROM turma t JOIN curso c ON t.id_curso = c.id_curso 
				WHERE t.id_professor = {professor.id} AND t.ativa = 1"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		for row in results:
			print(f"ID: {row[0]} | Código: {row[1]} | Curso: {row[2]} | Período: {row[3]} | Vagas: {row[4]}/{row[5]}")
		
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")

def cadastrar_avaliacao(professor):
	print("\n=== CADASTRAR AVALIAÇÃO ===")
	
	# Listar turmas do professor
	professor_turmas(professor)
	
	id_turma = int(input("ID da turma: "))
	titulo = input("Título: ")
	descricao = input("Descrição: ")
	tipo = input("Tipo (prova/trabalho/apresentacao/participacao): ")
	data = input("Data (YYYY-MM-DD): ")
	peso = float(input("Peso (ex: 0.3 para 30%): "))
	
	query = f"""INSERT INTO avaliacao (titulo, descricao, tipo, data_avaliacao, peso, id_turma) 
				VALUES ('{titulo}', '{descricao}', '{tipo}', '{data}', {peso:.2f}, {id_turma})"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		print("Avaliação cadastrada com sucesso!")
		cursor.close()
	except Error as e:
		print(f"Erro ao cadastrar avaliação: {e}")

def registrar_notas(professor):
	print("\n=== REGISTRAR NOTAS ===")
	
	# Listar avaliações do professor
	query = f"""SELECT a.id_avaliacao, a.titulo, t.codigo_turma 
				FROM avaliacao a JOIN turma t ON a.id_turma = t.id_turma 
				WHERE t.id_professor = {professor.id}"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		print("Avaliações:")
		for row in results:
			print(f"ID: {row[0]} | {row[1]} - Turma: {row[2]}")
	except Error as e:
		print(f"Erro: {e}")
	
	id_avaliacao = int(input("ID da avaliação: "))
	
	# Listar alunos da turma
	query = f"""SELECT u.id_usuario, u.nome, m.id_matricula 
				FROM usuario u JOIN aluno a ON u.id_usuario = a.id_aluno 
				JOIN matricula m ON a.id_aluno = m.id_aluno 
				JOIN avaliacao av ON m.id_turma = av.id_turma 
				WHERE av.id_avaliacao = {id_avaliacao} AND m.status = 'matriculado'"""
	
	try:
		cursor.execute(query)
		results = cursor.fetchall()
		
		print("\nAlunos para avaliação:")
		for row in results:
			print(f"ID: {row[0]} | Nome: {row[1]}")
			
			nota = float(input(f"Nota para {row[1]}: "))
			
			insert_query = f"""INSERT INTO nota (id_aluno, id_avaliacao, valor_nota) VALUES ({row[0]}, {id_avaliacao}, {nota:.2f}) 
							ON DUPLICATE KEY UPDATE valor_nota = {nota:.2f}"""
			cursor.execute(insert_query)
			conn.commit()
		
		cursor.close()
		print("Notas registradas com sucesso!")
	except Error as e:
		print(f"Erro: {e}")

# Funções do Aluno
def matricular_turma(aluno):
	print("\n=== MATRÍCULA EM TURMA ===")
	
	# Verificar se é reprovado para dar prioridade
	query = f"SELECT COUNT(*) FROM matricula WHERE id_aluno = {aluno.id} AND status = 'reprovado'"
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		eh_reprovado = result[0] > 0
		
		# Listar turmas disponíveis
		print("Turmas disponíveis:")
		query = """SELECT t.id_turma, t.codigo_turma, c.nome, d.nome, u.nome, t.vagas_ocupadas, t.vagas_totais 
				   FROM turma t JOIN curso c ON t.id_curso = c.id_curso 
				   JOIN disciplina d ON t.id_disciplina = d.id_disciplina 
				   JOIN usuario u ON t.id_professor = u.id_usuario 
				   WHERE t.ativa = 1 AND t.vagas_ocupadas < t.vagas_totais"""
		
		cursor.execute(query)
		results = cursor.fetchall()
		
		for row in results:
			print(f"ID: {row[0]} | {row[1]} - {row[2]} ({row[3]}) | Prof: {row[4]} | Vagas: {row[5]}/{row[6]}")
		
		id_turma = int(input("\nID da turma para matrícula: "))
		
		# Tentar matricular
		query = f"""INSERT INTO matricula (id_aluno, id_turma, status, prioridade) 
					VALUES ({aluno.id}, {id_turma}, 'matriculado', '{'reprovado' if eh_reprovado else 'normal'}')"""
		
		try:
			cursor.execute(query)
			conn.commit()
			
			# Atualizar contador de vagas
			query = f"UPDATE turma SET vagas_ocupadas = vagas_ocupadas + 1 WHERE id_turma = {id_turma}"
			cursor.execute(query)
			conn.commit()
			print("Matrícula realizada com sucesso!")
			
		except Error as e:
			error_msg = str(e)
			print(f"Erro na matrícula: {error_msg}")
			
			# Se falhou por vagas, criar solicitação
			if "vagas" in error_msg.lower():
				print("Turma lotada! Criando solicitação de vaga...")
				query = f"""INSERT INTO solicitacao_vagas (id_aluno, id_turma, mensagem) 
							VALUES ({aluno.id}, {id_turma}, 'Solicitação automática: turma lotada')"""
				cursor.execute(query)
				conn.commit()
				print("Solicitação enviada ao professor!")
		
		cursor.close()
		
	except Error as e:
		print(f"Erro: {e}")

def visualizar_notas(aluno):
	print("\n=== MINHAS NOTAS ===")
	
	query = f"""SELECT a.titulo, t.codigo_turma, n.valor_nota, a.data_avaliacao 
				FROM nota n JOIN avaliacao a ON n.id_avaliacao = a.id_avaliacao 
				JOIN turma t ON a.id_turma = t.id_turma 
				WHERE n.id_aluno = {aluno.id}"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		print("Avaliação | Turma | Nota | Data")
		print("--------------------------------")
		for row in results:
			print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
		
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")

# Funções de Relatórios
def relatorio_alunos_por_turma():
	print("\n=== ALUNOS POR TURMA ===")
	
	query = """SELECT c.nome, t.codigo_turma, COUNT(m.id_matricula) as total_alunos 
			   FROM curso c JOIN turma t ON c.id_curso = t.id_curso 
			   JOIN matricula m ON t.id_turma = m.id_turma 
			   WHERE m.status = 'matriculado' 
			   GROUP BY c.nome, t.codigo_turma"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		for row in results:
			print(f"Curso: {row[0]} | Turma: {row[1]} | Alunos: {row[2]}")
		
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")

def relatorio_medias_turmas():
	print("\n=== MÉDIAS POR TURMA ===")
	
	query = """SELECT t.codigo_turma, c.nome, AVG(n.valor_nota) as media 
			   FROM turma t JOIN curso c ON t.id_curso = c.id_curso 
			   JOIN avaliacao a ON t.id_turma = a.id_turma 
			   JOIN nota n ON a.id_avaliacao = n.id_avaliacao 
			   GROUP BY t.codigo_turma, c.nome"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		for row in results:
			print(f"Turma: {row[0]} | Curso: {row[1]} | Média: {row[2]}")
		
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")

def relatorio_alunos_abaixo_media():
	print("\n=== ALUNOS ABAIXO DA MÉDIA (<5) ===")
	
	query = """SELECT u.nome, t.codigo_turma, AVG(n.valor_nota) as media 
			   FROM usuario u JOIN nota n ON u.id_usuario = n.id_aluno 
			   JOIN avaliacao a ON n.id_avaliacao = a.id_avaliacao 
			   JOIN turma t ON a.id_turma = t.id_turma 
			   GROUP BY u.nome, t.codigo_turma 
			   HAVING media < 5.0"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		for row in results:
			print(f"Aluno: {row[0]} | Turma: {row[1]} | Média: {row[2]}")
		
		cursor.close()
	except Error as e:
		print(f"Erro: {e}")

# Menu principal por tipo de usuário
def menu_administrador(admin):
	while True:
		print("\n=== SISTEMA DE GESTÃO ACADÊMICA - ADMINISTRADOR ===")
		print("1. Cadastrar usuário")
		print("2. Gerenciar cursos")
		print("3. Criar turma")
		print("4. Relatório: Alunos por turma")
		print("5. Relatório: Médias por turma")
		print("6. Relatório: Alunos abaixo da média")
		print("7. Sair")
		opcao = input("Escolha: ")

		if opcao == "1":
			cadastrar_usuario()
		elif opcao == "2":
			gerenciar_cursos()
		elif opcao == "3":
			criar_turma()
		elif opcao == "4":
			relatorio_alunos_por_turma()
		elif opcao == "5":
			relatorio_medias_turmas()
		elif opcao == "6":
			relatorio_alunos_abaixo_media()
		elif opcao == "7":
			print("Saindo...")
			break
		else:
			print("Opção inválida!")
		
		if opcao != "7":
			pressione_para_continuar()

def menu_professor(professor):
	while True:
		print("\n=== SISTEMA DE GESTÃO ACADÊMICA - PROFESSOR ===")
		print("1. Minhas turmas")
		print("2. Cadastrar avaliação")
		print("3. Registrar notas")
		print("4. Cadastrar material de aula")
		print("5. Sair")
		opcao = input("Escolha: ")

		if opcao == "1":
			professor_turmas(professor)
		elif opcao == "2":
			cadastrar_avaliacao(professor)
		elif opcao == "3":
			registrar_notas(professor)
		elif opcao == "4":
			print("Funcionalidade em desenvolvimento...")
		elif opcao == "5":
			print("Saindo...")
			break
		else:
			print("Opção inválida!")
		
		if opcao != "5":
			pressione_para_continuar()

def menu_aluno(aluno):
	while True:
		print("\n=== SISTEMA DE GESTÃO ACADÊMICA - ALUNO ===")
		print("1. Matricular em turma")
		print("2. Visualizar minhas notas")
		print("3. Ver turmas matriculadas")
		print("4. Sair")
		opcao = input("Escolha: ")

		if opcao == "1":
			matricular_turma(aluno)
		elif opcao == "2":
			visualizar_notas(aluno)
		elif opcao == "3":
			print("Funcionalidade em desenvolvimento...")
		elif opcao == "4":
			print("Saindo...")
			break
		else:
			print("Opção inválida!")
		
		if opcao != "4":
			pressione_para_continuar()

def main():
	print("=== SISTEMA DE GESTÃO ACADÊMICA ===")
	
	if not conectar_banco():
		print("Erro ao conectar com o banco de dados!")
		return
	
	usuario = fazer_login()
	if usuario is None:
		if conn:
			conn.close()
		return
	
	print(f"\nBem-vindo, {usuario.nome}! ({usuario.tipo})")
	
	# Direcionar para o menu apropriado
	if usuario.tipo == "admin":
		menu_administrador(usuario)
	elif usuario.tipo == "professor":
		menu_professor(usuario)
	elif usuario.tipo == "aluno":
		menu_aluno(usuario)
	
	if conn:
		conn.close()


main()