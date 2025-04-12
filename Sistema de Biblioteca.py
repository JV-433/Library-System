import datetime  

# Dados iniciais
livros = []  
usuarios = []  
emprestimos = []  

# CADASTRO E CONSULTA  
def cadastrar_livro():  
    print("\n--- CADASTRO DE LIVRO ---")  
    while True:  
        titulo = input("Título do livro: ").strip()  
        if not titulo:  
            print("Erro: Título não pode ser vazio.")  
            continue  

        autor = input("Autor: ").strip()  
        isbn = input("ISBN (13 dígitos): ").strip()  
        if len(isbn) != 13 or not isbn.isdigit():  
            print("Erro: ISBN inválido. Deve ter 13 dígitos.")  
            continue  

        livros.append({  
            "id": len(livros) + 1,  
            "titulo": titulo,  
            "autor": autor,  
            "isbn": isbn,  
            "disponivel": True  
        })  
        print(f"Livro '{titulo}' cadastrado com sucesso! (ID: {len(livros)})")  
        break  

def listar_livros():  
    print("\n--- LIVROS CADASTRADOS ---")  
    if not livros:  
        print("Nenhum livro cadastrado.")  
        return  

    for livro in livros:  
        status = "Disponível" if livro["disponivel"] else "Emprestado"  
        print(f"ID: {livro['id']} | {livro['titulo']} ({livro['autor']}) - ISBN: {livro['isbn']} | {status}")  

def buscar_livro():  
    print("\n--- BUSCAR LIVRO ---")  
    termo = input("Digite título, autor ou ISBN: ").lower()  
    resultados = []  

    for livro in livros:  
        if (termo in livro["titulo"].lower() or  
            termo in livro["autor"].lower() or  
            termo in livro["isbn"]):  
            resultados.append(livro)  

    if not resultados:  
        print("Nenhum livro encontrado.")  
    else:  
        for livro in resultados:  
            status = "Disponível" if livro["disponivel"] else "Emprestado"  
            print(f"ID: {livro['id']} | {livro['titulo']} - {status}")  

# EMPRÉSTIMOS E RELATÓRIOS  
def emprestar_livro():  
    print("\n--- EMPRÉSTIMO DE LIVRO ---")  
    if not livros:  
        print("Erro: Nenhum livro cadastrado.")  
        return  

    listar_livros()  
    livro_id = int(input("ID do livro a emprestar: "))  
    usuario = input("Nome do usuário: ").strip()  

    livro = next((livro for livro in livros if livro["id"] == livro_id), None)  
    if not livro:  
        print("Erro: Livro não encontrado.")  
        return  
    if not livro["disponivel"]:  
        print("Erro: Livro já emprestado.")  
        return  

    data_emprestimo = datetime.date.today()  
    data_devolucao = data_emprestimo + datetime.timedelta(days=14)  

    emprestimos.append({  
        "livro_id": livro_id,  
        "usuario": usuario,  
        "data_emprestimo": data_emprestimo,  
        "data_devolucao": data_devolucao,  
        "devolvido": False  
    })  

    livro["disponivel"] = False  
    print(f"Livro '{livro['titulo']}' emprestado para {usuario}. Devolução em {data_devolucao}.")  

def devolver_livro():  
    print("\n--- DEVOLUÇÃO DE LIVRO ---")  
    listar_emprestimos_ativos()  
    livro_id = int(input("ID do livro a devolver: "))  

    emprestimo = next((e for e in emprestimos if e["livro_id"] == livro_id and not e["devolvido"]), None)  
    if not emprestimo:  
        print("Erro: Empréstimo não encontrado ou já devolvido.")  
        return  

    livro = next((livro for livro in livros if livro["id"] == livro_id), None)  
    livro["disponivel"] = True  
    emprestimo["devolvido"] = True  

    # Verificar atraso  
    hoje = datetime.date.today()  
    if hoje > emprestimo["data_devolucao"]:  
        dias_atraso = (hoje - emprestimo["data_devolucao"]).days  
        multa = dias_atraso * 2.50  
        print(f"Livro devolvido com {dias_atraso} dias de atraso! Multa: R${multa:.2f}")  
    else:  
        print("Livro devolvido no prazo!")  

def listar_emprestimos_ativos():  
    print("\n--- EMPRÉSTIMOS ATIVOS ---")  
    ativos = [e for e in emprestimos if not e["devolvido"]]  
    if not ativos:  
        print("Nenhum empréstimo ativo.")  
        return  

    for emp in ativos:  
        livro = next((livro for livro in livros if livro["id"] == emp["livro_id"]), None)  
        print(f"Livro: {livro['titulo']} | Usuário: {emp['usuario']} | Devolução: {emp['data_devolucao']}")  

# MENU PRINCIPAL  
def main():  
    while True:  
        print("\n=== SISTEMA DE BIBLIOTECA ===")  
        print("1. Cadastrar livro")  
        print("2. Listar livros")  
        print("3. Buscar livro")  
        print("4. Emprestar livro")  
        print("5. Devolver livro")  
        print("6. Empréstimos ativos")  
        print("0. Sair")  

        opcao = input("Escolha uma opção: ")  

        if opcao == "1":  
            cadastrar_livro()  
        elif opcao == "2":  
            listar_livros()  
        elif opcao == "3":  
            buscar_livro()  
        elif opcao == "4":  
            emprestar_livro()  
        elif opcao == "5":  
            devolver_livro()  
        elif opcao == "6":  
            listar_emprestimos_ativos()  
        elif opcao == "0":  
            print("Saindo do sistema...")  
            break  
        else:  
            print("Opção inválida!")  

if __name__ == "__main__":  
    main()  