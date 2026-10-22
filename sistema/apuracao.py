import pymysql


def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


def apurar_votos():
    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT
                    c.numero,
                    c.nome,
                    c.partido,
                    COUNT(v.id) AS total_votos
                FROM candidatos c
                LEFT JOIN votos v
                    ON c.id = v.candidato_id
                GROUP BY
                    c.id,
                    c.numero,
                    c.nome,
                    c.partido
                ORDER BY c.numero
            """)

            resultados = cursor.fetchall()

        print("\n===== APURAÇÃO DOS VOTOS =====")

        total_geral = 0
        for numero, nome, partido, votos in resultados:
            total_geral += votos

        # Lista todos os candidatos com seus votos e porcentagem
        for numero, nome, partido, votos in resultados:
            if total_geral > 0:
                percentual = (votos / total_geral) * 100
            else:
                percentual = 0

            print(f"\nNúmero: {numero}")
            print(f"Candidato: {nome}")
            print(f"Partido: {partido or 'Não informado'}")
            print(f"Total de votos: {votos} ({percentual:.1f}%)")

        print("\n------------------------------")
        print(f"Total geral de votos: {total_geral}")

        # ===== DESTAQUE DO VENCEDOR =====
        if total_geral == 0:
            print("\n⚠️  Não houve votos registrados. Não há vencedor.")
            return

        # Descobre o maior número de votos
        mais_votados = max(votos for _, _, _, votos in resultados)

        # Pega todos os candidatos que têm esse número de votos (empate)
        vencedores = [
            (numero, nome, partido, votos)
            for numero, nome, partido, votos in resultados
            if votos == mais_votados
        ]

        print("\n===== RESULTADO =====")

        if len(vencedores) == 1:
            numero, nome, partido, votos = vencedores[0]
            percentual = (votos / total_geral) * 100

            print("🏆 VENCEDOR:")
            print(f"   Número: {numero}")
            print(f"   Nome: {nome}")
            print(f"   Partido: {partido or 'Não informado'}")
            print(f"   Votos: {votos} ({percentual:.1f}%)")

        else:
            print("🤝 EMPATE entre:")
            for numero, nome, partido, votos in vencedores:
                percentual = (votos / total_geral) * 100
                print(f"   - {nome} (número {numero}) — {votos} votos ({percentual:.1f}%)")

    except pymysql.MySQLError as erro:
        print("Erro ao consultar os votos:", erro)

    finally:
        conexao.close()


if __name__ == "__main__":
    apurar_votos()