import os
from analise.sistema import SistemaAnaliseEngajamento

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("📊 Análise de Engajamento Globotech")
    print("="*35)
    print("1️⃣  Carregar interações do CSV")
    print("2️⃣  Processar interações")
    print("3️⃣  Relatório: usuários mais ativos")
    print("4️⃣  Relatório: conteúdos mais engajados")
    print("5️⃣  Relatório: comentários por conteúdo")
    print("6️⃣  Sair 🚪")
    print("="*35)

def main():
    sistema = SistemaAnaliseEngajamento()
    caminho_csv = ""

    while True:
        limpar_tela()
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            caminho_csv = input("🗂️  Informe o caminho do arquivo CSV: ")
            sistema.processar_interacoes_csv(caminho_csv)
            input("✅ Dados carregados! Pressione Enter para continuar...")

        elif opcao == "2":
            sistema.processar_interacoes_da_fila()
            input("🔄 Processamento concluído! Pressione Enter para continuar...")

        elif opcao == "3":
            n = input("Quantos usuários mostrar? (Deixe vazio para todos): ")
            if n.isdigit():
                sistema.gerar_relatorio_atividade_usuarios(top_n=int(n))
            else:
                sistema.gerar_relatorio_atividade_usuarios()
            input("Pressione Enter para continuar...")

        elif opcao == "4":
            print("📈 [Relatório de conteúdos mais engajados ainda não implementado]")
            sistema.relatorio_conteudos_mais_engajados()
            input("⬆️ Pressione Enter para continuar...")

        elif opcao == "5":
            print("💬 [Relatório de comentários por conteúdo ainda não implementado]")
            sistema.relatorio_comentarios_por_conteudo()
            input("⬆️ Pressione Enter para continuar...")

        elif opcao == "6":
            print("👋 Até a próxima!")
            break

        else:
            input("❗ Opção inválida! Pressione Enter para tentar novamente...")

if __name__ == "__main__":
    main()
