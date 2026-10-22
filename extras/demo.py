import random
import pymysql
from sistema.apuracao import apurar_votos 



def conectar_banco():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="urna_eletronica"
    )


def modo_demonstracao():
    try:
        conexao = conectar_banco()
    except pymysql.MySQLError as erro:
        print("Erro ao conectar com o banco:", erro)
        return

    try:
        with conexao.cursor() as cursor:
            # 1. Verifica se já existem votos
            cursor.execute("SELECT COUNT(*) FROM votos")
            votos_existentes = cursor.fetchone()[0]

            if votos_existentes > 0:
                print("\n⚠️  Já existem votos registrados no sistema.")
                print(f"Total atual de votos: {votos_existentes}")
                print("\nPara rodar o modo demonstração limpo, apague os votos antes.")
                print("Use o script 'limpar_dados.py' ou rode no banco:")
                print("   DELETE FROM votos;")
                print("   DELETE FROM eleitores;")
                return

            # 2. Verifica se há candidatos
            cursor.execute("SELECT id, numero, nome FROM candidatos ORDER BY numero")
            candidatos = cursor.fetchall()

            if not candidatos:
                print("\n⚠️  Não há candidatos cadastrados.")
                print("Use a opção 6 (Carregar candidatos de exemplo) primeiro.")
                return

            # 3. Confirma com o usuário
            print("\n===== MODO DEMONSTRAÇÃO =====")
            print(f"Isso vai registrar 10 eleitores fictícios e 10 votos.")
            print(f"Candidatos disponíveis: {len(candidatos)}")
            confirmar = input("Continuar? (s/n): ").strip().lower()

            if confirmar != "s":
                print("Modo demonstração cancelado.")
                return

            # 4. Roda as 10 iterações
            print("\nRegistrando 10 votações...\n")

            for i in range(1, 11):
                # Título fictício único de 12 dígitos (prefixo 9)
                titulo = f"9{i:011d}"

                # Insere o eleitor
                cursor.execute(
                    """
                    INSERT INTO eleitores (identificacao)
                    VALUES (%s)
                    """,
                    (titulo,)
                )
                eleitor_id = cursor.lastrowid

                # Escolhe um candidato aleatório
                candidato_escolhido = random.choice(candidatos)
                candidato_id, numero, nome = candidato_escolhido

                # Registra o voto
                cursor.execute(
                    """
                    INSERT INTO votos (eleitor_id, candidato_id)
                    VALUES (%s, %s)
                    """,
                    (eleitor_id, candidato_id)
                )

                # Marca como votou
                cursor.execute(
                    """
                    UPDATE eleitores
                    SET votou = TRUE
                    WHERE id = %s
                    """,
                    (eleitor_id,)
                )

                print(f"  Voto {i:2d}/10 → {nome} (número {numero})")

            conexao.commit()
            print("\n✅ Modo demonstração concluído: 10 votações registradas.")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print("Erro no modo demonstração:", erro)
        return

    finally:
        conexao.close()

    # 5. Pergunta se quer ver a apuração (fora do cursor, para liberar conexão)
    ver = input("\nDeseja ver a apuração agora? (s/n): ").strip().lower()
    if ver == "s":
        apurar_votos()


if __name__ == "__main__":
    modo_demonstracao()