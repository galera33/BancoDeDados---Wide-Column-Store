from astrapy import DataAPIClient
import random
import uuid
import names

from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("YOUR_TOKEN")
db = client.get_database_by_api_endpoint(
  "https://7ff40bfd-eabb-48dc-97ad-a901d85495f0-us-east-2.apps.astra.datastax.com"
)



# Dados aleatórios gerados
def gerar_ano_aleatorio():
    return random.randint(2019, 2024)

def gerar_semestre_aleatorio():
    return random.choice([1, 2])

def gerar_nota_aleatoria():
    return round(random.uniform(0, 100), 2)

def escolha_aleatoria(max_valor):
    return random.randint(1, max_valor)

def obter_disciplinas():
    return [
        "Matemática", "Física", "Química", "Biologia",
        "História", "Geografia", "Literatura", "Ciência da Computação"
    ]

# Distribui disciplinas entre professores, garantindo que cada professor tenha pelo menos uma disciplina.
def distribuir_disciplinas_para_professores(num_professores, disciplinas):
    disciplina_para_professor = {}
    professor_ids = list(range(1, num_professores + 1))
    num_disciplinas = len(disciplinas)
    
    for professor_id in professor_ids:
        disciplina_id = None
        for i in range(1, num_disciplinas + 1):
            if i not in disciplina_para_professor:
                disciplina_id = i
                break
        if disciplina_id:
            disciplina_para_professor[disciplina_id] = professor_id
    
    for disciplina_id in range(1, num_disciplinas + 1):
        if disciplina_id not in disciplina_para_professor:
            professor_id = random.choice(professor_ids)
            disciplina_para_professor[disciplina_id] = professor_id
    
    return disciplina_para_professor
# Cria e retorna um mapeamento de IDs para nomes de disciplinas.
def criar_mapeamento_disciplinas(disciplinas):
    mapeamento = {}
    for i in range(1, len(disciplinas) + 1):
        mapeamento[i] = disciplinas[i-1]
    return mapeamento

# Gera um dicionário de nomes aleatórios para alunos.
def gerar_nomes_alunos(quantidade):
    nomes = {}
    for aluno_id in range(1, quantidade + 1):
        nomes[aluno_id] = names.get_full_name()
    return nomes

# Gera um dicionário de nomes aleatórios para professores.
def gerar_nomes_professores(quantidade):
    nomes = {}
    for professor_id in range(1, quantidade + 1):
        nomes[professor_id] = names.get_full_name()
    return nomes

# Insere alunos no banco de dados.
def inserir_alunos(db, nomes_alunos):
    alunos = []
    for aluno_id, nome in nomes_alunos.items():
        alunos.append({
            'id_aluno': aluno_id,
            'nome': nome
        })
    db['alunos_historico'].insert_many(alunos)
    return alunos

# Insere as relações entre professores e disciplinas.
def inserir_professores_disciplinas(db, nomes_professores, mapeamento_disciplinas, disciplina_para_professor):
    professores_disciplinas = []
    
    for disciplina_id, professor_id in disciplina_para_professor.items():
        if disciplina_id <= len(mapeamento_disciplinas) and professor_id in nomes_professores:
            professores_disciplinas.append({
                'id_professor': professor_id,
                'professor_nome': nomes_professores[professor_id],
                'id_disciplina': disciplina_id,
                'disciplina_nome': mapeamento_disciplinas[disciplina_id],
                'semestre': gerar_semestre_aleatorio(),
                'ano': gerar_ano_aleatorio()
            })
    
    if professores_disciplinas:
        db['professores_disciplinas'].insert_many(professores_disciplinas)
    return professores_disciplinas

# Insere departamentos no banco de dados.
def inserir_departamentos(db, nomes_professores, num_departamentos=3):
    departamentos = []
    for departamento_id in range(1, num_departamentos + 1):
        chefe_id = escolha_aleatoria(len(nomes_professores))
        departamentos.append({
            'id_departamento': departamento_id,
            'id_chefe_professor': chefe_id,
            'nome': f"Departamento {departamento_id}"
        })
    db['departamentos'].insert_many(departamentos)
    return departamentos

# Insere cursos associados a departamentos.
def inserir_cursos(db, num_departamentos=3, cursos_por_departamento=4):
    cursos = []
    for departamento_id in range(1, num_departamentos + 1):
        for curso_id in range(1, cursos_por_departamento + 1):
            cursos.append({
                'id_curso': curso_id,
                'id_departamento': departamento_id,
                'nome': f"Curso {curso_id}"
            })
    db['cursos'].insert_many(cursos)
    return cursos

