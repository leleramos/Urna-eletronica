from cadastrar_candidatos import (
    cadastrar_candidato,
    listar_candidatos
)
from eleitores import cadastrar_eleitor
from votacao import votar
from apuracao import apurar_votos
from seed import carregar_candidatos_exemplo
from demo import modo_demonstracao


def menu():
    while True:
        print("\n===== URNA ELETRÔNICA =====")
        print("1 - Cadastrar candidato")
        print("2 - Listar candidatos")
        print("3 - Cadastrar eleitor")
        print("4 - Votar")
        print("5 - Apurar votos")
        print("6 - Carregar candidatos de exemplo")
        print("7 - Modo demonstração (10 votos automáticos)")
        print("8 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_candidato()

        elif opcao == "2":
            listar_candidatos()

        elif opcao == "3":
            cadastrar_eleitor()

        elif opcao == "4":
            votar()

        elif opcao == "5":
            apurar_votos()

        elif opcao == "6":
            carregar_candidatos_exemplo()

        elif opcao == "7":
            modo_demonstracao()

        elif opcao == "8":
            print("Encerrando a urna. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()