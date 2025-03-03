from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction

class BibliotecaDB:
    def __init__(self):
        self.storage = FileStorage.FileStorage('biblioteca.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        
        # Inicializa as "tabelas" se não existirem
        if not hasattr(self.root, 'usuarios'):
            self.root.usuarios = OOBTree()
        if not hasattr(self.root, 'funcionarios'):
            self.root.funcionarios = OOBTree()
        if not hasattr(self.root, 'livros'):
            self.root.livros = OOBTree()
        if not hasattr(self.root, 'emprestimos'):
            self.root.emprestimos = OOBTree()
        transaction.commit()

    def fechar(self):
        self.connection.close()
        self.db.close()
        self.storage.close()

    # Métodos para Usuario
    def salvar_usuario(self, usuario):
        self.root.usuarios[usuario.id] = usuario
        transaction.commit()

    def buscar_usuario(self, id):
        return self.root.usuarios.get(id)
    
    def buscar_usuario_por_cartao(self, numero_cartao):
        for usuario in self.root.usuarios.values():  # Percorre todos os usuários
            if usuario.numero_cartao == numero_cartao:
                return usuario
        return None  # Retorna None se não encontrar

    def listar_usuarios(self):
        return list(self.root.usuarios.values())

    # Métodos para Funcionario
    def salvar_funcionario(self, funcionario):
        self.root.funcionarios[funcionario.id] = funcionario
        transaction.commit()

    def buscar_funcionario(self, id):
        return self.root.funcionarios.get(id)

    def buscar_funcionario_por_matricula(self, matricula):
        for func in self.root.funcionarios.values():
            if func.matricula == matricula:
                return func
        return None
    
    def listar_funcionarios(self):
        return list(self.root.funcionarios.values())

    # Métodos para Livro
    def salvar_livro(self, livro):
        self.root.livros[livro.id] = livro
        transaction.commit()

    def buscar_livro(self, id):
        return self.root.livros.get(id)

    def buscar_livro_por_isbn(self, isbn):
        for livro in self.root.livros.values():
            if livro.isbn == isbn:
                return livro
        return None

    def listar_livros_disponiveis(self):
        return [livro for livro in self.root.livros.values() if livro.disponivel]
    
    def listar_livros_existentes(self):
        return list(self.root.livros.values())

    # Métodos para Emprestimo
    def salvar_emprestimo(self, emprestimo):
        self.root.emprestimos[emprestimo.id] = emprestimo
        transaction.commit()

    def buscar_emprestimo(self, id):
        return self.root.emprestimos.get(id)

    def listar_emprestimos_ativos(self):
        return [emp for emp in self.root.emprestimos.values() if not emp.devolvido]
    
    def listar_emprestimos_existentes(self):
        return list(self.root.emprestimos.values())
