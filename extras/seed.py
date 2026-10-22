import pymysql


def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


# Candidatos fictícios — você pode trocar os nomes se quiser
CANDIDATOS_EXEMPLO = [
    (10, "Ana Silva", "Partido A"),
    (13, "Bruno Costa", "Partido B"),
    (22, "Carla Mendes", "Partido C"),
    (45, "Diego Rocha", "Partido D"),
    (77, "Elisa Prado", "Partido E"),
]


def carregar_candidatos_exemplo():
    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            inseridos = 0
            ignorados = 0

            for numero, nome, partido in CANDIDATOS_EXEMPLO:
                try:
                    cursor.execute(
                        """
                        INSERT INTO candidatos (numero, nome, partido)
                        VALUES (%s, %s, %s)
                        """,
                        (numero, nome, partido)
                    )
                    inseridos += 1
                except pymysql.err.IntegrityError:
                    ignorados += 1

        conexao.commit()

        print("\n===== CANDIDATOS DE EXEMPLO =====")
        print(f"Inseridos: {inseridos}")
        if ignorados > 0:
            print(f"Ignorados (já existiam com esse número): {ignorados}")

        if inseridos == 0:
            print("\nOs candidatos de exemplo já estavam todos cadastrados.")
        else:
            print("\nCandidatos de exemplo carregados com sucesso!")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print("Erro ao carregar candidatos de exemplo:", erro)

    finally:
        conexao.close()