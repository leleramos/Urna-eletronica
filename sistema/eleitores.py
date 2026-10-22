import pymysql


def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


def cadastrar_eleitor():
    titulo = input("Digite o título de eleitor (12 dígitos): ").strip()

    if not titulo:
        print("O título não pode ficar vazio.")
        return

    if not titulo.isdigit():
        print("Título inválido. Digite apenas números.")
        return

    if len(titulo) != 12:
        print("Título inválido. O título deve ter exatamente 12 dígitos.")
        return

    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO eleitores (identificacao)
                VALUES (%s)
                """,
                (titulo,)
            )

        conexao.commit()
        print("Eleitor cadastrado com sucesso!")

    except pymysql.err.IntegrityError:
        conexao.rollback()
        print("Esse título de eleitor já está cadastrado.")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print("Erro ao cadastrar eleitor:", erro)

    finally:
        conexao.close()


if __name__ == "__main__":
    cadastrar_eleitor()