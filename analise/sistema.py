import csv

from estruturas_dados.fila import Fila
from estruturas_dados.algoritmos_ordenacao import quick_sort 

from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo
from entidades.usuario import Usuario
from entidades.interacao import Interacao

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

    def percurso_in_order(self) -> list:
        return self._arvore_conteudos.percurso_in_order()
    
        # -------- Métodos da árvore de usuário --------
    def inserir_usuario(self, usuario: Usuario) -> None:
        self._arvore_usuarios.inserir_elemento(usuario.id_usuario, usuario)

    def buscar_usuario(self, id_usuario: int) -> Usuario | None:
        return self._arvore_usuarios.buscar_elemento(id_usuario)

    def remover_usuario(self, id_usuario: int) -> None:
        self._arvore_usuarios.remover_elemento(id_usuario)

    def percurso_em_ordem(self) -> list:
        return self._arvore_usuarios.percurso_in_order()

    # -------- Métodos de processamento do arquivo csv --------
    """
    Lê o arquivo CSV e enfileira cada linha na estrutura de fila.

    - Melhor caso (Ω): O(n), se o arquivo for lido corretamente sem erros e todas as linhas forem válidas.
    - Caso médio (Θ): O(n), onde n é o número de linhas do CSV.
    - Pior caso (O): O(n), leitura sequencial e enfileiramento de n itens.

    Justificativa: a operação principal aqui é iterar sobre todas as linhas do CSV e armazená-las na fila.
    """
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
    """
    Processa cada interação da fila e atualiza as árvores e plataformas.

    - Melhor caso (Ω): O(n log n), se todas as buscas e inserções nas árvores forem balanceadas e rápidas.
    - Caso médio (Θ): O(n log n), onde n é o número de interações na fila, pois cada interação envolve múltiplas operações logarítmicas (inserção/busca em árvore).
    - Pior caso (O): O(n log n), com custo dominante vindo das árvores AVL.

    Justificativa: para cada linha desenfileirada, o método realiza buscas e inserções nas árvores AVL e em dicionário, o que mantém a complexidade logarítmica.
    """
    def processar_interacoes_da_fila(self) -> None:
        while not self._fila_interacoes_brutas.esta_vazia():
            linha = self._fila_interacoes_brutas.desenfileirar()

            # Extrai os dados da linha do CSV
            id_usuario = linha.get("id_usuario")
            id_conteudo = linha.get("id_conteudo")
            nome_conteudo = linha.get("nome_conteudo")
            timestamp_interacao = linha.get("timestamp_interacao")
            nome_plataforma = linha.get("nome_plataforma")
            tipo_interacao = linha.get("tipo_interacao")
            watch_duration_seconds = linha.get("watch_duration_seconds")
            comment_text = linha.get("comment_text", "")

            # Conteúdo
            conteudo = self._arvore_conteudos.buscar_elemento(int(id_conteudo))
            if conteudo is None:
                conteudo = Conteudo(int(id_conteudo), nome_conteudo)
                self.inserir_conteudo(conteudo)

            # Usuário
            usuario = self._arvore_usuarios.buscar_elemento(int(id_usuario))
            if usuario is None:
                usuario = Usuario(int(id_usuario))
                self.inserir_usuario(usuario)

            # Plataforma
            plataforma = self._plataformas_registradas.get(nome_plataforma)
            if plataforma is None:
                plataforma = Plataforma(len(self._plataformas_registradas) + 1, nome_plataforma)
                self._plataformas_registradas[nome_plataforma] = plataforma

            # Cria a interação
            try:
                interacao_obj = Interacao(
                    conteudo_associado=conteudo,
                    id_usuario=id_usuario,
                    timestamp_interacao=timestamp_interacao,
                    plataforma_interacao=plataforma,
                    tipo_interacao=tipo_interacao,
                    watch_duration_seconds=watch_duration_seconds,
                    comment_text=comment_text
                )
            except Exception as e:
                print(f"Erro ao criar interação: {e}")
                continue

            # Registra a interação no usuário e no conteúdo
            usuario.registrar_interacao(interacao_obj)
            conteudo.adicionar_interacao(interacao_obj)

    """
    Gera relatório dos usuários mais ativos com base na quantidade de interações.

    - Melhor caso (Ω): O(n log n), se a ordenação for eficiente e a árvore já estiver balanceada.
    - Caso médio (Θ): O(n log n), onde n é o número de usuários.
    - Pior caso (O): O(n²), caso o Quick Sort tenha piores divisões.

    Justificativa: a extração dos usuários da árvore leva O(n), e a ordenação com Quick Sort pode variar de O(n log n) a O(n²).
    """
    def gerar_relatorio_atividade_usuarios(self, top_n: int = None):
        # Obtém todos os usuários da árvore em ordem
        usuarios = self._arvore_usuarios.percurso_in_order()
        #print(f"DEBUG: Usuários encontrados: {len(usuarios)}")

        # Cria lista de tuplas (usuario, tempo_total_consumo)
        usuarios_consumo = []
        for usuario in usuarios:
            #print(f"DEBUG: Usuário {usuario.id_usuario}")
            #print(f"DEBUG: Interações: {getattr(usuario, '_Usuario__interacoes_realizadas', None)}")
            tempo_total = sum(
                interacao.watch_duration_seconds
                for interacao in getattr(usuario, '_Usuario__interacoes_realizadas', [])
            )
            usuarios_consumo.append((usuario, tempo_total))

        # Ordena a lista com base no tempo total de consumo (decrescente)
        quick_sort(usuarios_consumo, key=lambda x: x[1])

        # Reverte para ordem decrescente (Quick Sort faz crescente por padrão)
        usuarios_consumo.reverse()

        # Limita ao top_n se for informado
        if top_n is not None:
            usuarios_consumo = usuarios_consumo[:top_n]

        # Exibe o relatório
        print("\n--- Relatório: Usuários com Maior Tempo Total de Consumo ---")
        for usuario, tempo in usuarios_consumo:
            print(f"Usuário ID {usuario.id_usuario} - Tempo Total: {formatar_tempo(tempo)}")
            
