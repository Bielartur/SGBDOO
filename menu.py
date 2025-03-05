from modelos import Usuario, Funcionario, Livro, Emprestimo
from biblioteca_db import BibliotecaDB
import transaction

from typing import Literal
from time import sleep
import os

# Formatação de dados
def formatar_cpf(cpf: str) -> str:
    cpf_separado = list(cpf)
    cpf_separado.insert(3, '.')
    cpf_separado.insert(7, '.')
    cpf_separado.insert(11, '-')

    cpf = ''.join(cpf_separado)
    return cpf

# Cores
def amarelo(texto: str) -> str:
    return f'\033[33m{texto}\033[0m'

def verde(texto: str) -> str:
    return f'\033[32m{texto}\033[0m'

def vermelho(texto:str) -> str:
    return f'\033[31m{texto}\033[0m'

def azul(texto: str) -> str:
    return f'\033[34m{texto}\033[0m'

# Funcionalidades principais

def identificar_nova_matricula(db: BibliotecaDB, e_usuario: bool) -> str:
    if e_usuario:
        primeira_letra = 'U'
        usuarios = db.listar_usuarios()
        ultima_matricula = usuarios[-1].numero_cartao if usuarios else 'U000'
    else:
        primeira_letra = 'F'
        funcionarios = db.listar_funcionarios()
        ultima_matricula = funcionarios[-1].matricula if funcionarios else 'F000'
    
    num_nova_matricula = int(ultima_matricula[1:]) + 1
    
    # Verifica quantos algarismos tem o número
    if num_nova_matricula / 100 >= 1:
        nova_matricula = primeira_letra + str(num_nova_matricula)

    elif num_nova_matricula / 10 >= 1:
        nova_matricula = primeira_letra + '0' + str(num_nova_matricula)

    elif num_nova_matricula / 10 < 1:
        nova_matricula = primeira_letra + '00' + str(num_nova_matricula)

    return nova_matricula

def identificar_novo_id(db: BibliotecaDB, tipo: Literal['Livro', 'Empréstimo', 'Usuário', 'Funcionário']) -> int:
    listas = {
        'Usuário': db.listar_usuarios(),
        'Funcionário': db.listar_funcionarios(),
        'Livro': db.listar_livros_existentes(),
        'Empréstimo': db.listar_emprestimos_existentes(),
    }
    ultimo_id = listas[tipo][-1].id if listas[tipo] else 0
    return ultimo_id + 1


