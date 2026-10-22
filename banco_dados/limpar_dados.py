import pymysql

conexao = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="urna_eletronica"
)

try:
    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM votos")
        cursor.execute("DELETE FROM eleitores")

    conexao.commit()
    print("Votos e eleitores apagados. Candidatos mantidos.")

finally:
    conexao.close()