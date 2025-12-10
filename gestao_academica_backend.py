import mysql.connector
from mysql.connector import Error
import sys

# Classes para as estruturas
class Usuario:
	def __init__(self):
		self.id = 0
		self.nome = ""
		self.email = ""
		self.tipo = ""
		self.ativo = 0

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

# Funções para autenticação
def fazer_login():
	print("----- LOGIN -----")
	email = input("Email: ")
	senha = input("Senha: ")

	query = f"""SELECT id_usuario, nome, email, is_admin, is_professor, is_aluno 
				FROM usuario WHERE email = '{email}' AND senha = '{senha}'"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		
		if result:
			usuario = Usuario()
			usuario.id = result[0]
			usuario.nome = result[1]
			usuario.email = result[2]
			
			is_admin = bool(result[3])
			is_prof = bool(result[4])
			is_aluno = bool(result[5])
			
			if is_admin and is_prof:
				usuario.tipo = "admin_professor"
			elif is_admin:
				usuario.tipo = "admin"
			elif is_prof and is_aluno:
				usuario.tipo = "professor_aluno"
			elif is_prof:
				usuario.tipo = "professor"
			elif is_aluno:
				usuario.tipo = "aluno"
			else:
				usuario.tipo = "desconhecido"
			
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
	print("----- CADASTRAR USUÁRIO -----")
	nome = input("Nome: ")
	email = input("Email: ")
	senha = input("Senha: ")
	tipo = input("Tipo (admin/professor/aluno): ")
	
	tipos = {
	"admin": "FALSE, TRUE, FALSE",
	"professor": "TRUE, FALSE, FALSE",
	"aluno": "FALSE, FALSE, TRUE"
	}
	
	query = f"INSERT INTO usuario (nome, email, senha, is_professor, is_admin, is_aluno) VALUES ('{nome}', '{email}', '{senha}', {tipos[tipo]})"
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		
		print("Usuário cadastrado com sucesso!")
		
		# Se for aluno, cadastrar na tabela aluno
		if tipo == "aluno":
			id_usuario = cursor.lastrowid
			ra = f"2024{id_usuario:05d}"
			
			query = f"INSERT INTO aluno (id_aluno, data_ingresso, status, registro) VALUES ({id_usuario}, CURDATE(), 'ativo', '{ra}')"
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

def editar_usuario_admin(admin, email_usuario):
	"""Edita usuário (apenas para administradores)"""
	print(f"\n--- EDITAR USUÁRIO - Administrador ---")
	
	# Buscar informações do usuário a ser editado
	query = f"""SELECT id_usuario, nome, email, is_admin, is_professor, is_aluno FROM usuario WHERE email = '{email_usuario}'"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		
		if not result:
			print(f"Usuário com email '{email_usuario}' não encontrado!")
			cursor.close()
			return
		
		id_usuario = result[0]
		nome_atual = result[1]
		email_atual = result[2]
		eh_admin = bool(result[3])
		eh_prof = bool(result[4])
		is_aluno = bool(result[5])
		
		print(f"\nEditando usuário: {nome_atual} ({email_atual})")
		print(f"Perfis atuais: ", end="")
		perfis = []
		if eh_admin:
			perfis.append("Administrador")
		if eh_prof:
			perfis.append("Professor")
		if is_aluno:
			perfis.append("Aluno")
		print(", ".join(perfis) if perfis else "Nenhum perfil definido")
		
		while True:
			print("\n--- Opções de Edição (Admin) ---")
			print("1. Alterar nome")
			print("2. Alterar email")
			print("3. Alterar senha")
			print("4. Adicionar/Remover perfil de Administrador")
			print("5. Adicionar/Remover perfil de Professor")
			print("6. Adicionar/Remover perfil de Aluno")
			print("7. Finalizar edição")
			opcao = input("Escolha: ")
			
			if opcao == "1":
				novo_nome = input(f"Novo nome (atual: {nome_atual}): ").strip()
				if novo_nome:
					update_query = f"UPDATE usuario SET nome = '{novo_nome}' WHERE id_usuario = {id_usuario}"
					cursor.execute(update_query)
					conn.commit()
					nome_atual = novo_nome
					print("Nome alterado com sucesso!")
			
			elif opcao == "2":
				novo_email = input(f"Novo email (atual: {email_atual}): ").strip()
				if novo_email:
					# Verificar se email já existe
					check_query = f"SELECT COUNT(*) FROM usuario WHERE email = '{novo_email}' AND id_usuario != {id_usuario}"
					cursor.execute(check_query)
					count_result = cursor.fetchone()
					
					if count_result and count_result[0] > 0:
						print("Erro: Este email já está em uso por outro usuário!")
					else:
						update_query = f"UPDATE usuario SET email = '{novo_email}' WHERE id_usuario = {id_usuario}"
						cursor.execute(update_query)
						conn.commit()
						email_atual = novo_email
						print("Email alterado com sucesso!")
			
			elif opcao == "3":
				nova_senha = getpass.getpass("Nova senha: ")
				confirmar_senha = getpass.getpass("Confirmar senha: ")
				
				if nova_senha and nova_senha == confirmar_senha:
					update_query = f"UPDATE usuario SET senha = '{nova_senha}' WHERE id_usuario = {id_usuario}"
					cursor.execute(update_query)
					conn.commit()
					print("Senha alterada com sucesso!")
				else:
					print("Erro: As senhas não coincidem ou estão vazias!")
			
			elif opcao == "4":
				novo_status = not eh_admin
				update_query = f"UPDATE usuario SET is_admin = {int(novo_status)} WHERE id_usuario = {id_usuario}"
				cursor.execute(update_query)
				conn.commit()
				eh_admin = novo_status
				print(f"Perfil de Administrador {'adicionado' if novo_status else 'removido'}!")
				
				# Se está removendo admin e é o próprio usuário logado, verificar
				if id_usuario == admin.id and not novo_status:
					print("AVISO: Você removeu seu próprio perfil de administrador!")
			
			elif opcao == "5":
				novo_status = not eh_prof
				update_query = f"UPDATE usuario SET is_professor = {int(novo_status)} WHERE id_usuario = {id_usuario}"
				cursor.execute(update_query)
				conn.commit()
				eh_prof = novo_status
				print(f"Perfil de Professor {'adicionado' if novo_status else 'removido'}!")
				
				# Se adicionando perfil de professor, criar registro na tabela professor
				if novo_status:
					check_prof_query = f"SELECT COUNT(*) FROM professor WHERE id_professor = {id_usuario}"
					cursor.execute(check_prof_query)
					prof_exists = cursor.fetchone()[0] > 0
					
					if not prof_exists:
						insert_prof_query = f"INSERT INTO professor (id_professor, data_contratacao) VALUES ({id_usuario}, CURDATE())"
						cursor.execute(insert_prof_query)
						conn.commit()
						print("Registro de professor criado com data de contratação atual.")
				# Se removendo perfil de professor, verificar se pode remover da tabela professor
				else:
					# Verificar se o professor está ministrando alguma turma ativa
					check_turmas_query = f"SELECT COUNT(*) FROM turma WHERE id_professor = {id_usuario} AND ativa = 1"
					cursor.execute(check_turmas_query)
					tem_turmas_ativas = cursor.fetchone()[0] > 0
					
					if tem_turmas_ativas:
						print("AVISO: Não é possível remover o perfil de professor enquanto ele ministra turmas ativas!")
						# Reverter a mudança
						update_query = f"UPDATE usuario SET is_professor = 1 WHERE id_usuario = {id_usuario}"
						cursor.execute(update_query)
						conn.commit()
						eh_prof = True
					else:
						print("Perfil de professor removido.")
			
			elif opcao == "6":
				novo_status = not is_aluno
				update_query = f"UPDATE usuario SET is_aluno = {int(novo_status)} WHERE id_usuario = {id_usuario}"
				cursor.execute(update_query)
				conn.commit()
				is_aluno = novo_status
				print(f"Perfil de Aluno {'adicionado' if novo_status else 'removido'}!")
				
				# Se adicionando perfil de aluno, criar registro na tabela aluno
				if novo_status:
					check_aluno_query = f"SELECT COUNT(*) FROM aluno WHERE id_aluno = {id_usuario}"
					cursor.execute(check_aluno_query)
					aluno_exists = cursor.fetchone()[0] > 0
					
					if not aluno_exists:
						ra = f"2024{id_usuario:05d}"
						insert_aluno_query = f"INSERT INTO aluno (id_aluno, data_ingresso, status, registro) VALUES ({id_usuario}, CURDATE(), 'ativo', '{ra}')"
						cursor.execute(insert_aluno_query)
						conn.commit()
						print(f"Registro de aluno criado com RA: {ra}")
				# Se removendo perfil de aluno, verificar se pode remover da tabela aluno
				else:
					# Verificar se o aluno está matriculado em alguma turma
					check_matriculas_query = f"SELECT COUNT(*) FROM matricula WHERE id_aluno = {id_usuario} AND status = 'matriculado'"
					cursor.execute(check_matriculas_query)
					tem_matriculas_ativas = cursor.fetchone()[0] > 0
					
					if tem_matriculas_ativas:
						print("AVISO: Não é possível remover o perfil de aluno enquanto ele tem matrículas ativas!")
						# Reverter a mudança
						update_query = f"UPDATE usuario SET is_aluno = 1 WHERE id_usuario = {id_usuario}"
						cursor.execute(update_query)
						conn.commit()
						is_aluno = True
					else:
						print("Perfil de aluno removido.")
			
			elif opcao == "7":
				break
			
			else:
				print("Opção inválida!")
		
		cursor.close()
		print(f"\nEdição do usuário {nome_atual} finalizada!")
		
	except Error as e:
		print(f"Erro ao editar usuário: {e}")

