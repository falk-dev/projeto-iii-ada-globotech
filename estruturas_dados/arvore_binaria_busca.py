from bintrees import AVLTree


class ArvoreBinariaBusca:
    def __init__(self) -> None:
        self._arvore_binaria: AVLTree = AVLTree()

    # Complexidade:
    # Pior caso:   O(log n) - mesmo em situações mais desfavoráveis, a árvore se ajusta para manter a altura e organização controladas, mantendo a inserção eficiente.
    # Melhor caso: Ω(log n) - a chave é inserida em uma parte já balanceada da árvore sem necessidade de reorganização, o que mantém a eficiência da inserção.
    # Caso médio:  Θ(log n) - a chave é inserida normalmente e a árvore realiza algumas rotações para se redistribuir, garantindo que a altura continue próxima a logaritmo do número de nós.
    def inserir_elemento(self, chave: int, elemento: str) -> None:
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
    def buscar_elemento(self, chave: int) -> str:
        return self._arvore_binaria.get_value(chave)

    # Complexidade:
    # Pior caso:   O(n) - visita todos os nós, independentemente do tamanho e distribuição da árvore.
    # Melhor caso: Ω(n) - mesmo no melhor cenário, é necessário visitar todos os nós da árvore.
    # Caso médio:  Θ(n) - percorre todos os nós com custo constante por visita.
    def visualizacao_in_order(self) -> None:
        for chave, elemento in self._arvore_binaria.items():
            print(chave, "->", elemento)
