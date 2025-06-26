from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca
from entidades.plataforma import Plataforma


class SistemaAnaliseEngajamento:
    def __init__(self):
        self._fila_interacoes_brutas: Fila = Fila()
        self._arvore_conteudos: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._arvore_usuarios: ArvoreBinariaBusca = ArvoreBinariaBusca()
        self._plataformas_registradas: dict[str, Plataforma] = {}