def editar_usuario_professor(professor):
	"""Edita informações do próprio professor"""
	print(f"\n--- EDITAR MEUS DADOS - Professor ---")
	
	try:
		cursor = conn.cursor()
		
		while True:
			print("\n--- Opções de Edição (Professor) ---")
			print("1. Alterar nome")
			print("2. Alterar email")
			print("3. Alterar senha")
			print("4. Visualizar meus dados")
			print("5. Finalizar edição")
			opcao = input("Escolha: ")
			
			if opcao == "1":
				# Obter nome atual
				query = f"SELECT nome FROM usuario WHERE id_usuario = {professor.id}"
				cursor.execute(query)
				nome_atual = cursor.fetchone()[0]
				
				novo_nome = input(f"Novo nome (atual: {nome_atual}): ").strip()
				if novo_nome:
					update_query = f"UPDATE usuario SET nome = '{novo_nome}' WHERE id_usuario = {professor.id}"
					cursor.execute(update_query)
					conn.commit()
					professor.nome = novo_nome
					print("Nome alterado com sucesso!")
			
			elif opcao == "2":
				# Obter email atual
				query = f"SELECT email FROM usuario WHERE id_usuario = {professor.id}"
				cursor.execute(query)
				email_atual = cursor.fetchone()[0]
				
				novo_email = input(f"Novo email (atual: {email_atual}): ").strip()
				if novo_email:
					# Verificar se email já existe
					check_query = f"SELECT COUNT(*) FROM usuario WHERE email = '{novo_email}' AND id_usuario != {professor.id}"
					cursor.execute(check_query)
					count_result = cursor.fetchone()
					
					if count_result and count_result[0] > 0:
						print("Erro: Este email já está em uso por outro usuário!")
					else:
						update_query = f"UPDATE usuario SET email = '{novo_email}' WHERE id_usuario = {professor.id}"
						cursor.execute(update_query)
						conn.commit()
						professor.email = novo_email
						print("Email alterado com sucesso!")
			
			elif opcao == "3":
				nova_senha = getpass.getpass("Nova senha: ")
				confirmar_senha = getpass.getpass("Confirmar senha: ")
				
				if nova_senha and nova_senha == confirmar_senha:
					update_query = f"UPDATE usuario SET senha = '{nova_senha}' WHERE id_usuario = {professor.id}"
					cursor.execute(update_query)
					conn.commit()
					print("Senha alterada com sucesso!")
				else:
					print("Erro: As senhas não coincidem ou estão vazias!")
			
			elif opcao == "4":
				# Visualizar dados do professor
				query = f"""SELECT u.nome, u.email, p.data_contratacao, COUNT(DISTINCT t.id_turma) as turmas_ministradas FROM usuario u LEFT JOIN professor p ON u.id_usuario = p.id_professor LEFT JOIN turma t ON u.id_usuario = t.id_professor AND t.ativa = 1 WHERE u.id_usuario = {professor.id} GROUP BY u.id_usuario"""
				
				cursor.execute(query)
				result = cursor.fetchone()
				
				if result:
					print(f"\n--- MEUS DADOS ---")
					print(f"Nome: {result[0]}")
					print(f"Email: {result[1]}")
					print(f"Data de contratação: {result[2] if result[2] else 'N/A'}")
					print(f"Turmas ativas ministrando: {result[3]}")
			
			elif opcao == "5":
				break
			
			else:
				print("Opção inválida!")
		
		cursor.close()
		
	except Error as e:
		print(f"Erro ao editar dados: {e}")

