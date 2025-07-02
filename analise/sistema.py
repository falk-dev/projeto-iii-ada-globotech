import csv

from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo

from estruturas_dados.algoritmos_ordenacao import quick_sort 


class SistemaAnaliseEngajamento:
    def __init__(self):
        self._fila_interacoes_brutas: Fila = Fila()
        self._arvore_conteudos: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._arvore_usuarios: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._plataformas_registradas: dict[str, Plataforma] = {}

    # -------- Métodos da árvore de conteúdos --------
    def inserir_conteudo(self, conteudo: Conteudo) -> None:
        self._arvore_conteudos.inserir_elemento(conteudo.id_conteudo, conteudo)

    def buscar_conteudo(self, id_conteudo: int) -> Conteudo | None:
        return self._arvore_conteudos.buscar_elemento(id_conteudo)

    def remover_conteudo(self, id_conteudo: int) -> None:
        self._arvore_conteudos.remover_elemento(id_conteudo)

    def percurso_em_ordem(self) -> list:
        return self._arvore_conteudos.percurso_in_order()

    # -------- Métodos de processamento do arquivo csv --------
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
        
    def gerar_relatorio_atividade_usuarios(self, top_n: int = None):
    
        """
    Gera um relatório dos usuários mais ativos com base no tempo total de consumo (em segundos).

    Args:
        top_n (int, opcional): Número de usuários mais ativos a exibir. Se None, exibe todos.

    Complexidade:
        - Percurso da árvore: O(n)
        - Cálculo de tempo total: O(n)
        - Ordenação (Quick Sort): O(n log n) em média
        - Total: O(n log n)

    Retorna:
        None. Apenas imprime o relatório no console.
        """ 
        # Passo 1: Obter todos os usuários da árvore em ordem
        usuarios = self._arvore_usuarios.percurso_em_ordem()

        # Passo 2: Criar lista de tuplas (usuario, tempo_total_consumo)
        usuarios_consumo = []
        for usuario in usuarios:
            tempo_total = sum(
                interacao.watch_duration_seconds
                for interacao in usuario._Usuario__interacoes_realizadas
            )
            usuarios_consumo.append((usuario, tempo_total))

        # Passo 3: Ordenar a lista com base no tempo total de consumo (decrescente)
        quick_sort(usuarios_consumo, key=lambda x: x[1])

        # Passo 4: Reverter para ordem decrescente (Quick Sort faz crescente por padrão)
        usuarios_consumo.reverse()

        # Passo 5: Limitar ao top_n se for informado
        if top_n is not None:
            usuarios_consumo = usuarios_consumo[:top_n]

        # Passo 6: Exibir o relatório
        print("\n--- Relatório: Usuários com Maior Tempo Total de Consumo ---")
        for usuario, tempo in usuarios_consumo:
            print(f"Usuário ID {usuario.id_usuario} - Tempo Total: {tempo} segundos")