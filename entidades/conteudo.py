from .interacao import Interacao


class Conteudo:
    def __init__(self, id_conteudo: int, nome_conteudo: str):
        self._id_conteudo: int = id_conteudo
        self._nome_conteudo: str = nome_conteudo
        self._interacoes: list[Interacao] = []

    # Getters e Setters
    @property
    def id_conteudo(self) -> int:
        return self._id_conteudo

    @id_conteudo.setter
    def id_conteudo(self, id: int) -> None:
        self._id_conteudo = id

    @property
    def nome_conteudo(self) -> str:
        return self._nome_conteudo

    @nome_conteudo.setter
    def nome_conteudo(self, nome: str) -> None:
        self._nome_conteudo = nome

    @property
    def interacoes(self):
        return self._interacoes

    # Método de interação
    def adicionar_interacao(self, interacao: Interacao) -> None:
        self._interacoes.append(interacao)

    # Métodos mágicos
    def __str__(self) -> str:
        relatorio = f"ID: {self.id_conteudo}\n"
        relatorio += f"Conteúdo: {self.nome_conteudo}\n"
        relatorio += f"\n--------------------------------\n"

        return relatorio

    def __repr__(self) -> str:
        return f"Conteudo(id_conteudo={self.id_conteudo}, nome_conteudo={self.nome_conteudo})"
