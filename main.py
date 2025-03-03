from modelos import Usuario, Funcionario, Livro, Emprestimo
from biblioteca_db import BibliotecaDB

def main():
    # Inicializa o banco de dados
    db = BibliotecaDB()

    try:
        # Criar e salvar um usuário
        usuario = Usuario(1, "João Silva", "123.456.789-00", "joao@email.com", "U001")
        db.salvar_usuario(usuario)

        # Criar e salvar um funcionário
        funcionario = Funcionario(2, "Maria Santos", "987.654.321-00", 
                                "maria@biblioteca.com", "F001", "Bibliotecária")
        db.salvar_funcionario(funcionario)

        # Criar e salvar um livro
        livro = Livro(1, "O Senhor dos Anéis", "J.R.R. Tolkien", "978-8533613379")
        db.salvar_livro(livro)
        livro = Livro(2, "O Senhor dos Anéis - As Duas Torres", "J.R.R. Tolkien", "978-8845292255")
        db.salvar_livro(livro)

        # Criar e salvar um empréstimo
        emprestimo = Emprestimo(1, usuario, livro)
        db.salvar_emprestimo(emprestimo)

        # Buscar e exibir empréstimos ativos
        print("\nEmpréstimos ativos:")
        emprestimos_ativos = db.listar_emprestimos_ativos()
        for emp in emprestimos_ativos:
            print(f"Empréstimo: Usuário={emp.usuario.nome}, Livro={emp.livro.titulo}")

        # Listar livros disponíveis
        print("\nLivros disponíveis:")
        livros_disponiveis = db.listar_livros_disponiveis()
        for livro in livros_disponiveis:
            print(f"Livro: {livro.titulo} - {livro.autor}")

    finally:
        # Fecha a conexão com o banco
        db.fechar()

if __name__ == "__main__":
    main()