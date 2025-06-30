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

                for linha in leitor_csv:
                    self._fila_interacoes_brutas.enfileirar(linha)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV '{caminho_arquivo}': {e}")
            return None

    def processar_interacoes_da_fila(self) -> None:
        interacao_atual = self._fila_interacoes_brutas.desenfileirar()

        """
        Para cada linha desenfileirada:
            - Obtém/Cria o objeto Plataforma (pode continuar usando o dicionário existente).
            - Obtém/Cria o objeto Conteudo (utilizando buscar_conteudo e inserir_conteudo da sua _arvore_conteudos).
            - Obtém/Cria o objeto Usuario (utilizando buscar_usuario e inserir_usuario da sua _arvore_usuarios).
            - Tenta instanciar Interacao, lidando com validações.
            - Se Interacao válida, registra-a nos objetos Conteudo e Usuario correspondentes.
        """