def cadastrar_usuario(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Usuário')
    nova_matricula = identificar_nova_matricula(db, e_usuario=True)

    nome = input('Nome: ')
    cpf = formatar_cpf(input('CPF: '))
    email = input('Email: ')

    usuario = Usuario(novo_id, nome, cpf, email, nova_matricula)
    db.salvar_usuario(usuario)
    print(f'{amarelo('IMPORTANTE')}: Sua matrícula é {amarelo(nova_matricula)}')
    print(verde('Usuário cadastrado com sucesso'))

def cadastrar_funcionario(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Usuário')
    nova_matricula = identificar_nova_matricula(db, e_usuario=False)

    nome = input('Nome: ')
    cpf = formatar_cpf(input('CPF(apenas numeros): ').strip())
    email = input('Email: ')
    cargo = input('Cargo: ')

    funcionario = Funcionario(novo_id, nome, cpf, email, nova_matricula, cargo)
    db.salvar_funcionario(funcionario)
    print(f'{amarelo('IMPORTANTE')}: Sua matrícula é {amarelo(nova_matricula)}')
    print(verde('Funcionário cadastrado com sucesso'))
    
def logar_usuario(db: BibliotecaDB) -> bool:
    numero_cartao = input('Numero do cartão: ').upper()
    usuario = db.buscar_usuario_por_cartao(numero_cartao)
    if not usuario:
        print(f'O usuário de número de cartão {amarelo(numero_cartao)} não existe')
        return usuario, False
    
    cpf = formatar_cpf(input('CPF(apenas numeros): '))
    if usuario.cpf == cpf:
        print('Carregando...')
        sleep(1)
        print(verde('Usuário logado com sucesso'))
        return usuario, True
    else:
        print('CPF incorreto')
        return usuario, False
    
def logar_funcionario(db: BibliotecaDB) -> bool:
    matricula = input('Matricula: ').upper()
    funcionario = db.buscar_funcionario_por_matricula(matricula)
    if not funcionario:
        print(f'O funcionário de matricula {amarelo(matricula)} não existe')
        return funcionario, False
    
    cpf = formatar_cpf(input('CPF(apenas numeros): '))
    if funcionario.cpf == cpf:
        print('Carregando...')
        sleep(1)
        print(verde('Funcionário logado com sucesso'))
        return funcionario, True
    else:
        print('CPF incorreto')
        print(funcionario.cpf)
        return funcionario, False
    
# Funções do funcionário
def cadastrar_livro(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Livro')

    titulo = input('Título: ')
    autor = input('Autor: ')
    isbn = input('ISBN: ')

    livro = Livro(novo_id, titulo, autor, isbn)
    db.salvar_livro(livro)
    print(verde('Livro cadastrado com sucesso'))

def editar_livros(db: BibliotecaDB) -> None:
    print(amarelo('Escolha o livro que vai editar:'))
    livros_disponiveis = ver_todos_livros(db, index=True)
    
    print('\n0 - Voltar')
    valido = False
    while not valido:
        opcao = int(input('Resposta: '))
        if opcao == 0:
            return
        elif opcao > len(livros_disponiveis) or opcao < 0:
            print('Selecione uma opção válida')
        else:
            valido = True
    
    livro = livros_disponiveis[opcao - 1]

    titulo = livro.titulo
    autor = livro.autor
    isbn = livro.isbn

    print('Informações atuais:')
    print(f'{verde('Título')}: {titulo}')
    print(f'{azul('Autor')}: {autor}')
    print(f'ISBN: {isbn}')

    print('\nO que você quer editar:')
    print('1 - Título')
    print('2 - Autor')
    print('3 - ISBN')
    print('4 - Tudo')
    print('\n0 - Voltar')

    opcao = int(input('Resposta: '))

    print('Editando:')
    if opcao == 0:
        return
    elif opcao == 1:
        titulo = input('Título: ')
    elif opcao == 2:
        autor = input('Autor: ')
    elif opcao == 3:
        isbn = input('ISBN: ')
    elif opcao == 4:
        titulo = input('Título: ')
        autor = input('Autor: ')
        isbn = input('ISBN: ')

    livro_editado = Livro(livro.id, titulo, autor, isbn)
    db.salvar_livro(livro_editado)
    print(verde('Livro editado com sucesso'))

def criar_emprestimo(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Empréstimo')

    numero_cartao = input('Número do cartão do usuário: ')
    usuario = db.buscar_usuario_por_cartao(numero_cartao)
    if not usuario:
        print(f'O usuário de número de cartão {amarelo(numero_cartao)} não existe')
        return

    isbn = input('ISBN do livro: ')
    livro = db.buscar_livro_por_isbn(isbn)
    if not usuario:
        print(f'O livro com o ISBN {isbn} não existe')
        return
    
    emprestimo = Emprestimo(novo_id, usuario, livro)
    db.salvar_emprestimo(emprestimo)
    print('Carregando...')
    sleep(1)
    print(verde('Empréstimo registrado com sucesso'))

def ver_livros_disponiveis(db: BibliotecaDB, index=False) -> None:
    print("\nLivros disponíveis:")
    livros_disponiveis = db.listar_livros_disponiveis()
    if len(livros_disponiveis) == 0:
        print('Nenhum livro disponível')
    
    if index:
        for i, livro in enumerate(livros_disponiveis):
            print(f"{i + 1} - {amarelo('Livro')}: {livro.titulo} - {azul(livro.autor)}")
    else:
        for livro in livros_disponiveis:
            print(f"{amarelo('Livro')}: {livro.titulo} - {azul(livro.autor)}")

    return livros_disponiveis

def ver_todos_livros(db: BibliotecaDB, index=False) -> None:
    print("\nLivros disponíveis:")
    livros_existentes = db.listar_livros_existentes()
    if len(livros_existentes) == 0:
        print('Nenhum livro cadastrado')
    
    if index:
        for i, livro in enumerate(livros_existentes):
            print(f"{i + 1} - {amarelo('Livro')}: {livro.titulo} - {azul(livro.autor)}")
    else:
        for livro in livros_existentes:
            print(f"{amarelo('Livro')}: {livro.titulo} - {azul(livro.autor)}")

    return livros_existentes

def ver_emprestimos_ativos(db: BibliotecaDB) -> None:
    print("\nEmpréstimos ativos:")
    emprestimos_ativos = db.listar_emprestimos_ativos()
    if len(emprestimos_ativos) == 0:
        print('Nenhum empréstimo ativo')
    for emp in emprestimos_ativos:
        print(f"Empréstimo: {verde('Usuário')}={emp.usuario.nome}, {amarelo('Livro')}={emp.livro.titulo}")

def devolver_livro(db: BibliotecaDB, usuario: Usuario) -> None:
    print('\nDigite o número do empréstimo que quer devolver:')
    print('Seus empréstimos:\n')
    emprestimos_ativos = db.listar_emprestimos_ativos()

    emprestimos_desse_usuario = []
    i = 0
    for emp in emprestimos_ativos:
        if emp.usuario.numero_cartao == usuario.numero_cartao:
            emprestimos_desse_usuario.append(emp)
            print(f"{i + 1} - {amarelo('Livro')}={emp.livro.titulo}, {azul('Autor')}={emp.livro.autor}")
            i += 1

    print('\n0 - Voltar')
    valido = False
    while not valido:
        opcao = int(input('Resposta: '))
        if opcao == 0:
            return
        elif opcao > len(emprestimos_desse_usuario) or opcao < 0:
            print('Selecione uma opção válida')
        else:
            valido = True
    emprestimos_ativos[opcao - 1].livro.disponivel = True
    emprestimos_ativos[opcao - 1].devolvido = True
    transaction.commit()
    print(verde('Empréstimo devolvido'))

def pegar_livro_emprestado(db: BibliotecaDB, usuario: Usuario) -> None:
    novo_id = identificar_novo_id(db, tipo='Empréstimo')

    valido = False
    while not valido:
        livros_disponiveis = ver_livros_disponiveis(db, index=True)
        print('\n0 - Voltar')
        opcao = int(input('Resposta: '))
        if opcao == 0:
            return
        elif opcao > len(livros_disponiveis):
            print('Selecione uma opção válida')
        else:
            valido = True
    livro = livros_disponiveis[opcao - 1]

    emprestimo = Emprestimo(novo_id, usuario, livro)
    db.salvar_emprestimo(emprestimo)
    print(verde('Empréstimo registrado com sucesso')) 

def menu_usuario(db: BibliotecaDB, usuario: Usuario):
    while True:
        print('\nO que deseja fazer:')
        print('1 - Ver livros disponíveis')
        print('2 - Devolver livro')
        print('3 - Pegar livro emprestado')
        print('4 - Voltar ao menu principal')
        print('0 - Sair')

        opcao = int(input('Resposta: '))

        if opcao == 1:
            ver_livros_disponiveis(db)
        elif opcao == 2:
            devolver_livro(db, usuario)
        elif opcao == 3:
            pegar_livro_emprestado(db, usuario)
        elif opcao == 4:
            return
        elif opcao == 0:
            exit()

def menu_funcionario(db: BibliotecaDB):
    while True:
        print('\nO que deseja fazer:')
        print('1 - Cadastrar livro')
        print('2 - Editar Livro')
        print('3 - Criar empréstimo')
        print('4 - Ver empréstimos ativos')
        print('5 - Ver livros disponíveis')
        print('6 - Voltar para o menu inicial')
        print('0 - Sair')

        opcao = int(input('Resposta: '))

        if opcao == 1:
            cadastrar_livro(db)
        elif opcao == 2:
            editar_livros(db)
        elif opcao == 3:
            criar_emprestimo(db)
        elif opcao == 4:
            ver_emprestimos_ativos(db)
        elif opcao == 5:
            ver_livros_disponiveis(db)
        elif opcao == 6:
            return
        elif opcao == 0:
            exit()

def menu():
    os.system('cls')
    db = BibliotecaDB()

    try:
        while True:
            print('\n1 - Fazer Login')
            print('2 - Cadastrar-se')
            print('0 - Sair')

            opcao = int(input('Resposta: '))

            if opcao == 1:
                print('\nFazer login como:')
                print('1 - Usuário')
                print('2 - Funcionário')
                print('3 - Voltar')

                opcao = int(input('Resposta: '))

                if opcao == 1:
                    usuario, logado = logar_usuario(db)
                    if logado:
                        menu_usuario(db, usuario)

                elif opcao == 2:
                    funcionario, logado = logar_funcionario(db)
                    if logado:
                        menu_funcionario(db)

            elif opcao == 2:
                print('\nCadastrar como:')
                print('1 - Usuário')
                print('2 - Funcionário')
                print('3 - Voltar')

                opcao = int(input('Resposta: '))

                if opcao == 1:
                    cadastrar_usuario(db)
                elif opcao == 2:
                    cadastrar_funcionario(db)

            elif opcao == 0:
                exit()
    finally:
        db.fechar()


if __name__ == '__main__':
    menu()
