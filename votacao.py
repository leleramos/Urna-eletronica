import pymysql


def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


def votar():
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
            # Busca o eleitor
            cursor.execute(
                """
                SELECT id, votou
                FROM eleitores
                WHERE identificacao = %s
                """,
                (titulo,)
            )

            eleitor = cursor.fetchone()

            if eleitor is None:
                print("Eleitor não cadastrado.")
                return

            eleitor_id, ja_votou = eleitor

            if ja_votou:
                print("Este eleitor já votou!")
                return

            # Mostra os candidatos
            cursor.execute(
                """
                SELECT id, numero, nome, partido
                FROM candidatos
                ORDER BY numero
                """
            )

            candidatos = cursor.fetchall()

            if not candidatos:
                print("Não existem candidatos cadastrados.")
                return

            print("\n===== CANDIDATOS =====")

            for candidato in candidatos:
                candidato_id, numero, nome, partido = candidato
                print(
                    f"Número: {numero} | "
                    f"Nome: {nome} | "
                    f"Partido: {partido or 'Não informado'}"
                )

            numero_escolhido = input(
                "\nDigite o número do candidato: "
            ).strip()

            # Confere se o candidato existe
            cursor.execute(
                """
                SELECT id
                FROM candidatos
                WHERE numero = %s
                """,
                (numero_escolhido,)
            )

            candidato = cursor.fetchone()

            if candidato is None:
                print("Número de candidato inválido.")
                return

            candidato_id = candidato[0]

            # Registra o voto
            cursor.execute(
                """
                INSERT INTO votos (eleitor_id, candidato_id)
                VALUES (%s, %s)
                """,
                (eleitor_id, candidato_id)
            )

            # Marca o eleitor como alguém que já votou
            cursor.execute(
                """
                UPDATE eleitores
                SET votou = TRUE
                WHERE id = %s
                """,
                (eleitor_id,)
            )

        conexao.commit()
        print("Voto registrado com sucesso!")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print("Não foi possível registrar o voto:", erro)

    finally:
        conexao.close()


if __name__ == "__main__":
    votar()