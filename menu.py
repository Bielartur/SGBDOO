from modelos import Usuario, Funcionario, Livro, Emprestimo
from biblioteca_db import BibliotecaDB
import transaction

from typing import Literal
import os

# Formatação de dados
def formatar_cpf(cpf: str) -> str:
    cpf_separado = list(cpf)
    cpf_separado.insert(3, '.')
    cpf_separado.insert(7, '.')
    cpf_separado.insert(11, '-')

    cpf = ''.join(cpf_separado)
    return cpf

# Funcionalidades principais

def identificar_nova_matricula(db: BibliotecaDB, e_usuario: bool) -> str:
    if e_usuario:
        primeira_letra = 'U'
        ultima_matricula = db.listar_usuarios()[-1].numero_cartao
    else:
        primeira_letra = 'F'
        ultima_matricula = db.listar_funcionarios()[-1].matricula
    
    num_nova_matricula = int(ultima_matricula[1:]) + 1
    
    # Verifica se o número está entre 10 e 100
    if num_nova_matricula / 100 >= 1:
        nova_matricula = primeira_letra + str(num_nova_matricula)

    elif num_nova_matricula / 10 >= 1:
        nova_matricula = primeira_letra + '0' + str(num_nova_matricula)

    elif num_nova_matricula / 10 < 1:
        nova_matricula = primeira_letra + '00' + str(num_nova_matricula)

    return nova_matricula

def identificar_novo_id(db: BibliotecaDB, tipo: Literal['Livro', 'Empréstimo', 'Usuário', 'Funcionário']) -> int:

    if tipo == 'Usuário':
        ultimo_id = int(db.listar_usuarios()[-1].id)

    elif tipo == 'Funcionário':
        ultimo_id = int(db.listar_funcionarios()[-1].id)

    elif tipo == 'Livro':
        ultimo_id = int(db.listar_livros_existentes()[-1].id)

    elif tipo == 'Empréstimo':
        ultimo_id = int(db.listar_emprestimos_existentes()[-1].id)

    return ultimo_id + 1