def editar_usuario_aluno(aluno):
	"""Edita informações do próprio aluno"""
	print(f"\n--- EDITAR MEUS DADOS - Aluno ---")
	
	try:
		cursor = conn.cursor()
		
		while True:
			print("\n--- Opções de Edição (Aluno) ---")
			print("1. Alterar nome")
			print("2. Alterar email")
			print("3. Alterar senha")
			print("4. Visualizar meus dados")
			print("5. Finalizar edição")
			opcao = input("Escolha: ")
			
			if opcao == "1":
				# Obter nome atual
				query = f"SELECT nome FROM usuario WHERE id_usuario = {aluno.id}"
				cursor.execute(query)
				nome_atual = cursor.fetchone()[0]
				
				novo_nome = input(f"Novo nome (atual: {nome_atual}): ").strip()
				if novo_nome:
					update_query = f"UPDATE usuario SET nome = '{novo_nome}' WHERE id_usuario = {aluno.id}"
					cursor.execute(update_query)
					conn.commit()
					aluno.nome = novo_nome
					print("Nome alterado com sucesso!")
			
			elif opcao == "2":
				# Obter email atual
				query = f"SELECT email FROM usuario WHERE id_usuario = {aluno.id}"
				cursor.execute(query)
				email_atual = cursor.fetchone()[0]
				
				novo_email = input(f"Novo email (atual: {email_atual}): ").strip()
				if novo_email:
					# Verificar se email já existe
					check_query = f"SELECT COUNT(*) FROM usuario WHERE email = '{novo_email}' AND id_usuario != {aluno.id}"
					cursor.execute(check_query)
					count_result = cursor.fetchone()
					
					if count_result and count_result[0] > 0:
						print("Erro: Este email já está em uso por outro usuário!")
					else:
						update_query = f"UPDATE usuario SET email = '{novo_email}' WHERE id_usuario = {aluno.id}"
						cursor.execute(update_query)
						conn.commit()
						aluno.email = novo_email
						print("Email alterado com sucesso!")
			
			elif opcao == "3":
				nova_senha = getpass.getpass("Nova senha: ")
				confirmar_senha = getpass.getpass("Confirmar senha: ")
				
				if nova_senha and nova_senha == confirmar_senha:
					update_query = f"UPDATE usuario SET senha = '{nova_senha}' WHERE id_usuario = {aluno.id}"
					cursor.execute(update_query)
					conn.commit()
					print("Senha alterada com sucesso!")
				else:
					print("Erro: As senhas não coincidem ou estão vazias!")
			
			elif opcao == "4":
				# Visualizar dados do aluno
				query = f"""SELECT u.nome, u.email, a.ra, a.data_ingresso, a.status,COUNT(DISTINCT m.id_turma) as turmas_matriculadas, AVG(n.valor_nota) as media_geral FROM usuario u LEFT JOIN aluno a ON u.id_usuario = a.id_aluno LEFT JOIN matricula m ON u.id_usuario = m.id_aluno AND m.status = 'matriculado' LEFT JOIN nota n ON u.id_usuario = n.id_aluno WHERE u.id_usuario = {aluno.id} GROUP BY u.id_usuario"""
				
				cursor.execute(query)
				result = cursor.fetchone()
				
				if result:
					print(f"\n--- MEUS DADOS ---")
					print(f"Nome: {result[0]}")
					print(f"Email: {result[1]}")
					print(f"Registro: {result[2] if result[2] else 'N/A'}")
					print(f"Data de ingresso: {result[3] if result[3] else 'N/A'}")
					print(f"Status: {result[4] if result[4] else 'N/A'}")
					print(f"Turmas matriculadas: {result[5]}")
					print(f"Média geral: {result[6]:.2f if result[6] else 'N/A'}")
			
			elif opcao == "5":
				break
			
			else:
				print("Opção inválida!")
		
		cursor.close()
		
	except Error as e:
		print(f"Erro ao editar dados: {e}")

def menu_editar_usuario(usuario_logado):
	"""Menu principal para edição de usuário"""
	if usuario_logado.tipo == "admin":
		# Administrador pode editar qualquer usuário
		email_usuario = input("\nDigite o email do usuário que deseja editar: ").strip()
		if email_usuario:
			editar_usuario_admin(usuario_logado, email_usuario)
		else:
			print("Email inválido!")
	
	elif usuario_logado.tipo == "professor":
		# Professor só pode editar seus próprios dados
		editar_usuario_professor(usuario_logado)
	
	elif usuario_logado.tipo == "aluno":
		# Aluno só pode editar seus próprios dados
		editar_usuario_aluno(usuario_logado)
	
	elif usuario_logado.tipo == "professor_aluno":
		# Usuário com ambos os perfis escolhe qual perfil usar para edição
		print("\nVocê possui perfis de Professor e Aluno.")
		print("1. Editar como Professor")
		print("2. Editar como Aluno")
		escolha = input("Escolha: ")
		
		if escolha == "1":
			editar_usuario_professor(usuario_logado)
		elif escolha == "2":
			editar_usuario_aluno(usuario_logado)
		else:
			print("Opção inválida!")
	
	elif usuario_logado.tipo == "admin_professor":
		# Administrador/Professor pode escolher modo
		print("\nVocê possui perfis de Administrador e Professor.")
		print("1. Editar outro usuário (modo Administrador)")
		print("2. Editar meus dados (modo Professor)")
		escolha = input("Escolha: ")
		
		if escolha == "1":
			email_usuario = input("Digite o email do usuário que deseja editar: ").strip()
			if email_usuario:
				editar_usuario_admin(usuario_logado, email_usuario)
			else:
				print("Email inválido!")
		elif escolha == "2":
			editar_usuario_professor(usuario_logado)
		else:
			print("Opção inválida!")

def gerenciar_cursos():
	while True:
		print("\n----- GERENCIAR CURSOS -----")
		print("1. Listar cursos")
		print("2. Cadastrar curso")
		print("3. Voltar")
		opcao = input("Escolha: ")
		
		if opcao == "1":
			# Listar cursos
			query = "SELECT c.id_curso, c.nome, c.carga_horaria_total, c.coordenador_id FROM curso"
			
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
	print("\n----- CRIAR TURMA -----")
	
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
	print("\n----- MINHAS TURMAS -----")
	query = f"""SELECT t.id_turma, t.codigo_turma, c.nome, t.periodo, t.vagas_ocupadas, t.vagas_totais FROM turma t JOIN curso c ON t.id_curso = c.id_curso WHERE t.id_professor = {professor.id} AND t.ativa = 1"""
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
	print("\n----- CADASTRAR AVALIAÇÃO -----")
	
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
	print("\n----- REGISTRAR NOTAS -----")
	
	# Listar avaliações do professor
	query = f"""SELECT a.id_avaliacao, a.titulo, t.codigo_turma FROM avaliacao a JOIN turma t ON a.id_turma = t.id_turma WHERE t.id_professor = {professor.id}"""
	
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
	query = f"""SELECT u.id_usuario, u.nome, m.id_matricula FROM usuario u JOIN aluno a ON u.id_usuario = a.id_aluno JOIN matricula m ON a.id_aluno = m.id_aluno JOIN avaliacao av ON m.id_turma = av.id_turma WHERE av.id_avaliacao = {id_avaliacao} AND m.status = 'matriculado'"""
	
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
	print("\n----- MATRÍCULA EM TURMA -----")
	
	query = f"SELECT COUNT(*) FROM matricula WHERE id_aluno = {aluno.id} AND status = 'reprovado'"
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		result = cursor.fetchone()
		is_reprovado = result[0] > 0
		
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
		query = f"""INSERT INTO matricula (id_aluno, id_turma, status) 
					VALUES ({aluno.id}, {id_turma}, 'matriculado')"""
		
		try:
			cursor.execute(query)
			conn.commit()
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
	print("\n----- MINHAS NOTAS -----")
	
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

