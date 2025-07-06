import csv

from estruturas_dados.fila import Fila
from estruturas_dados.algoritmos_ordenacao import quick_sort 

from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo

from collections import defaultdict


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
            
# Relatorio Analiticos
    def gerar_relatorio_analitico(self):
        """
        Gera relatórios analíticos de engajamento a partir dos dados processados.
        Inclui rankings e estatísticas conforme solicitado no enunciado.
        """
        print("\n===== RELATÓRIOS ANALÍTICOS DE ENGAJAMENTO =====")
        
        # 1. Ranking de conteúdos mais consumidos (por tempo total de consumo)
        """
        Coleta todos os conteúdos da árvore AVL.
        Para cada conteúdo, soma o tempo total assistido (watch_duration_seconds).
        Armazena em uma lista os conteúdos e seus respectivos tempos de consumo.
        Ordena a lista de tuplas por ordem crescente de tempo de consumo.
        """
        conteudos = [value for _, value in self._arvore_conteudos.items()]
        ranking_conteudos = []
        for c in conteudos:
            total = sum(i.watch_duration_seconds for i in c.interacoes_recebidas)
            ranking_conteudos.append((c, total))

        quick_sort(ranking_conteudos, key=lambda x: x[1])
        ranking_conteudos.reverse()
        
        print("\n--- Conteúdos Mais Consumidos (por tempo total) ---")
        for c, tempo in ranking_conteudos[:10]:
            print(f"Conteúdo ID {c.id_conteudo} - Tipo: {type(c).__name__} - Tempo: {formatar_tempo(tempo)}")
        
        # 2. Usuários com maior tempo total de consumo
        """
        Coleta todos os usuários da árvore AVL.
        Para cada usuário, soma o tempo total assistido (watch_duration_seconds) 
        de todas as interações realizadas.
        - Armazena em uma lista os usuários e seus respectivos tempos de consumo.
        - Ordena a lista de tuplas por ordem crescente de tempo de consumo.
        
        """
        usuarios = [value for _, value in self._arvore_usuarios.items()]
        ranking_usuarios = []
        for u in usuarios:
            tempo_total = sum(i.watch_duration_seconds for i in u._Usuario__interacoes_realizadas)
            ranking_usuarios.append((u, tempo_total))

        quick_sort(ranking_usuarios, key=lambda x: x[1])
        ranking_usuarios.reverse()
        
        print("\n--- Usuários com Maior Tempo de Consumo ---")
        for u, tempo in ranking_usuarios[:10]:
            print(f"Usuário ID {u.id_usuario} - Tempo: {formatar_tempo(tempo)}")

        # 3. Plataforma com maior engajamento (like, share, comment)
        """
        Coleta todos os conteúdos da árvore AVL.
        Para cada conteúdo, conta o número de interações de tipo "like", "share" e "comment".
        - Armazena em um dicionário os conteúdos e seus respectivos engajamentos.
        - Ordena o dicionário por ordem crescente de engajamento.
        """
        engajamento = defaultdict(int)
        for conteudo in conteudos:
            for interacao in conteudo.interacoes:
                if interacao.tipo_interacao in ["like", "share", "comment"]:
                    engajamento[conteudo.plataforma.nome_plataforma] += 1
        
        ranking_engajamento = list(engajamento.items())
        quick_sort(ranking_engajamento, key=lambda x: x[1])
        ranking_engajamento.reverse()
        
        print("\n--- Plataforma com Maior Engajamento ---")
        for plataforma, engajamento in ranking_engajamento[:10]:
            print(f"Plataforma {plataforma} - Engajamento: {engajamento}")
        
        # 4. Conteúdo mais comentado
        """
        Coleta todos os conteúdos da árvore AVL.
        Para cada conteúdo, conta o número de interações de tipo "comment".
        - Armazena em uma lista os conteúdos e seus respectivos comentários.
        - Ordena a lista de tuplas por ordem crescente de comentários.
        """
        ranking_comentados = []
        for conteudo in conteudos:
            total_comentarios = sum(1 for interacao in conteudo.interacoes if interacao.tipo_interacao == "comment")
            ranking_comentados.append((conteudo, total_comentarios))

        quick_sort(ranking_comentados, key=lambda x: x[1])
        ranking_comentados.reverse()
        
        print("\n--- Conteúdos Mais Comentados ---")
        for c, comentarios in ranking_comentados[:10]:
            print(f"Conteúdo ID {c.id_conteudo} - Tipo: {type(c).__name__} - Comentarios: {comentarios}")
        
        # 5. Total de interações por tipo de conteúdo
        """
        Coleta todos os conteúdos da árvore AVL.    
        Para cada conteúdo, conta o número de interações.
        - Armazena em um dicionário os conteúdos e seus respectivos interações.
        - Ordena o dicionário por ordem crescente de interações.
        """
        interacoes_por_tipo = defaultdict(int)
        for conteudo in conteudos:
            tipo = type(conteudo).__name__
            interacoes_por_tipo[tipo] += len(conteudo.interacoes)
        
        ranking_interacoes = list(interacoes_por_tipo.items())
        quick_sort(ranking_interacoes, key=lambda x: x[1])
        ranking_interacoes.reverse()
        
        print("\n--- Total de Interações por Tipo de Conteúdo ---")
        for tipo, interacoes in ranking_interacoes:
            print(f"Tipo: {tipo} - Quantidade de Interações: {interacoes}")
        
        # 6. Tempo médio de consumo por plataforma
        """
        Coleta todos os conteúdos da árvore AVL.    
        Para cada conteúdo, soma o tempo de cada interação.
        - Armazena em um dicionário os conteúdos e seus respectivos tempos de interação.
        - Calcula a média de interações por plataforma.
        - Exibe a plataforma com a média de interações mais alta.
        """
        tempo_plataforma = defaultdict(int)
        qtd_plataforma = defaultdict(int)
        for c in conteudos:
            for i in c.interacoes_recebidas:
                tempo_plataforma[i.plataforma_interacao.nome_plataforma] += i.watch_duration_seconds
                qtd_plataforma[i.plataforma_interacao.nome_plataforma] += 1

        print("\n--- Tempo Médio de Consumo por Plataforma ---")
        for plataforma, total in tempo_plataforma.items():
            qtd = qtd_plataforma[plataforma]
            media = total // qtd if qtd > 0 else 0
            print(f"{plataforma} - Média: {formatar_tempo(media)}")

        # 7. Quantidade de comentários por conteúdo
        """
        Coleta todos os conteúdos da árvore AVL.
        Para cada conteúdo, conta o número de interações de tipo "comment". 
        - Armazena em uma lista os conteúdos e seus respectivos comentários.
        - Ordena a lista de tuplas por ordem crescente de comentários.
        """
        print("\n--- Comentários por Conteúdo ---")
        for c in conteudos:
            comentarios = sum(1 for i in c.interacoes_recebidas if i.tipo_interacao == "comment")
            print(f"Conteúdo ID {c.id_conteudo} - Comentários: {comentarios}")

def formatar_tempo(segundos: int) -> str:
    """
    Formata o tempo em segundos para o formato HH:MM:SS.
    - Calcula as horas, minutos e segundos a partir dos segundos.
    """
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"
