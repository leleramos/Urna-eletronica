
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eleitores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                identificacao VARCHAR(30) NOT NULL UNIQUE,
                votou BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidatos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numero INT NOT NULL UNIQUE,
                nome VARCHAR(100) NOT NULL,
                partido VARCHAR(50)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                eleitor_id INT NOT NULL UNIQUE,
                candidato_id INT NOT NULL,
                data_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (eleitor_id)
                    REFERENCES eleitores(id),

                FOREIGN KEY (candidato_id)
                    REFERENCES candidatos(id)
            )
        """)

    conexao.commit()
    print("Tabelas criadas com sucesso!")

finally:
    conexao.close()