def ver_turmas_matriculadas(aluno):
    """Mostra as turmas que o aluno está matriculado"""
    print("\n=== MINHAS TURMAS MATRICULADAS ===")
    
    query = f"""SELECT t.id_turma, t.codigo_turma, c.nome as curso_nome, 
               d.nome as disciplina_nome, u.nome as professor_nome,
               t.periodo, t.horario, m.status as status_matricula,
               m.data_matricula, m.prioridade,
               t.vagas_ocupadas, t.vagas_totais,
               COUNT(DISTINCT a.id_avaliacao) as total_avaliacoes,
               COUNT(DISTINCT mat.id_material) as total_materiais
               FROM matricula m 
               JOIN turma t ON m.id_turma = t.id_turma
               JOIN curso c ON t.id_curso = c.id_curso
               JOIN disciplina d ON t.id_disciplina = d.id_disciplina
               JOIN usuario u ON t.id_professor = u.id_usuario
               LEFT JOIN avaliacao a ON t.id_turma = a.id_turma
               LEFT JOIN material_aula mat ON t.id_turma = mat.id_turma
               WHERE m.id_aluno = {aluno.id} AND m.status = 'matriculado'
               GROUP BY t.id_turma, t.codigo_turma, c.nome, d.nome, u.nome,
                        t.periodo, t.horario, m.status, m.data_matricula, 
                        m.prioridade, t.vagas_ocupadas, t.vagas_totais
               ORDER BY t.periodo, c.nome"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        turmas = cursor.fetchall()
        
        if turmas:
            print(f"\n📚 Você está matriculado em {len(turmas)} turma(s):")
            
            for i, turma in enumerate(turmas, 1):
                ocupacao = (turma[10] / turma[11] * 100) if turma[11] > 0 else 0
                print(f"\n{i}. {turma[1]} - {turma[2]}")
                print(f"   Disciplina: {turma[3]}")
                print(f"   Professor: {turma[4]}")
                print(f"   Período: {turma[5]} | Horário: {turma[6]}")
                print(f"   Matriculado desde: {turma[8]}")
                print(f"   Status: {turma[7]} | Prioridade: {turma[9]}")
                print(f"   Vagas: {turma[10]}/{turma[11]} ({ocupacao:.1f}% ocupada)")
                print(f"   Recursos: {turma[12]} avaliações | {turma[13]} materiais")
        else:
            print("Você não está matriculado em nenhuma turma no momento.")
            print("Use a opção 'Matricular em turma' para se matricular.")
        
        cursor.close()
        
        # Opção para ver detalhes de uma turma específica
        if turmas:
            opcao = input("\nDigite o número da turma para ver detalhes (ou 0 para voltar): ")
            if opcao.isdigit():
                idx = int(opcao) - 1
                if 0 <= idx < len(turmas):
                    ver_detalhes_turma(aluno, turmas[idx][0])  # id_turma
                elif idx != -1:
                    print("Número inválido!")
        
    except Error as e:
        print(f"Erro ao buscar turmas: {e}")

def ver_detalhes_turma(aluno, id_turma):
    """Mostra detalhes específicos de uma turma"""
    query = f"""SELECT t.codigo_turma, c.nome as curso_nome, 
               d.nome as disciplina_nome, u.nome as professor_nome,
               t.periodo, t.horario, t.local,
               d.carga_horaria, d.ementa,
               m.status as status_matricula, m.data_matricula,
               AVG(n.valor_nota) as minha_media
               FROM turma t 
               JOIN curso c ON t.id_curso = c.id_curso
               JOIN disciplina d ON t.id_disciplina = d.id_disciplina
               JOIN usuario u ON t.id_professor = u.id_usuario
               JOIN matricula m ON t.id_turma = m.id_turma AND m.id_aluno = {aluno.id}
               LEFT JOIN avaliacao av ON t.id_turma = av.id_turma
               LEFT JOIN nota n ON av.id_avaliacao = n.id_avaliacao AND n.id_aluno = {aluno.id}
               WHERE t.id_turma = {id_turma}
               GROUP BY t.id_turma, t.codigo_turma, c.nome, d.nome, u.nome,
                        t.periodo, t.horario, t.local, d.carga_horaria, d.ementa,
                        m.status, m.data_matricula"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        turma = cursor.fetchone()
        
        if turma:
            print(f"\n📖 DETALHES DA TURMA {turma[0]}")
            print(f"Curso: {turma[1]}")
            print(f"Disciplina: {turma[2]}")
            print(f"Professor: {turma[3]}")
            print(f"Período: {turma[4]} | Horário: {turma[5]}")
            print(f"Local: {turma[6] if turma[6] else 'Não informado'}")
            print(f"Carga horária: {turma[7]} horas")
            print(f"Ementa: {turma[8] if turma[8] else 'Não disponível'}")
            print(f"Sua matrícula: {turma[9]} desde {turma[10]}")
            print(f"Sua média atual: {turma[11]:.2f if turma[11] else 'N/A'}")
            
            # Menu de opções para esta turma
            while True:
                print("\n--- OPÇÕES PARA ESTA TURMA ---")
                print("1. Ver materiais de aula")
                print("2. Ver avaliações")
                print("3. Voltar")
                escolha = input("Escolha: ")
                
                if escolha == "1":
                    acessar_materiais_turma(aluno, id_turma)
                elif escolha == "2":
                    acessar_avaliacoes_turma(aluno, id_turma)
                elif escolha == "3":
                    break
                else:
                    print("Opção inválida!")
        
        cursor.close()
    except Error as e:
        print(f"Erro ao buscar detalhes: {e}")

def acessar_materiais_turma(aluno, id_turma):
    """Acessa os materiais de aula da turma"""
    print("\n=== MATERIAIS DE AULA ===")
    
    query = f"""SELECT m.id_material, m.titulo, m.tipo, m.descricao, 
               m.arquivo_url, m.data_publicacao,
               u.nome as professor_nome, COUNT(DISTINCT ac.id_aluno) as acessos
               FROM material_aula m 
               JOIN usuario u ON m.id_professor = u.id_usuario
               LEFT JOIN acesso_material ac ON m.id_material = ac.id_material AND ac.id_aluno = {aluno.id}
               WHERE m.id_turma = {id_turma} AND m.visivel = 1
               GROUP BY m.id_material, m.titulo, m.tipo, m.descricao, 
                        m.arquivo_url, m.data_publicacao, u.nome
               ORDER BY m.data_publicacao DESC"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        materiais = cursor.fetchall()
        
        if materiais:
            print(f"\n📚 {len(materiais)} material(is) disponível(is):")
            
            for i, material in enumerate(materiais, 1):
                print(f"\n{i}. {material[1]} ({material[2]})")
                print(f"   Por: {material[6]} em {material[5]}")
                print(f"   Descrição: {material[3] if material[3] else 'Sem descrição'}")
                print(f"   Arquivo: {material[4] if material[4] else 'Nenhum arquivo'}")
                print(f"   Você acessou: {'Sim' if material[7] > 0 else 'Não'}")
            
            # Opção para acessar um material específico
            opcao = input("\nDigite o número do material para acessar (ou 0 para voltar): ")
            if opcao.isdigit():
                idx = int(opcao) - 1
                if 0 <= idx < len(materiais):
                    acessar_material_detalhe(aluno, materiais[idx][0])
                elif idx != -1:
                    print("Número inválido!")
        else:
            print("Nenhum material disponível para esta turma.")
        
        cursor.close()
    except Error as e:
        print(f"Erro ao buscar materiais: {e}")

def acessar_material_detalhe(aluno, id_material):
    """Acessa um material específico e registra o acesso"""
    query = f"""SELECT m.titulo, m.tipo, m.descricao, m.conteudo, 
               m.arquivo_url, m.data_publicacao, u.nome as professor_nome
               FROM material_aula m 
               JOIN usuario u ON m.id_professor = u.id_usuario
               WHERE m.id_material = {id_material}"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        material = cursor.fetchone()
        
        if material:
            print(f"\n📄 {material[0]} ({material[1]})")
            print(f"Publicado por: {material[6]} em {material[5]}")
            print(f"Arquivo: {material[4] if material[4] else 'Nenhum arquivo'}")
            
            if material[2]:
                print(f"\nDescrição: {material[2]}")
            
            if material[3]:
                print(f"\nConteúdo:\n{material[3]}")
            
            # Registrar acesso ao material
            registrar_acesso_query = f"""INSERT INTO acesso_material (id_aluno, id_material, data_acesso) 
                                       VALUES ({aluno.id}, {id_material}, NOW()) 
                                       ON DUPLICATE KEY UPDATE data_acesso = NOW()"""
            cursor.execute(registrar_acesso_query)
            conn.commit()
            
            # Mostrar opções
            if material[4]:  # Se tem arquivo
                print("\n1. Baixar arquivo")
                print("2. Voltar")
                escolha = input("Escolha: ")
                if escolha == "1":
                    print(f"Simulando download do arquivo: {material[4]}")
                    print("Download iniciado... (simulação)")
            
        cursor.close()
    except Error as e:
        print(f"Erro ao acessar material: {e}")

