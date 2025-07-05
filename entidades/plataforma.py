class Plataforma:
    # Construtor
    def __init__(self, id_plataforma: int, nome_plataforma: str) -> None:
        self.__id_plataforma = id_plataforma
        self.__nome_plataforma = nome_plataforma

    # Getters e Setters

    # Property para nome_plataforma
    @property
    def nome_plataforma(self):
        return self.__nome_plataforma

    @nome_plataforma.setter
    def nome_plataforma(self, novo_nome):
        """Define o nome da plataforma, garantindo que não seja vazio."""
        if not novo_nome.strip():
            raise ValueError("O nome da plataforma não pode ser vazio.")
        self.__nome_plataforma = novo_nome.strip()

    # Property para id_plataforma
    @property
    def id_plataforma(self):
        return self.__id_plataforma

    @id_plataforma.setter
    def id_plataforma(self, novo_id):
        """Define o ID da plataforma, garantindo que seja um inteiro não negativo."""
        if novo_id is not None and (not isinstance(novo_id, int) or novo_id < 0):
            raise ValueError("O ID da plataforma deve ser um inteiro não negativo.")
        self.__id_plataforma = novo_id

    @property
    def nome_plataforma(self) -> str:
        return self.__nome_plataforma

    # Metodos Magicos

    def __str__(self):
        relatorio = f"ID: {self.id_plataforma}\n"
        relatorio += f"Plataforma: {self.nome_plataforma}\n"
        relatorio += f"\n--------------------------------\n"
        return relatorio

    def __repr__(self):
        """Retorna uma representação legível da plataforma."""
        return f"Plataforma(id={self.__id_plataforma}, nome='{self.__nome_plataforma}')"

    def __eq__(self, other):
        """Compara plataformas com base no nome."""
        return (
            isinstance(other, Plataforma)
            and self.__nome_plataforma == other.__nome_plataforma
        )

    def __hash__(self):
        """Permite uso de Plataforma como chave em dicionários/sets."""
        return hash(self.__nome_plataforma)

    # Metodo magico para comparação de plataformas para ordenação
    def __lt__(self, other):
        """Compara plataformas com base no nome para ordenação."""
        if not isinstance(other, Plataforma):
            return NotImplemented
        return self.__nome_plataforma < other.__nome_plataforma