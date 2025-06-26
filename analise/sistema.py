import csv

from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca
from entidades.plataforma import Plataforma


class SistemaAnaliseEngajamento:
    def __init__(self):
        self._fila_interacoes_brutas: Fila = Fila()
        self._arvore_conteudos: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._arvore_usuarios: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._plataformas_registradas: dict[str, Plataforma] = {}

    def processar_interacoes_csv(self, caminho_arquivo: str) -> None:
        self._carregar_interacoes_csv(caminho_arquivo)

    def _carregar_interacoes_csv(self, caminho_arquivo: str) -> None:
        try:
            with open(caminho_arquivo, mode="r", encoding="utf-8") as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv)
                cabecalho = next(leitor_csv)

                for linha in leitor_csv:
                    self._fila_interacoes_brutas.enfileirar(linha)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV '{caminho_arquivo}': {e}")
            return None