def acessar_avaliacoes_turma(aluno, id_turma):
    """Acessa as avaliações da turma"""
    print("\n=== AVALIAÇÕES ===")
    
    query = f"""SELECT a.id_avaliacao, a.titulo, a.tipo, a.descricao, 
               a.data_avaliacao, a.peso, a.data_limite,
               n.valor_nota as minha_nota, r.id_resposta,
               COUNT(DISTINCT p.id_pergunta) as total_perguntas,
               a.liberada, a.permite_resposta_tardia
               FROM avaliacao a 
               LEFT JOIN nota n ON a.id_avaliacao = n.id_avaliacao AND n.id_aluno = {aluno.id}
               LEFT JOIN resposta_atividade r ON a.id_avaliacao = r.id_avaliacao AND r.id_aluno = {aluno.id}
               LEFT JOIN pergunta p ON a.id_avaliacao = p.id_avaliacao
               WHERE a.id_turma = {id_turma}
               GROUP BY a.id_avaliacao, a.titulo, a.tipo, a.descricao, 
                        a.data_avaliacao, a.peso, a.data_limite, n.valor_nota,
                        r.id_resposta, a.liberada, a.permite_resposta_tardia
               ORDER BY a.data_avaliacao"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        avaliacoes = cursor.fetchall()
        
        if avaliacoes:
            print(f"\n📝 {len(avaliacoes)} avaliação(ões):")
            
            hoje = datetime.now().date()
            
            for i, avaliacao in enumerate(avaliacoes, 1):
                status = ""
                data_limite = avaliacao[6]
                
                if avaliacao[10] == 0:  # Não liberada
                    status = "🔒 Não liberada"
                elif data_limite and hoje > data_limite:
                    if avaliacao[7] is not None:
                        status = f"📊 Nota: {avaliacao[7]:.1f}"
                    else:
                        status = "⏰ Prazo expirado"
                elif avaliacao[8] is not None:  # Já respondeu
                    status = f"✅ Respondida | Nota: {avaliacao[7]:.1f if avaliacao[7] else 'N/A'}"
                else:
                    status = "📝 Disponível para resposta"
                
                print(f"\n{i}. {avaliacao[1]} ({avaliacao[2]}) - Peso: {avaliacao[5]:.2f}")
                print(f"   Data: {avaliacao[4]} | Limite: {data_limite if data_limite else 'Sem limite'}")
                print(f"   Status: {status}")
                if avaliacao[3]:
                    print(f"   Descrição: {avaliacao[3][:100]}...")
            
            # Opção para acessar uma avaliação específica
            opcao = input("\nDigite o número da avaliação para acessar (ou 0 para voltar): ")
            if opcao.isdigit():
                idx = int(opcao) - 1
                if 0 <= idx < len(avaliacoes):
                    gerenciar_resposta_avaliacao(aluno, avaliacoes[idx][0], avaliacoes[idx])
                elif idx != -1:
                    print("Número inválido!")
        else:
            print("Nenhuma avaliação disponível para esta turma.")
        
        cursor.close()
    except Error as e:
        print(f"Erro ao buscar avaliações: {e}")

def gerenciar_resposta_avaliacao(aluno, id_avaliacao, info_avaliacao):
    """Gerencia as respostas do aluno para uma avaliação"""
    # Primeiro verificar se a avaliação está liberada
    if info_avaliacao[10] == 0:  # Não liberada
        print("Esta avaliação ainda não foi liberada pelo professor.")
        return
    
    # Verificar se ainda está no prazo
    hoje = datetime.now().date()
    data_limite = info_avaliacao[6]
    
    if data_limite and hoje > data_limite and not info_avaliacao[11]:  # Prazo expirado e não permite resposta tardia
        print("O prazo para responder esta avaliação expirou.")
        if info_avaliacao[7] is not None:
            print(f"Sua nota: {info_avaliacao[7]:.1f}")
        return
    
    # Verificar se já respondeu
    if info_avaliacao[8] is not None:  # Já tem resposta
        print(f"\n📄 AVALIAÇÃO: {info_avaliacao[1]}")
        print(f"Você já respondeu esta avaliação.")
        if info_avaliacao[7] is not None:
            print(f"Sua nota: {info_avaliacao[7]:.1f}")
        
        opcao = input("\n1. Ver minhas respostas\n2. Voltar\nEscolha: ")
        if opcao == "1":
            ver_minhas_respostas(aluno, id_avaliacao)
        return
    
    # Se chegou aqui, pode responder a avaliação
    print(f"\n📝 RESPONDER AVALIAÇÃO: {info_avaliacao[1]}")
    print(f"Tipo: {info_avaliacao[2]} | Peso: {info_avaliacao[5]:.2f}")
    if info_avaliacao[3]:
        print(f"Descrição: {info_avaliacao[3]}")
    
    # Buscar perguntas da avaliação
    query = f"""SELECT p.id_pergunta, p.texto, p.tipo, p.peso, 
               p.opcoes, p.resposta_correta
               FROM pergunta p 
               WHERE p.id_avaliacao = {id_avaliacao}
               ORDER BY p.numero_ordem"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        perguntas = cursor.fetchall()
        
        if not perguntas:
            print("Esta avaliação não tem perguntas definidas.")
            cursor.close()
            return
        
        print(f"\nEsta avaliação contém {len(perguntas)} pergunta(s).")
        print("Deseja começar a responder? (s/n): ")
        if input().lower() != 's':
            print("Resposta cancelada.")
            cursor.close()
            return
        
        # Coletar respostas para cada pergunta
        respostas = []
        
        for pergunta in perguntas:
            print(f"\nPergunta {pergunta[0]}: {pergunta[1]}")
            print(f"Tipo: {pergunta[2]} | Peso: {pergunta[3]:.2f}")
            
            if pergunta[4]:  # Se tem opções (para múltipla escolha)
                opcoes = pergunta[4].split(';')
                print("Opções:")
                for j, opcao in enumerate(opcoes, 1):
                    print(f"  {j}. {opcao}")
            
            resposta_aluno = input("Sua resposta: ").strip()
            
            if resposta_aluno:
                respostas.append((pergunta[0], resposta_aluno))
            else:
                print("Pergunta pulada (resposta em branco)")
        
        if respostas:
            print(f"\nSalvando {len(respostas)} resposta(s)...")
            
            insert_resposta = f"""INSERT INTO resposta_atividade 
                                (id_aluno, id_avaliacao, data_resposta, status) 
                                VALUES ({aluno.id}, {id_avaliacao}, NOW(), 'submetida')"""
            cursor.execute(insert_resposta)
            id_resposta = cursor.lastrowid
            
            # Salvar cada resposta individual
            for id_pergunta, resposta in respostas:
                insert_detalhe = f"""INSERT INTO resposta_detalhe 
                                   (id_resposta, id_pergunta, resposta_aluno) 
                                   VALUES ({id_resposta}, {id_pergunta}, '{resposta}')"""
                cursor.execute(insert_detalhe)
            
            conn.commit()
            print("Respostas salvas com sucesso!")
            print("O professor irá corrigir e lançar a nota posteriormente.")
        else:
            print("Nenhuma resposta foi fornecida.")
        
        cursor.close()
        
    except Error as e:
        print(f"Erro ao responder avaliação: {e}")

