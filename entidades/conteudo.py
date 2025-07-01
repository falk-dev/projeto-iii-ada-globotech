from .interacao import Interacao
from collections import Counter


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

    # Métodos de interação
    def adicionar_interacao(self, interacao: Interacao) -> None:
        self._interacoes.append(interacao)

    def calcular_contagem_por_tipo_interacao(self) -> dict:
        # Caso nao tenha interações cadastradas, retorna um dicionario vazio
        if not self._interacoes:
            return {}

        # Criando uma lista em que vai ser iterado na coluna de tipo de interação
        # Daí, o que vai ter de retorno é algo como: ['view_start', 'like', 'like', 'comment']
        tipos = [interacao.tipo_interacao for interacao in self.interacoes]

        # O counter é o responsável por transformar a lista acima em um dicionário
        # Então o resultado vai ser algo como: {'view_start': 1, 'like': 2, 'comment': 1}
        return Counter(tipos)

    def calcular_total_interacoes_engajamento(self) -> str:
        interacoes = {"like", "comment", "share"}

        engajamentos = sum(1 for i in self.interacoes if i.tipo_interacao in interacoes)

        if not engajamentos:
            relatorio = f"\n➡️   {self.nome_conteudo}\n"
            relatorio += f"\nNenhuma interação registrada"
            relatorio += "\n\n---------------------------------------"
            return relatorio

        relatorio = f"➡️   {self.nome_conteudo}\n"
        relatorio += f"\nTotal de engajamentos: {engajamentos}"

        # Linha de separação entre relatórios
        relatorio += "\n\n---------------------------------------"

        return f"\n{relatorio}"

    def converter_segundos_para_hms(self, segundos: int) -> str:
        try:
            # Verificação para ter certeza de que o tipo do dado que chegou por parâmetro é de fato um número
            if not isinstance(segundos, (int, float)):
                print("O argumento deve ser um número.")
                return None

            # Conversão de segundos para horas, minutos e segundos
            horas = segundos // 3600
            minutos = (segundos % 3600) // 60
            segundos_restantes = segundos % 60

            # Formatação em HH:MM:SS
            return f"{int(horas):02d}:{int(minutos):02d}:{segundos_restantes:05.2f}"

        except Exception as e:
            print(f"{e}: não foi possível converter os segundos em HH:MM:SS.")
            return None

    def calcular_tempo_total_consumo(self) -> str:
        tempo_assistido_conteudo = 0

        # Laço para armazenar em uma variável os segundos de tempo assistido
        # Em qque o tempo seja maior do que 0 segundos
        for interacao in self.interacoes:
            if interacao.watch_duration_seconds > 0:
                tempo_assistido_conteudo += interacao.watch_duration_seconds

        # Enviando para o método de converter e formatar o tmepo assistido de conteúdo
        tempo_assistido_conteudo = self.converter_segundos_para_hms(
            tempo_assistido_conteudo
        )

        relatorio = (
            f"📺 {self.id_conteudo} - {self.nome_conteudo}: {tempo_assistido_conteudo}"
        )

        return relatorio

    def calcular_media_tempo_consumo(self) -> str:
        tempo = [
            interacoes.watch_duration_seconds
            for interacoes in self.interacoes
            if interacoes.watch_duration_seconds > 0
        ]
        media_tempo_consumo = sum(tempo) / len(tempo)
        media_tempo_consumo = self.converter_segundos_para_hms(media_tempo_consumo)

        relatorio = (
            f"📺 {self.id_conteudo} - {self.nome_conteudo}: {media_tempo_consumo}"
        )

        return relatorio

    def listar_comentarios(self) -> list:
        comentarios = [
            interacoes.comment_text
            for interacoes in self.interacoes
            if interacoes.comment_text != ""
        ]

        relatorio = f"➡️   {self.nome_conteudo}\n"

        if not comentarios:
            relatorio += f"Nenhum comentário registrado."
            relatorio += "\n\n---------------------------------------\n"
            return relatorio

        for c in comentarios:
            relatorio += f"- {c}\n"

        relatorio += "\n---------------------------------------\n"
        return relatorio

    # Métodos mágicos
    def __str__(self) -> str:
        relatorio = f"ID: {self.id_conteudo}\n"
        relatorio += f"Conteúdo: {self.nome_conteudo}\n"
        relatorio += f"\n--------------------------------\n"

        return relatorio

    def __repr__(self) -> str:
        return f"Conteudo(id_conteudo={self.id_conteudo}, nome_conteudo={self.nome_conteudo})"
