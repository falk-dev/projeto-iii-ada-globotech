import csv

from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreConteudos, ArvoreUsuarios
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo
from estruturas_dados.algoritmos_ordenacao import quick_sort, insertion_sort


class SistemaAnaliseEngajamento:
    def __init__(self):
        self._fila_interacoes_brutas: Fila = Fila()
        self._arvore_conteudos: ArvoreConteudos = ArvoreConteudos()
        self._arvore_usuarios: ArvoreUsuarios = ArvoreUsuarios()
        self._plataformas_registradas: dict[str, Plataforma] = {}

    def processar_interacoes_csv(self, caminho_arquivo: str) -> None:
        self._carregar_interacoes_csv(caminho_arquivo)

    def _carregar_interacoes_csv(self, caminho_arquivo: str):
        try:
            with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo_csv:
                leitor_csv = csv.DictReader(arquivo_csv)
                for linha in leitor_csv:
                    self._fila_interacoes_brutas.enfileirar(linha)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV '{caminho_arquivo}': {e}")
            return None

    def processar_interacoes_da_fila(self) -> None:
        while not self._fila_interacoes_brutas.esta_vazia():
            interacao = self._fila_interacoes_brutas.desenfileirar()
            id_conteudo = int(interacao.get("id_conteudo", 0))
            nome_conteudo = interacao.get("nome_conteudo", "")
            conteudo = Conteudo(id_conteudo, nome_conteudo)

            if self._arvore_conteudos.buscar_conteudo(id_conteudo) is None:
                self._arvore_conteudos.inserir_conteudo(conteudo)

            # TODO: implementar processamento completo com Usuario, Plataforma, Interacao

    def _selecionar_top_n(self, itens: list, metric_func, n: int | None = None, algoritmo: str = "quick"):
        if algoritmo == "quick":
            quick_sort(itens, key=metric_func)
        elif algoritmo == "insertion":
            insertion_sort(itens, key=metric_func)
        else:
            raise ValueError("Algoritmo não suportado")
        itens.reverse()
        return itens if n is None else itens[:n]

    def gerar_relatorio_atividade_usuarios(self, top_n: int = None):
        usuarios = self._arvore_usuarios.percurso_em_ordem()
        usuarios_consumo = []
        for usuario in usuarios:
            tempo_total = sum(
                interacao.watch_duration_seconds
                for interacao in usuario._Usuario__interacoes_realizadas
            )
            usuarios_consumo.append((usuario, tempo_total))

        usuarios_consumo = self._selecionar_top_n(
            itens=usuarios_consumo,
            metric_func=lambda x: x[1],
            n=top_n,
            algoritmo="quick"
        )

        print("\n--- Relatório: Usuários com Maior Tempo Total de Consumo ---")
        for usuario, tempo in usuarios_consumo:
            print(f"Usuário ID {usuario.id_usuario} - Tempo Total: {tempo} segundos")
