class Usuario:
    # Construtor
    def __init__(self, id_usuario: int) -> None:
        self.__id_usuario: int = id_usuario
        self.__interacoes_realizadas: list = []  # lista com objetos Interacao

    # Getters e setters
    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def interacoes_realizadas(self):
        return self.__interacoes_realizadas

    # Métodos
    """
    Adiciona uma nova interação à lista de interações do usuário.

    - Melhor caso (Ω): O(1), inserção direta no final da lista.
    - Caso médio (Θ): O(1), operação constante típica de `list.append()`.
    - Pior caso (O): O(1), mesmo em caso de listas grandes (não exige realocação visível em Python).

    Justificativa: a operação de adicionar ao final da lista é constante em listas Python dinâmicas.
    """
    def registrar_interacao(self, interacao):
        self.__interacoes_realizadas.append(interacao)

    """
    Filtra as interações realizadas por tipo.

    - Melhor caso (Ω): O(n), se todas as interações forem do tipo desejado.
    - Caso médio (Θ): O(n), onde n é o número de interações.
    - Pior caso (O): O(n), se nenhuma for do tipo buscado.

    Justificativa: percorre todas as interações verificando seu tipo.
    """
    def obter_interacoes_por_tipo(
        self, tipo_desejado: str
    ) -> list:  # filtra interacoes_realizadas
        return [
            i for i in self.interacoes_realizadas if i.tipo_interacao == tipo_desejado
        ]

    """
    Retorna o conjunto de conteúdos únicos consumidos pelo usuário.

    - Melhor caso (Ω): O(n), se todos os conteúdos forem únicos.
    - Caso médio (Θ): O(n), onde n é o número de interações.
    - Pior caso (O): O(n), com conversão para conjunto (`set()`).

    Justificativa: cria uma lista e transforma em conjunto, ambos com custo linear.
    """
    def obter_conteudos_unicos_consumidos(
        self,
    ) -> set:  # retorna set de objetos 'conteúdo'
        return set(i.conteudo_associado for i in self.interacoes_realizadas)

    """
    Calcula o tempo total de consumo do usuário em uma plataforma específica.

    - Melhor caso (Ω): O(n), se todas as interações forem da plataforma buscada.
    - Caso médio (Θ): O(n), onde n é o número de interações.
    - Pior caso (O): O(n), se nenhuma for da plataforma buscada.

    Justificativa: itera sobre todas as interações e filtra por nome de plataforma.
    """
    def calcular_tempo_total_consumo_plataforma(
        self, plataforma
    ) -> int:  # retorna tempo para uma plataforma
        return sum(
            i.watch_duration_seconds
            for i in self.interacoes_realizadas
            if i.plataforma_interacao == plataforma
        )

    """
    Retorna as plataformas mais frequentes entre as interações do usuário.

    - Melhor caso (Ω): O(n log n), com poucos empates e distribuições homogêneas.
    - Caso médio (Θ): O(n log n), onde n é o número de interações (contagem + ordenação).
    - Pior caso (O): O(n log n), se houver muitas plataformas com contagem próxima.

    Justificativa: o uso de Counter (O(n)) seguido de `most_common()` (ordenado internamente) domina o custo total.
    """
    def plataformas_mais_frequentes(
        self, top_n=3
    ) -> list:  # retorna as plataformas mais frequentes do usuário
        cont = {}
        for interacao in self.interacoes_realizadas:
            plataforma = interacao.plataforma
            cont[plataforma] = cont.get(plataforma, 0) + 1
            return sorted(cont, key=lambda p: cont[p], reverse=True)[:top_n]

    # Métodos mágicos
    def __str__(self):
        interacoes_formatadas = "\n".join(str(i) for i in self.__interacoes_realizadas)
        """Retorna o id do usuário e interações como string formatada"""
        return (
            f"ID do Usuário:{self.__id_usuario}\nInterações:\n{interacoes_formatadas}"
        )

    def __repr__(self):
        """Retorna uma representação legível do usuário"""
        return f"Usuário(id={self.__id_usuario}, interações='{self.__interacoes_realizadas}')"
