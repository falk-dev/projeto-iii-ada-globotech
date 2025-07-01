import csv

from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreConteudos, ArvoreUsuarios
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo


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
                # Transformando a linha de interação em um dicionário
                # Nova estrutura da linha:
                # 'id_conteudo': 1, 'nome_conteudo': 'Jornal Nacional' ... etc.
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
        # Executa o loop abaixo enquanto a fila de interações não estiver vazia
        # A cada execução do loop será realizado operações nas classes Plataforma, Conteudo, Usuario e Interacao
        while not self._fila_interacoes_brutas.esta_vazia():
            # Armazenando em uma variável cada interação desenfileirada
            interacao = self._fila_interacoes_brutas.desenfileirar()

            # Armazenando o id e nome do conteúdo de cada interação em uma variável
            # Estrura dos get's abaixo:
            # 1º argumento: chave (obrigatório)
            # 2º argumento: valor para caso a chave solicitada não exista na estrutura (opcional)
            id_conteudo = int(interacao.get("id_conteudo", 0))
            nome_conteudo = interacao.get("nome_conteudo", "")
            conteudo = Conteudo(id_conteudo, nome_conteudo)

            # Caso após a busca na árvore não seja encontrado o id_conteudo do conteúdo em questão, será realizada uma inserção na BST.
            if self._arvore_conteudos.buscar_conteudo(id_conteudo) is None:
                self._arvore_conteudos.inserir_conteudo(conteudo)

        """
        Para cada linha desenfileirada:
            - Obtém/Cria o objeto Plataforma (pode continuar usando o dicionário existente).
            - Obtém/Cria o objeto Usuario (utilizando buscar_usuario e inserir_usuario da sua _arvore_usuarios).
            - Tenta instanciar Interacao, lidando com validações.
            - Se Interacao válida, registra-a nos objetos Conteudo e Usuario correspondentes.
        """