def cadastrar_usuario(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Usuário')
    nova_matricula = identificar_nova_matricula(db, e_usuario=True)

    nome = input('Nome: ')
    cpf = formatar_cpf(input('CPF: '))
    email = input('Email: ')

    usuario = Usuario(novo_id, nome, cpf, email, nova_matricula)
    db.salvar_usuario(usuario)
    print(f'IMPORTANTE: Sua matrícula é {nova_matricula}')
    print('Usuário cadastrado com sucesso')

def cadastrar_funcionario(db: BibliotecaDB) -> None:
    novo_id = identificar_novo_id(db, tipo='Usuário')
    nova_matricula = identificar_nova_matricula(db, e_usuario=False)

    nome = input('Nome: ')
    cpf = formatar_cpf(input('CPF(apenas numeros): ').strip())
    email = input('Email: ')
    cargo = input('Cargo: ')

    funcionario = Funcionario(novo_id, nome, cpf, email, nova_matricula, cargo)
    db.salvar_funcionario(funcionario)
    print(f'IMPORTANTE: Sua matrícula é {nova_matricula}')
    print('Funcionário cadastrado com sucesso')
    
def logar_usuario(db: BibliotecaDB) -> bool:
    numero_cartao = input('Numero do cartão: ').upper()
    usuario = db.buscar_usuario_por_cartao(numero_cartao)
    if not usuario:
        print(f'O usuário de número de cartão {numero_cartao} não existe')
        return usuario, False
    
    cpf = formatar_cpf(input('CPF(apenas numeros): '))
    if usuario.cpf == cpf:
        print('Usuário logado com sucesso')
        return usuario, True
    else:
        print('CPF incorreto')
        return usuario, False
    
def logar_funcionario(db: BibliotecaDB) -> bool:
    matricula = input('Matricula: ').upper()
    funcionario = db.buscar_funcionario_por_matricula(matricula)
    if not funcionario:
        print(f'O funcionário de matricula {matricula} não existe')
        return funcionario, False
    
    cpf = formatar_cpf(input('CPF(apenas numeros): '))
    if funcionario.cpf == cpf:
        print('Funcionário logado com sucesso')
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
    print('Livro cadastrado com sucesso')

def criar_emprestimo(db: BibliotecaDB):
    novo_id = identificar_novo_id(db, tipo='Empréstimo')

    numero_cartao = input('Número do cartão do usuário: ')
    usuario = db.buscar_usuario_por_cartao(numero_cartao)
    if not usuario:
        print(f'O usuário de número de cartão {numero_cartao} não existe')
        return

    isbn = input('ISBN do livro: ')
    livro = db.buscar_livro_por_isbn(isbn)
    if not usuario:
        print(f'O livro com o ISBN {isbn} não existe')
        return
    
    emprestimo = Emprestimo(novo_id, usuario, livro)
    db.salvar_emprestimo(emprestimo)
    print('Empréstimo registrado com sucesso') 

def ver_livros_disponiveis(db: BibliotecaDB, index=False):
    print("\nLivros disponíveis:")
    livros_disponiveis = db.listar_livros_disponiveis()
    if len(livros_disponiveis) == 0:
        print('Nenhum livro disponível')
    
    if index:
        for i, livro in enumerate(livros_disponiveis):
            print(f"{i + 1} - Livro: {livro.titulo} - {livro.autor}")
    else:
        for livro in livros_disponiveis:
            print(f"Livro: {livro.titulo} - {livro.autor}")


    return livros_disponiveis

def ver_emprestimos_ativos(db: BibliotecaDB):
    print("\nEmpréstimos ativos:")
    emprestimos_ativos = db.listar_emprestimos_ativos()
    if len(emprestimos_ativos) == 0:
        print('Nenhum empréstimo ativo')
    for emp in emprestimos_ativos:
        print(f"Empréstimo: Usuário={emp.usuario.nome}, Livro={emp.livro.titulo}")

def devolver_livro(db: BibliotecaDB, usuario: Usuario) -> None:
    print('\nDigite o número do empréstimo que quer devolver:')
    print('Seus empréstimos:\n')
    emprestimos_ativos = db.listar_emprestimos_ativos()

    emprestimos_desse_usuario = []
    i = 0
    for emp in emprestimos_ativos:
        if emp.usuario.numero_cartao == usuario.numero_cartao:
            emprestimos_desse_usuario.append(emp)
            print(f"{i + 1} - Livro={emp.livro.titulo}, Autor={emp.livro.autor}")
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
    print('Empréstimo devolvido')

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
    print('Empréstimo registrado com sucesso') 

def menu():
    os.system('cls')
    db = BibliotecaDB()

    try:
        opcao = 10
        while opcao != 0:
            opcao = int(input('\n1 - Fazer Login\n2 - Cadastrar-se\n0 - Sair\nResposta: '))
            
            if opcao == 1:
                print('\nFazer login como:')
                opcao = int(input('1 - Usuário\n2 - Funcionário\n3 - Voltar\nResposta: '))
                if opcao == 1:
                    usuario, logado = logar_usuario(db)

                    if logado:
                        voltar = True
                        while voltar:
                            print('\nO que deseja fazer:')
                            opcao = int(input('1 - Ver livros disponíveis\n2 - Devolver livro\n3 - Pegar livro emprestado\n4 - Voltar ao menu principal\n0 - Sair\nResposta: '))
                            
                            if opcao == 1:
                                ver_livros_disponiveis(db)

                            elif opcao == 2:
                                devolver_livro(db, usuario)
                                continue

                            elif opcao == 3:
                                pegar_livro_emprestado(db, usuario)
                                continue

                            elif opcao == 4:
                                break

                            elif opcao == 0:
                                break

                            if opcao in [1, 2]:
                                    opcao = int(input('\n1 - Voltar\n0 - Sair\nResposta: '))

                                    if opcao == 1:
                                        voltar = True
                                    else:
                                        break

                elif opcao == 2:
                    funcionario, logado = logar_funcionario(db)

                    if logado:
                        voltar = True
                        while voltar:
                            print('\nO que deseja fazer:')
                            opcao = int(input('1 - Cadastrar livro\n2 - Criar empréstimo\n3 - Ver empréstimos ativos\n4 - Ver livros disponíveis\n5 - Voltar para o menu inicial\n0 - Sair\nResposta: '))

                            if opcao == 0:
                                break

                            if opcao == 1:
                                cadastrar_livro(db)

                            elif opcao == 2:
                                criar_emprestimo(db)

                            elif opcao == 3:
                                ver_emprestimos_ativos(db)
                            
                            elif opcao == 4:
                                ver_livros_disponiveis(db)

                            elif opcao == 5:
                                break

                            if opcao in [1, 2, 3, 4]:
                                opcao = int(input('\n1 - Voltar\n0 - Sair\nResposta: '))

                                if opcao == 1:
                                    voltar = True
                                else:
                                    break
                elif opcao == 3:
                    continue
                else:
                    print('Selecione uma opção válida')
                

            elif opcao == 2:
                print('Cadastrar como:\n')
                opcao = int(input('1 - Usuário\n2 - Funcionário\n3 - Voltar\nResposta: '))

                if opcao == 1:
                    cadastrar_usuario(db)
                elif opcao == 2:
                    cadastrar_funcionario(db)
                elif opcao == 3:
                    continue
                else:
                    print('Selecione uma opção válida')
            else:
                print('Selecione uma opção válida')

    finally:
        db.fechar()

if __name__ == '__main__':
    menu()