# Insere matrizes curriculares para os cursos.
def inserir_matrizes_curriculares(db, num_cursos=4, matrizes_por_curso=2):
    matrizes = []
    for curso_id in range(1, num_cursos + 1):
        for matriz_id in range(1, matrizes_por_curso + 1):
            matrizes.append({
                'id_curso': curso_id,
                'curso_nome': f"Curso {curso_id}",
                'id_matriz': matriz_id
            })
    db['matrizes_curriculares'].insert_many(matrizes)
    return matrizes

def inserir_historicos(db, nomes_alunos, nomes_professores, mapeamento_disciplinas, disciplina_para_professor):

    historicos = []
    
    for aluno_id in nomes_alunos.keys():
        disciplina_id = escolha_aleatoria(len(mapeamento_disciplinas))
        
        if disciplina_id in disciplina_para_professor:
            professor_id = disciplina_para_professor[disciplina_id]
        else:
            professor_id = escolha_aleatoria(len(nomes_professores))
        historicos.append({
            'id_aluno': aluno_id,
            'id_historico': str(uuid.uuid4()),
            'ano': gerar_ano_aleatorio(),
            'semestre': gerar_semestre_aleatorio(),
            'nota_final': gerar_nota_aleatoria(),
            'id_disciplina': disciplina_id,
            'disciplina_nome': mapeamento_disciplinas[disciplina_id],
            'id_professor': professor_id,
            'professor_nome': nomes_professores[professor_id]
        })
    
    for aluno_id in nomes_alunos.keys():
        num_extras = random.randint(4, 9)
        
        for _ in range(num_extras):
            disciplina_id = escolha_aleatoria(len(mapeamento_disciplinas))
            if disciplina_id in disciplina_para_professor:
                professor_id = disciplina_para_professor[disciplina_id]
            else:
                professor_id = escolha_aleatoria(len(nomes_professores))
            
            historicos.append({
                'id_aluno': aluno_id,
                'id_historico': str(uuid.uuid4()),
                'ano': gerar_ano_aleatorio(),
                'semestre': gerar_semestre_aleatorio(),
                'nota_final': gerar_nota_aleatoria(),
                'id_disciplina': disciplina_id,
                'disciplina_nome': mapeamento_disciplinas[disciplina_id],
                'id_professor': professor_id,
                'professor_nome': nomes_professores[professor_id]
            })
    
    db['alunos_historico'].insert_many(historicos)
    return historicos

# Insere grupos de TCC.
def inserir_grupos_tcc(db, nomes_alunos, nomes_professores, num_grupos=5):
    grupos = []
    for grupo_id in range(1, num_grupos + 1):
        aluno1_id = escolha_aleatoria(len(nomes_alunos))
        # Garantir que o segundo aluno é diferente do primeiro
        aluno2_id = aluno1_id
        while aluno2_id == aluno1_id:
            aluno2_id = escolha_aleatoria(len(nomes_alunos))
            
        professor_id = escolha_aleatoria(len(nomes_professores))
        
        grupos.append({
            'id_grupo_tcc': str(uuid.uuid4()),
            'tema': f"Tema {grupo_id}",
            'id_aluno1': aluno1_id,
            'aluno1_nome': nomes_alunos[aluno1_id],
            'id_aluno2': aluno2_id,
            'aluno2_nome': nomes_alunos[aluno2_id],
            'id_professor': professor_id,
            'professor_nome': nomes_professores[professor_id]
        })
    
    db['grupos_tcc'].insert_many(grupos)
    return grupos

# Função principal que coordena a execução do programa.
def principal():
    
    # Preparar dados
    disciplinas = obter_disciplinas()
    mapeamento_disciplinas = criar_mapeamento_disciplinas(disciplinas)
    
    # Número de professores e alunos
    num_professores = 5
    num_alunos = 10
    
    nomes_alunos = gerar_nomes_alunos(num_alunos)
    nomes_professores = gerar_nomes_professores(num_professores)
    
    # Distribuir disciplinas entre professores aleatoriamente
    disciplina_para_professor = distribuir_disciplinas_para_professores(num_professores, disciplinas)
    
    # Inserir dados no banco
    inserir_alunos(db, nomes_alunos)
    inserir_professores_disciplinas(db, nomes_professores, mapeamento_disciplinas, disciplina_para_professor)
    inserir_departamentos(db, nomes_professores)
    inserir_cursos(db)
    inserir_matrizes_curriculares(db)
    inserir_historicos(db, nomes_alunos, nomes_professores, mapeamento_disciplinas, disciplina_para_professor)
    inserir_grupos_tcc(db, nomes_alunos, nomes_professores)
    
    print("Dados inseridos com nomes aleatórios com sucesso!")

if __name__ == "__main__":
    principal()
