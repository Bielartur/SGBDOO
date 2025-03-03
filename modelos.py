from persistent import Persistent
from datetime import datetime, timedelta

class Pessoa(Persistent):
    def __init__(self, id, nome, cpf, email):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email

class Usuario(Pessoa):
    def __init__(self, id, nome, cpf, email, numero_cartao):
        super().__init__(id, nome, cpf, email)
        self.numero_cartao = numero_cartao
        self.ativo = True

class Funcionario(Pessoa):
    def __init__(self, id, nome, cpf, email, matricula, cargo):
        super().__init__(id, nome, cpf, email)
        self.matricula = matricula
        self.cargo = cargo

class Livro(Persistent):
    def __init__(self, id, titulo, autor, isbn):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = True

class Emprestimo(Persistent):
    def __init__(self, id, usuario: Usuario, livro: Livro):
        self.id = id
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = datetime.now()
        self.data_devolucao = datetime.now() + timedelta(days=14)
        self.devolvido = False
        self.livro.disponivel = False
        self._p_changed = True  # Notifica ZODB da mudança no objeto

    def devolver(self):
        self.devolvido = True
        self.livro.disponivel = True
        self._p_changed = True  # Notifica ZODB da mudança no objeto