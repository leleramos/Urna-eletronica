import pymysql


def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


def cadastrar_candidato():
    try:
        numero = int(input("Digite o número do candidato: "))
    except ValueError:
        print("Número inválido. Digite apenas dígitos.")
        return

    nome = input("Digite o nome do candidato: ").strip()
    partido = input("Digite o partido do candidato: ").strip()

    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            sql = """
                INSERT INTO candidatos (numero, nome, partido)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (numero, nome, partido))

        conexao.commit()
        print("Candidato cadastrado com sucesso!")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print("Erro ao cadastrar candidato:", erro)

    finally:
        conexao.close()


def listar_candidatos():
    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT numero, nome, partido
                FROM candidatos
                ORDER BY numero
            """)
            candidatos = cursor.fetchall()

        print("\n===== CANDIDATOS CADASTRADOS =====")
        if not candidatos:
            print("Nenhum candidato cadastrado.")
        else:
            for numero, nome, partido in candidatos:
                print(f"Número: {numero}")
                print(f"Nome: {nome}")
                print(f"Partido: {partido or 'Não informado'}")
                print("-" * 30)

    except pymysql.MySQLError as erro:
        print("Erro ao listar candidatos:", erro)

    finally:
        conexao.close()