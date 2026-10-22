import pymysql

try:
    conexao = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="mysql"
    )

    print("Conexão com o MariaDB realizada com sucesso!")

    conexao.close()

except Exception as erro:
    print("Não foi possível conectar ao banco.")
    print("Erro:", erro)
