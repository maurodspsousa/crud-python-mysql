import MySQLdb

def conectar():
    try:
        conn = MySQLdb.connect(
            db='pmysql',
            host='localhost',
            user='pmsqlteste',
            passwd='teste'
        )
        return conn
    except MySQLdb.Error as e:
        print(f'Erro ao fazer a conexão ao MySQL Server: {e}')


def desconectar(conn):
    if conn:
        conn.close()
    print('Desconectando do Servidor')

def checagem(produtos):
    if len(produtos) > 0:
            print('Produtos: ')
            for produto in produtos:
                print('--------------------')
                print(f'ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Estoque: {produto[3]}, Tipo: {produto[4]}')
            print('Deseja voltar ao menu? 1 - Sim, 2 - Não')
            opc = input('Opção: ')
            if opc == 1:
                menu()
            else:
                print('Até mais!')
                exit()
    else:
        print("Sem produtos cadastrados")
        menu()

def listar():
    conn = conectar()
    cursor = conn.cursor()
    print('Deseja listar:')
    print('1 - Todos os produtos ')
    print('2 - Tipo de produto')
    print('3 - Produto especifico \n')
    opc = int(input('Opção: '))

    if opc == 1:
        cursor.execute('SELECT p.id, p.nome, p.preco, p.estoque, tp.nome FROM produtos AS p, tipo_produto AS tp WHERE p.id_tipo_produto = tp.id')
        produtos = cursor.fetchall()
        checagem(produtos)
    elif opc == 2:
        tipo = input('Qual tipo de produto? \n')
        cursor.execute(f"SELECT p.id, p.nome, p.preco, p.estoque, tp.nome FROM produtos AS p, tipo_produto AS tp WHERE p.id_tipo_produto = tp.id AND tp.nome = '{tipo}'")
        produtos = cursor.fetchall()
        checagem(produtos)
    elif opc == 3:
        nome = input('Qual o nome do produto? \n')
        cursor.execute(f"SELECT * FROM produtos WHERE nome = '{nome}'")
        produtos = cursor.fetchall()
        checagem(produtos)
    else:
        print('Opção inválida')
    desconectar(conn)
    menu()


def adicionar():
    conn = conectar()
    cursor = conn.cursor()
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço do produto: '))
    estoque = int(input('Informe a quantidade em Estoque: '))
    id = int(input('Qual o tipo de produto? 1 - Computador, 2 - Videogame, 3 - Teste: '))
    cursor.execute(f"INSERT INTO produtos (nome, preco, estoque, id_tipo_produto) VALUES ('{nome}',{preco},{estoque},{id})")
    conn.commit()

    if cursor.rowcount == 1:
        print(f'Produto: {nome} foi inserido com sucesso')
    else:
        print('Erro ao inserir produto')
    
    desconectar(conn)
    menu()


def atualizar():
    conn = conectar()
    cursor = conn.cursor()
    id = int(input('Informe o id do produto que deseja atualizar: '))
    nome = input('Informe o novo nome do produto: ')
    preco = float(input('Informe o novo preço do produto: '))
    estoque = int(input('Informe a nova quantidade em estoque: '))
    cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco}, estoque={estoque} WHERE id={id}")
    conn.commit()

    if cursor.rowcount == 1:
        print('Produto atualizado com sucesso \n\n')
    else:
        print('Erro ao atualizar produto \n\n')
    desconectar(conn)

    menu()


def deletar():
    conn = conectar()
    cursor = conn.cursor()
    id = int(input('Informe o ID do Produto a ser deletado: '))
    cursor.execute(f'SELECT * FROM produtos WHERE id = {id}')
    produtos = cursor.fetchall()
    if len(produtos) > 0:
        for produto in produtos:
            print(f'ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Estoque: {produto[3]} ')
            opc = input('Deletar este produto? s/n')
        if opc.lower() == 's':
            cursor.execute(f'DELETE FROM produtos WHERE id = {id}')
            conn.commit()
            print('Produto deletado com sucesso')
        elif opc.lower() == 'n':
            print('Voltando...')
            deletar()
        else:
            print('Opção inválida')
            deletar()
            
    desconectar(conn)
    menu()

def menu():
    print('----------------------------------')
    print('---- Gerenciamento de Estoque ----')
    print('Escolha uma das opções: ')
    print('1 - Listar Produtos: ')
    print('2 - Adicionar um produto: ')
    print('3 - Atualizar um produto: ')
    print('4 - Excluir um produto: ')
    print('5 - Encerrar \n')
    opcao = int(input('Opção: '))
    print('-----------------------------------')
    if opcao == 1:
        listar()
    elif opcao == 2:
        adicionar()
    elif opcao == 3:
        atualizar()
    elif opcao == 4:
        deletar()
    elif opcao == 5:
        exit()
    else:
        print('Opção incorreta, por favor escolha uma opção disponível')
    