def ver_minhas_respostas(aluno, id_avaliacao):
    query = f"""SELECT r.data_resposta, r.status, 
               p.texto as pergunta, rd.resposta_aluno,
               p.resposta_correta, p.tipo, p.peso
               FROM resposta_atividade r 
               JOIN resposta_detalhe rd ON r.id_resposta = rd.id_resposta
               JOIN pergunta p ON rd.id_pergunta = p.id_pergunta
               WHERE r.id_aluno = {aluno.id} AND r.id_avaliacao = {id_avaliacao}
               ORDER BY p.numero_ordem"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        respostas = cursor.fetchall()
        
        if respostas:
            print(f"\n📋 SUAS RESPOSTAS:")
            print(f"Data de submissão: {respostas[0][0]}")
            print(f"Status: {respostas[0][1]}")
            
            for i, resposta in enumerate(respostas, 1):
                print(f"\n{i}. {resposta[2]}")
                print(f"   Tipo: {resposta[5]} | Peso: {resposta[6]:.2f}")
                print(f"   Sua resposta: {resposta[3]}")
                
                if resposta[4]:  # Se tem resposta correta definida
                    print(f"   Resposta correta: {resposta[4]}")
                    
                    # Verificar se acertou (apenas para comparação)
                    if resposta[3].strip().lower() == resposta[4].strip().lower():
                        print("   ✅ Resposta correta!")
                    else:
                        print("   ❌ Resposta incorreta")
        
        cursor.close()
    except Error as e:
        print(f"Erro ao buscar respostas: {e}")

def ver_historico_cursos(aluno):
    print("\n=== MEU HISTÓRICO DE CURSOS ===")
    
    query = f"""SELECT c.id_curso, c.nome as curso_nome, 
               COUNT(DISTINCT t.id_turma) as total_turmas,
               MIN(m.data_matricula) as primeira_matricula,
               MAX(m.data_matricula) as ultima_matricula,
               GROUP_CONCAT(DISTINCT t.codigo_turma SEPARATOR ', ') as turmas,
               AVG(n.valor_nota) as media_curso,
               MAX(CASE WHEN m.status = 'concluido' THEN 1 ELSE 0 END) as curso_concluido
               FROM curso c 
               JOIN turma t ON c.id_curso = t.id_curso
               JOIN matricula m ON t.id_turma = m.id_turma
               LEFT JOIN avaliacao av ON t.id_turma = av.id_turma
               LEFT JOIN nota n ON av.id_avaliacao = n.id_avaliacao AND n.id_aluno = {aluno.id}
               WHERE m.id_aluno = {aluno.id}
               GROUP BY c.id_curso, c.nome
               ORDER BY MAX(m.data_matricula) DESC"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursos = cursor.fetchall()
        
        if cursos:
            print(f"\n📊 Você já cursou {len(cursos)} curso(s) diferentes:")
            
            total_horas = 0
            cursos_concluidos = 0
            
            for i, curso in enumerate(cursos, 1):
                status = "✅ Concluído" if curso[7] else "📚 Cursando"
                print(f"\n{i}. {curso[1]} - {status}")
          

# Funções de Relatórios
def relatorio_alunos_por_turma():
	print("\n----- ALUNOS POR TURMA -----")
	
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
	print("\n----- MÉDIAS POR TURMA -----")
	
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
	print("\n----- ALUNOS ABAIXO DA MÉDIA (<5) -----")
	
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
		

def identificar_professores_alunos():
	"""Identifica professores que também são alunos"""
	print("\n----- PROFESSORES QUE TAMBÉM SÃO ALUNOS -----")
	
	query = """SELECT u.id_usuario, u.nome, u.email, 
			   p.especialidade, a.ra, 
			   COUNT(DISTINCT m.id_turma) as turmas_como_aluno 
			   FROM usuario u 
			   JOIN professor p ON u.id_usuario = p.id_professor 
			   JOIN aluno a ON u.id_usuario = a.id_aluno 
			   LEFT JOIN matricula m ON u.id_usuario = m.id_aluno AND m.status = 'matriculado' 
			   WHERE u.is_professor = TRUE AND u.is_aluno = TRUE 
			   GROUP BY u.id_usuario 
			   ORDER BY u.nome"""
	
	try:
		cursor = conn.cursor()
		cursor.execute(query)
		results = cursor.fetchall()
		
		print(f"\n{'ID':<5} {'Nome':<30} {'Email':<30} {'Especialidade':<25} {'RA':<12} {'Turmas como Aluno':<15}")
		print("-" * 120)
		
		count = 0
		for row in results:
			print(f"{row[0]:<5} {row[1]:<30} {row[2]:<30} {row[3] if row[3] else 'N/A':<25} {row[4]:<12} {row[5]:<15}")
			count += 1
		
		if count == 0:
			print("Nenhum professor encontrado que também seja aluno.\n")
		else:
			print(f"\nTotal: {count} professor(es) que também são aluno(s)")
		
		cursor.close()
	except Error as e:
		print(f"Erro na consulta: {e}")

def identificar_aluno_mais_cursos():
    """Identifica qual aluno fez mais cursos"""
    print("\n--- ALUNO COM MAIS CURSOS ---")
    
    query = """SELECT u.id_usuario, u.nome, a.ra, 
               COUNT(DISTINCT c.id_curso) as total_cursos
               FROM usuario u 
               JOIN aluno a ON u.id_usuario = a.id_aluno
               JOIN matricula m ON u.id_usuario = m.id_aluno
               JOIN turma t ON m.id_turma = t.id_turma
               JOIN curso c ON t.id_curso = c.id_curso
               WHERE m.status IN ('matriculado', 'concluido', 'aprovado')
               GROUP BY u.id_usuario, u.nome, a.ra
               ORDER BY total_cursos DESC, u.nome
               LIMIT 1"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            print(f"\n🎓 ALUNO COM MAIS CURSOS:")
            print(f"ID: {result[0]}")
            print(f"Nome: {result[1]}")
            print(f"RA: {result[2]}")
            print(f"Total de cursos diferentes: {result[3]}")
            
            # Mostrar detalhes dos cursos
            query_detalhes = f"""SELECT DISTINCT c.nome, m.status, m.data_matricula
                                 FROM curso c 
                                 JOIN turma t ON c.id_curso = t.id_curso
                                 JOIN matricula m ON t.id_turma = m.id_turma
                                 WHERE m.id_aluno = {result[0]} 
                                 AND m.status IN ('matriculado', 'concluido', 'aprovado')"""
            
            cursor.execute(query_detalhes)
            cursos = cursor.fetchall()
            
            if cursos:
                print(f"\n Cursos matriculados/aprovados:")
                for i, curso in enumerate(cursos, 1):
                    print(f"  {i}. {curso[0]} - Status: {curso[1]} - Data: {curso[2]}")
        else:
            print("Nenhum aluno encontrado com matrículas em cursos.")
        
        cursor.close()
    except Error as e:
        print(f"Erro na consulta: {e}")

def indicar_professor_mais_turmas_ativas():
    """Indica o professor com maior número de turmas ativas"""
    print("\n--- PROFESSOR COM MAIS TURMAS ATIVAS ---")
    
    query = """SELECT u.id_usuario, u.nome, u.email, 
               COUNT(DISTINCT t.id_turma) as total_turmas_ativas,
               GROUP_CONCAT(DISTINCT c.nome SEPARATOR '; ') as cursos_ministrados
               FROM usuario u 
               JOIN professor p ON u.id_usuario = p.id_professor
               JOIN turma t ON u.id_usuario = t.id_professor
               JOIN curso c ON t.id_curso = c.id_curso
               WHERE t.ativa = 1
               GROUP BY u.id_usuario, u.nome, u.email
               ORDER BY total_turmas_ativas DESC, u.nome
               LIMIT 1"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            print(f"\n PROFESSOR COM MAIS TURMAS ATIVAS:")
            print(f"ID: {result[0]}")
            print(f"Nome: {result[1]}")
            print(f"Email: {result[2]}")
            print(f"Total de turmas ativas: {result[3]}")
            
            if result[4]:
                print(f"Cursos ministrados: {result[4]}")
            
            # Mostrar detalhes das turmas
            query_turmas = f"""SELECT t.codigo_turma, t.periodo, c.nome as curso_nome,
                               t.vagas_ocupadas, t.vagas_totais,
                               COUNT(DISTINCT m.id_aluno) as total_alunos_matriculados
                               FROM turma t 
                               JOIN curso c ON t.id_curso = c.id_curso
                               LEFT JOIN matricula m ON t.id_turma = m.id_turma AND m.status = 'matriculado'
                               WHERE t.id_professor = {result[0]} AND t.ativa = 1
                               GROUP BY t.id_turma, t.codigo_turma, t.periodo, c.nome, 
                                        t.vagas_ocupadas, t.vagas_totais
                               ORDER BY t.periodo, t.codigo_turma"""
            
            cursor.execute(query_turmas)
            turmas = cursor.fetchall()
            
            if turmas:
                print(f"\nTurmas ativas deste professor:")
                for i, turma in enumerate(turmas, 1):
                    ocupacao = (turma[3] / turma[4] * 100) if turma[4] > 0 else 0
                    print(f"  {i}. {turma[0]} - Período: {turma[1]}")
                    print(f"     Curso: {turma[2]}")
                    print(f"     Alunos: {turma[5]}/{turma[4]} ({ocupacao:.1f}% ocupação)")
        else:
            print("Nenhum professor encontrado com turmas ativas.")
        
        cursor.close()
    except Error as e:
        print(f"Erro na consulta: {e}")

