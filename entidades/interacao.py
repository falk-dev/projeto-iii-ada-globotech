from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .conteudo import Conteudo
    from .plataforma import Plataforma


class Interacao:
    TIPOS_INTERACAO_VALIDOS = {"view_start", "like", "share", "comment"}

    def __init__(
        self,
        conteudo_associado: "Conteudo",
        id_usuario: str,
        timestamp_interacao: str,
        plataforma_interacao: "Plataforma",
        tipo_interacao: str,
        watch_duration_seconds: str,
        comment_text: str = "",
    ) -> None:
        self._conteudo_associado = conteudo_associado
        self._id_usuario = int(id_usuario)
        self._plataforma_interacao = plataforma_interacao

        if isinstance(timestamp_interacao, str):
            self._timestamp_interacao = datetime.fromisoformat(timestamp_interacao)
        else:
            self._timestamp_interacao = timestamp_interacao

        if tipo_interacao not in self.TIPOS_INTERACAO_VALIDOS:
            raise ValueError(
                f"Tipo de interação '{tipo_interacao}' inválido. Permitidos: {self.TIPOS_INTERACAO_VALIDOS}"
            )
        self._tipo_interacao = tipo_interacao

        self._watch_duration_seconds = max(0, int(watch_duration_seconds or 0))
        self._comment_text = (comment_text or "").strip()

    @property
    def id_interacao(self):
        return self._id_interacao

    @property
    def conteudo_associado(self):
        return self._conteudo_associado

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def plataforma_interacao(self):
        return self._plataforma_interacao

    @property
    def timestamp_interacao(self):
        return self._timestamp_interacao

    @property
    def tipo_interacao(self):
        return self._tipo_interacao

    @property
    def watch_duration_seconds(self):
        return self._watch_duration_seconds

    @property
    def comment_text(self):
        return self._comment_text

    def is_engajamento(self):
        return self._tipo_interacao in {"like", "share", "comment"}

    def is_comentario(self):
        return self._tipo_interacao == "comment" and bool(self._comment_text)

    def __str__(self):
        relatorio = f"Interação do tipo: '{self.tipo_interacao}'\n"
        relatorio += f"  - Usuário ID: {self.id_usuario}\n"
        relatorio += f"  - Data/Hora: {self.timestamp_interacao}\n"
        relatorio += f"  - Conteúdo: '{self.conteudo_associado.nome_conteudo}' (ID: {self.conteudo_associado.id_conteudo})\n"
        relatorio += f"  - Plataforma: '{self.plataforma_interacao.nome_plataforma}'\n"

        if self.watch_duration_seconds:
            relatorio += (
                f"  - Duração Assistida: {self.watch_duration_seconds} segundos\n"
            )

        if self.comment_text:
            relatorio += f'  - Comentário: "{self.comment_text}"\n'

        relatorio += "---------------------------------------\n"

        return relatorio

    def __repr__(self):
        return (
            f"Interacao("
            f"conteudo_associado={repr(self.conteudo_associado)}, "
            f"id_usuario={repr(self.id_usuario)}, "
            f"timestamp_interacao={repr(self.timestamp_interacao)}, "
            f"plataforma_interacao={repr(self.plataforma_interacao)}, "
            f"tipo_interacao={repr(self.tipo_interacao)}, "
            f"watch_duration_seconds={repr(self.watch_duration_seconds)}, "
            f"comment_text={repr(self.comment_text)})"
        )