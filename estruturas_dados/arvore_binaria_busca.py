from bintrees import AVLTree
from entidades.conteudo import Conteudo


class ArvoreBinariaBusca:
    def __init__(self) -> None:
        self._arvore_binaria: AVLTree = AVLTree()

    # Complexidade:
    # Pior caso:   O(log n) - mesmo em situações mais desfavoráveis, a árvore se ajusta para manter a altura e organização controladas, mantendo a inserção eficiente.
    # Melhor caso: Ω(log n) - a chave é inserida em uma parte já balanceada da árvore sem necessidade de reorganização, o que mantém a eficiência da inserção.
    # Caso médio:  Θ(log n) - a chave é inserida normalmente e a árvore realiza algumas rotações para se redistribuir, garantindo que a altura continue próxima a logaritmo do número de nós.
    def inserir_elemento(self, chave: int, elemento: object) -> None:
        self._arvore_binaria.insert(chave, elemento)

    # Complexidade:
    # Pior caso:   O(log n) - mesmo removendo nós que exigem vários ajustes, a árvore garante que a operação seja eficiente devido ao autobalanceamento.
    # Melhor caso: Ω(log n) - o nó a ser removido precisa de poucas reorganizações para manter o balanceamento.
    # Caso médio:  Θ(log n) - a remoção envolve buscar o nó e realizar algumas reorganizações para reorganizar a árvore.
    def remover_elemento(self, chave: int) -> None:
        self._arvore_binaria.remove(chave)

    # Complexidade:
    # Pior caso:   O(log n) - a estrutura mantém a altura controlada devido o autobalanceamento, garantindo que seja eficiente mesmo no pior caso.
    # Melhor caso: Ω(1) - o elemento buscado está na raiz ou próximo dela, o que permite que a busca seja muito rápida.
    # Caso médio:  Θ(log n) - a busca percorre um caminho proporcional à altura da árvore balanceada.
    # --------------------------------------------------------------------------------------------
    # Usando dicas de tipo, a partir da versão 3.10, é possível definir os possíveis retornos com o pipe (|).
    # Caso fosse em versões anteriores à 3.10, seria necessário importar 'Union' da biblioteca 'typing', daí o a dica de retorno seria: Union[Conteudo, None].
    def buscar_elemento(self, chave: int) -> object | None:
        # É extremamente necessário que seja implementado um try-except para o caso de tentativa de localização de chave pois ao não localizar a chave solicitada,
        # é retornado um 'raise' (palavra-chave para gerar uma exceção).
        try:
            return self._arvore_binaria.get_value(chave)
        except Exception:
            return None

    # Complexidade:
    # Pior caso:   O(n) - visita todos os nós, independentemente do tamanho e distribuição da árvore.
    # Melhor caso: Ω(n) - mesmo no melhor cenário, é necessário visitar todos os nós da árvore.
    # Caso médio:  Θ(n) - percorre todos os nós com custo constante por visita.
    def percurso_in_order(self) -> list:
        conteudos: list = []

        for _, elemento in self._arvore_binaria.items():
            conteudos.append(elemento)

        return conteudos


# Sub-classe de ArvoreBinariaBusca.
# Pensando em trazer o conceito de Herança, fizemos a árvore de conteúdos como sub-classe de ArvoreBinariaBusca.
# Definimos os métodos de inserção, remoção, busca e visualização, em que cada método desta sub-classe invoca os métodos
# da classe principal (ArvoreBinariaBusca).
class ArvoreConteudos(ArvoreBinariaBusca):
    def __init__(self):
        super().__init__()

    def inserir_conteudo(self, conteudo: Conteudo) -> None:
        self.inserir_elemento(conteudo.id_conteudo, conteudo)

    def buscar_conteudo(self, id_conteudo: int) -> Conteudo | None:
        return self.buscar_elemento(id_conteudo)

    def remover_conteudo(self, id_conteudo: int) -> None:
        self.remover_elemento(id_conteudo)

    def percurso_em_ordem(self) -> list:
        return self.percurso_in_order()


class ArvoreUsuarios(ArvoreBinariaBusca):
    pass