def listar_top3_turmas_melhor_desempenho():
    """Lista as 3 turmas que tiveram o melhor desempenho médio"""
    print("\n--- TOP 3 TURMAS COM MELHOR DESEMPENHO MÉDIO ---")
    
    query = """SELECT t.id_turma, t.codigo_turma, c.nome as curso_nome, 
               u.nome as professor_nome, t.periodo,
               AVG(n.valor_nota) as media_geral,
               COUNT(DISTINCT m.id_aluno) as total_alunos,
               COUNT(DISTINCT n.id_aluno) as alunos_com_nota
               FROM turma t 
               JOIN curso c ON t.id_curso = c.id_curso
               JOIN usuario u ON t.id_professor = u.id_usuario
               LEFT JOIN matricula m ON t.id_turma = m.id_turma AND m.status = 'matriculado'
               LEFT JOIN avaliacao av ON t.id_turma = av.id_turma
               LEFT JOIN nota n ON av.id_avaliacao = n.id_avaliacao
               WHERE t.ativa = 1 AND n.valor_nota IS NOT NULL
               GROUP BY t.id_turma, t.codigo_turma, c.nome, u.nome, t.periodo
               HAVING COUNT(DISTINCT n.id_avaliacao) > 0  -- Tem pelo menos uma avaliação com nota
               ORDER BY media_geral DESC, total_alunos DESC
               LIMIT 3"""
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            print("\n TOP 3 TURMAS COM MELHOR DESEMPENHO:")
            
            for i, turma in enumerate(results, 1):
                print(f"\n{i}º LUGAR:")
                print(f"  Código: {turma[1]}")
                print(f"  Curso: {turma[2]}")
                print(f"  Professor: {turma[3]}")
                print(f"  Período: {turma[4]}")
                print(f"  Média geral: {turma[5]:.2f}")
                print(f"  Total de alunos: {turma[6]}")
                print(f"  Alunos com notas registradas: {turma[7]}")
                
                # Calcular faixa de notas para esta turma
                query_faixa = f"""SELECT MIN(n.valor_nota), MAX(n.valor_nota), 
                                 COUNT(CASE WHEN n.valor_nota >= 7 THEN 1 END) as aprovados,
                                 COUNT(CASE WHEN n.valor_nota >= 5 AND n.valor_nota < 7 THEN 1 END) as recuperacao,
                                 COUNT(CASE WHEN n.valor_nota < 5 THEN 1 END) as reprovados
                                 FROM nota n 
                                 JOIN avaliacao av ON n.id_avaliacao = av.id_avaliacao
                                 WHERE av.id_turma = {turma[0]}"""
                
                cursor.execute(query_faixa)
                faixa = cursor.fetchone()
                
                if faixa and faixa[0] is not None:
                    total_alunos_nota = sum(faixa[2:5]) or 1  # Evita divisão por zero
                    print(f"  Faixa de notas: {faixa[0]:.1f} - {faixa[1]:.1f}")
                    print(f"  Aprovados (≥7): {faixa[2]} ({faixa[2]/total_alunos_nota*100:.1f}%)")
                    print(f"  Recuperação (5-7): {faixa[3]} ({faixa[3]/total_alunos_nota*100:.1f}%)")
                    print(f"  Reprovados (<5): {faixa[4]} ({faixa[4]/total_alunos_nota*100:.1f}%)")
                
                # Listar avaliações desta turma
                query_avaliacoes = f"""SELECT titulo, tipo, peso, COUNT(DISTINCT n.id_aluno) as alunos_avaliados
                                       FROM avaliacao 
                                       LEFT JOIN nota n ON avaliacao.id_avaliacao = n.id_avaliacao
                                       WHERE id_turma = {turma[0]}
                                       GROUP BY avaliacao.id_avaliacao, titulo, tipo, peso"""
                
                cursor.execute(query_avaliacoes)
                avaliacoes = cursor.fetchall()
                
                if avaliacoes:
                    print(f"  Avaliações aplicadas: {len(avaliacoes)}")
                    for j, avaliacao in enumerate(avaliacoes, 1):
                        print(f"    {j}. {avaliacao[0]} ({avaliacao[1]}) - Peso: {avaliacao[2]:.2f} - Alunos: {avaliacao[3]}")
        else:
            print("Nenhuma turma encontrada com notas registradas.")
        
        cursor.close()
    except Error as e:
        print(f"Erro na consulta: {e}")

