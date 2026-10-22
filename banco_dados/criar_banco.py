
import pymysql

conexao = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password=""
)

try:
    with conexao.cursor() as cursor:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS urna_eletronica"
        )

    conexao.commit()
    print("Banco de dados criado com sucesso!")

finally:
    conexao.close()
