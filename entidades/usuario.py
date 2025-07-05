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
    def registrar_interacao(self, interacao):
        self.__interacoes_realizadas.append(interacao)

    def obter_interacoes_por_tipo(
        self, tipo_desejado: str
    ) -> list:  # filtra interacoes_realizadas
        return [
            i for i in self.interacoes_realizadas if i.tipo_interacao == tipo_desejado
        ]

    def obter_conteudos_unicos_consumidos(
        self,
    ) -> set:  # retorna set de objetos 'conteúdo'
        return set(i.conteudo_associado for i in self.interacoes_realizadas)

    def calcular_tempo_total_consumo_plataforma(
        self, plataforma
    ) -> int:  # retorna tempo para uma plataforma
        return sum(
            i.watch_duration_seconds
            for i in self.interacoes_realizadas
            if i.plataforma_interacao == plataforma
        )

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