def relatorio_estatisticas_gerais():
    """Relatório completo com todas as estatísticas principais"""
    print("\n--- RELATÓRIO DE ESTATÍSTICAS GERAIS ---")
    
    try:
        cursor = conn.cursor()
        
        # 1. Estatísticas básicas
        print("\nESTATÍSTICAS BÁSICAS:")
        
        # Total de usuários por tipo
        query_usuarios = """SELECT 
                           SUM(is_admin) as admins,
                           SUM(is_professor) as professores,
                           SUM(is_aluno) as alunos,
                           COUNT(*) as total
                           FROM usuario"""
        cursor.execute(query_usuarios)
        stats_usuarios = cursor.fetchone()
        print(f"  Total de usuários: {stats_usuarios[3]}")
        print(f"  • Administradores: {stats_usuarios[0]}")
        print(f"  • Professores: {stats_usuarios[1]}")
        print(f"  • Alunos: {stats_usuarios[2]}")
        
        # Total de cursos e turmas
        query_cursos = """SELECT COUNT(DISTINCT id_curso) as total_cursos, COUNT(DISTINCT id_turma) as total_turmas, SUM(vagas_ocupadas) as total_matriculados FROM turma WHERE ativa = TRUE"""
        cursor.execute(query_cursos)
        stats_cursos = cursor.fetchone()
        print(f"\n  Total de cursos ativos: {stats_cursos[0]}")
        print(f"  Total de turmas ativas: {stats_cursos[1]}")
        print(f"  Total de matrículas ativas: {stats_cursos[2]}")
        
        # 2. Chamar as funções específicas
        print("\n" + "="*50)
        identificar_aluno_mais_cursos()
        
        print("\n" + "="*50)
        indicar_professor_mais_turmas_ativas()
        
        print("\n" + "="*50)
        listar_top3_turmas_melhor_desempenho()
        
        # 3. Estatísticas de desempenho geral
        print("\n" + "="*50)
        print("\n ESTATÍSTICAS DE DESEMPENHO:")
        
        query_desempenho = """SELECT AVG(n.valor_nota) as media_geral, MIN(n.valor_nota) as nota_minima, MAX(n.valor_nota) as nota_maxima, COUNT(DISTINCT n.id_aluno) as alunos_com_nota,COUNT(DISTINCT n.id_avaliacao) as avaliacoes_aplicadas FROM nota n"""
        cursor.execute(query_desempenho)
        desempenho = cursor.fetchone()
        
        if desempenho and desempenho[0] is not None:
            print(f"  Média geral de todas as turmas: {desempenho[0]:.2f}")
            print(f"  Nota mais baixa registrada: {desempenho[1]:.1f}")
            print(f"  Nota mais alta registrada: {desempenho[2]:.1f}")
            print(f"  Alunos com notas registradas: {desempenho[3]}")
            print(f"  Total de avaliações aplicadas: {desempenho[4]}")
        
        cursor.close()
        
    except Error as e:
        print(f"Erro no relatório: {e}")

# -----------------------

# Menus Principais separados por tipo de usuário
def menu_administrador(admin):
    """Menu do administrador com todas as funcionalidades"""
    while True:
        print("\n--- SISTEMA DE GESTÃO ACADÊMICA - ADMINISTRADOR ---")
        print("\n--- GESTÃO DE USUÁRIOS ---")
        print("1. Cadastrar usuário")
        print("2. Editar usuário")
        
        print("\n--- GESTÃO DE CURSOS E TURMAS ---")
        print("3. Gerenciar cursos")
        print("4. Criar turma")
        
        print("\n--- RELATÓRIOS E ESTATÍSTICAS ---")
        print("5. Relatório: Alunos por turma")
        print("6. Relatório: Médias por turma")
        print("7. Relatório: Alunos abaixo da média")
        print("8. Identificar professores que também são alunos")
        print("9. Aluno com mais cursos")  
        print("10. Professor com mais turmas ativas")  
        print("11. Top 3 turmas com melhor desempenho")  
        print("12. Relatório completo de estatísticas")  
        
        print("\n--- SAIR ---")
        print("13. Sair")
        
        opcao = input("\nEscolha: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            menu_editar_usuario(admin)
        elif opcao == "3":
            gerenciar_cursos()
        elif opcao == "4":
            criar_turma()
        elif opcao == "5":
            relatorio_alunos_por_turma()
        elif opcao == "6":
            relatorio_medias_turmas()
        elif opcao == "7":
            relatorio_alunos_abaixo_media()
        elif opcao == "8":
            identificar_professores_alunos()
        elif opcao == "9":
            identificar_aluno_mais_cursos()
        elif opcao == "10":
            indicar_professor_mais_turmas_ativas()
        elif opcao == "11":
            listar_top3_turmas_melhor_desempenho()
        elif opcao == "12":
            relatorio_estatisticas_gerais()
        elif opcao == "13":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
        
        if opcao != "13":
            pressione_para_continuar()


def menu_professor(professor):
	while True:
		print("\n----- SISTEMA DE GESTÃO ACADÊMICA - PROFESSOR -----")
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



def menu_professor_aluno(usuario):
	while True:
		print("\n----- SISTEMA DE GESTÃO ACADÊMICA - PROFESSOR/ALUNO -----")
		print("1. Acessar como Professor")
		print("2. Acessar como Aluno")
		print("3. Sair")
		opcao = input("Escolha: ")

		if opcao == "1":
			menu_professor(usuario)
		elif opcao == "2":
			menu_aluno(usuario)
		elif opcao == "3":
			print("Saindo...")
			break
		else:
			print("Opção inválida!")



def menu_aluno(aluno):
    """Menu do aluno com todas as funcionalidades"""
    while True:
        print(f"\n=== SISTEMA DE GESTÃO ACADÊMICA - ALUNO ===")
        print(f"Olá, {aluno.nome}!")
        
        print("\n--- MATRÍCULAS E CURSOS ---")
        print("1. Matricular em nova turma")
        print("2. Ver minhas turmas matriculadas")  # NOVA OPÇÃO
        print("3. Ver histórico de cursos")  # NOVA OPÇÃO
        
        print("\n--- ESTUDOS E AVALIAÇÕES ---")
        print("4. Acessar materiais e avaliações")  # NOVA OPÇÃO
        print("5. Visualizar minhas notas")
        print("6. Ver minhas respostas/entregas")  # NOVA OPÇÃO
        
        print("\n--- CONTA ---")
        print("7. Editar meus dados")
        
        print("\n--- SAIR ---")
        print("8. Sair")
        
        opcao = input("\nEscolha: ")

        if opcao == "1":
            matricular_turma(aluno)
        elif opcao == "2":  # NOVA OPÇÃO
            ver_turmas_matriculadas(aluno)
        elif opcao == "3":  # NOVA OPÇÃO
            ver_historico_cursos(aluno)
        elif opcao == "4":  # NOVA OPÇÃO
            ver_materiais_avaliacoes(aluno)
        elif opcao == "5":
            visualizar_notas(aluno)
        elif opcao == "6":  # NOVA OPÇÃO
            # Esta função já é chamada dentro de ver_materiais_avaliacoes,
            # mas podemos criar um acesso direto também
            id_turma = input("Digite o ID da turma (ou Enter para listar todas): ").strip()
            if id_turma and id_turma.isdigit():
                gerenciar_minhas_respostas(int(id_turma), aluno.id)
            else:
                # Primeiro listar as turmas
                query = f"SELECT id_turma, codigo_turma FROM matricula JOIN turma ON matricula.id_turma = turma.id_turma WHERE id_aluno = {aluno.id} AND status IN ('matriculado', 'cursando')"
                try:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    turmas = cursor.fetchall()
                    cursor.close()
                    
                    if turmas:
                        print("Suas turmas:")
                        for turma in turmas:
                            print(f"ID: {turma[0]} - Código: {turma[1]}")
                        
                        escolha = input("Digite o ID da turma: ")
                        if escolha.isdigit():
                            gerenciar_minhas_respostas(int(escolha), aluno.id)
                    else:
                        print("Você não está matriculado em nenhuma turma.")
                except Error as e:
                    print(f"Erro: {e}")
        elif opcao == "7":
            menu_editar_usuario(aluno)
        elif opcao == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
        
        if opcao != "8":
            pressione_para_continuar()

# ---------------------------

def main():
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
	elif usuario.tipo == "professor_aluno":
		menu_professor_aluno(usuario)
	elif usuario.tipo == "admin_professor":
		print("Usuário Administrador/Professor")
		menu_administrador(usuario)
	else:
		print(f"Tipo de usuário desconhecido: {usuario.tipo}")
	
	if conn:
		conn.close()

decision = True

while(decision):
	print("----- SISTEMA DE GESTÃO ACADÊMICA -----")
	d = int(input("\n\nO que você deseja fazer?\n1. login \n2. sair\n"))
	if d == 1:
		main()
	else:
		decision = False