# Relatorios Analiticos
    """
    Exibe um resumo analítico com métricas de engajamento por tipo de conteúdo e plataforma.

    - Melhor caso (Ω): O(n), se os dados estiverem organizados e exigirem poucas iterações por categoria.
    - Caso médio (Θ): O(n), onde n é o total de conteúdos percorridos na árvore.
    - Pior caso (O): O(n), se todos os conteúdos tiverem muitos dados e diferentes tipos/plataformas.

    Justificativa: percorre linearmente os conteúdos para agregar contagens e tempos por tipo/plataforma.
    """
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

    """
    Exibe os conteúdos com maior engajamento baseado na soma de interações (like, comment, share).

    - Melhor caso (Ω): O(n log n), com partições equilibradas no Quick Sort.
    - Caso médio (Θ): O(n log n), onde n é o número de conteúdos na árvore.
    - Pior caso (O): O(n²), se o Quick Sort operar em ordem ruim de pivôs (lista já ordenada, por exemplo).

    Justificativa: a ordenação dos conteúdos por engajamento domina o custo, após a coleta linear dos dados.
    """
    def relatorio_conteudos_mais_engajados(self):
        conteudos = self._arvore_conteudos.percurso_in_order()
        engajamento = []
        for conteudo in conteudos:
            # Tenta usar interacoes_recebidas, se não existir, usa interacoes
            interacoes = getattr(conteudo, 'interacoes_recebidas', None)
            if interacoes is None:
                interacoes = getattr(conteudo, 'interacoes', [])
            likes = sum(1 for i in interacoes if getattr(i, 'tipo_interacao', None) == "like")
            shares = sum(1 for i in interacoes if getattr(i, 'tipo_interacao', None) == "share")
            comments = sum(1 for i in interacoes if getattr(i, 'tipo_interacao', None) == "comment")
            total = likes + shares + comments
            engajamento.append((conteudo, total, likes, shares, comments))
        quick_sort(engajamento, key=lambda x: x[1])
        engajamento.reverse()
        print("\n--- Conteúdos Mais Engajados ---")
        for c, total, likes, shares, comments in engajamento[:10]:
            print(f"Conteúdo ID {c.id_conteudo} - {c.nome_conteudo} | Engajamento Total: {total}\n👍 {likes}\n🔄 {shares}\n💬 {comments}\n")

    """
    Lista a quantidade de comentários para cada conteúdo registrado.

    - Melhor caso (Ω): O(n), se todos os conteúdos tiverem interações válidas do tipo 'comment'.
    - Caso médio (Θ): O(n), onde n é o número de conteúdos na árvore.
    - Pior caso (O): O(n), iteração simples em todos os conteúdos.

    Justificativa: cada conteúdo é acessado uma vez para verificar interações do tipo 'comment', com complexidade linear.
    """
    def gerar_relatorio_comentarios_por_conteudo(self):
        conteudos = self._arvore_conteudos.percurso_in_order()
        print("\n--- Comentários por Conteúdo ---")
        for c in conteudos:
            interacoes = getattr(c, 'interacoes_recebidas', None)
            if interacoes is None:
                interacoes = getattr(c, 'interacoes', [])
            comentarios = [getattr(i, 'comment_text', '') for i in interacoes if getattr(i, 'tipo_interacao', None) == "comment"]
            print(f"Conteúdo ID {c.id_conteudo} - {c.nome_conteudo} | 💬 Comentários: {len(comentarios)}")
            for texto in comentarios:
                print(f"  - {texto}")
            print("")
    
    """
    Gera relatório de conteúdos mais engajados, ordenando pelo total de interações com Quick Sort.

    - Melhor caso (Ω): O(n log n), quando a partição do Quick Sort é sempre equilibrada.
    - Caso médio (Θ): O(n log n), onde n é o número de conteúdos a ordenar.
    - Pior caso (O): O(n²), se os conteúdos já estiverem em ordem desfavorável e o pivô for mal escolhido.

    Justificativa: o tempo de ordenação depende do algoritmo escolhido (Quick Sort neste caso), que no pior caso pode degradar para O(n²).
    """
    def gerar_relatorio_engajamento_conteudos(self, top_n: int = None):
        # Obtém todos os conteúdos armazenados na árvore binária (ordenados por ID)
        conteudos = self._arvore_conteudos.percurso_in_order()

        # Calcula o total de interações (engajamento) para cada conteúdo
        engajamento_conteudos = []
        for conteudo in conteudos:
            total_interacoes = len(conteudo.interacoes)
            engajamento_conteudos.append((conteudo, total_interacoes))

        # Ordena os conteúdos com base na métrica de engajamento (número de interações)
        # Usa quick_sort (poderia ser insertion_sort para listas pequenas)
        from estruturas_dados.algoritmos_ordenacao import quick_sort
        quick_sort(engajamento_conteudos, key=lambda x: x[1])

        # Inverte a lista para ordem decrescente (do mais engajado para o menos)
        engajamento_conteudos.reverse()

        # Se top_n foi especificado, limita a lista aos primeiros N conteúdos
        if top_n is not None:
            engajamento_conteudos = engajamento_conteudos[:top_n]

        # Exibe o relatório formatado no console
        print("\n--- Relatório: Conteúdos com Maior Engajamento ---")
        for conteudo, total in engajamento_conteudos:
            print(f"Conteúdo ID {conteudo.id_conteudo} - Nome: {conteudo.nome_conteudo} - Total de Interações: {total}")

def formatar_tempo(segundos: int) -> str:
    """
    Formata o tempo em segundos para o formato HH:MM:SS.
    - Calcula as horas, minutos e segundos a partir dos segundos.
    """
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60
    return f"{horas:02}:{minutos:02}:{segundos_restantes:02}"