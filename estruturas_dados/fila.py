# Para o caso desta classe (Fila), será utilizada a estrutura de dados 'deque' de forma que se comporte como uma fila (Queue).
from collections import deque


class Fila:
    def __init__(self):
        self._fila = deque()

    # Complexidade:
    # Pior caso:   O(1) - sempre enfileira ao fim da fila
    # Melhor caso: Ω(1) - idem, operação constante
    # Caso médio:  Θ(1) - sempre constante, independentemente do tamanho da fila
    def enfileirar(self, linha_csv):
        self._fila.append(linha_csv)

    # Complexidade:
    # Pior caso:   O(1) - sempre desenfileira o primeiro da fila
    # Melhor caso: Ω(1) - idem, operação constante
    # Caso médio:  Θ(1) - sempre constante, independentemente do tamanho da fila
    def desenfileirar(self) -> bool:
        if self.esta_vazia():
            return False

        self._fila.popleft()
        return self._fila[0]

    # Complexidade:
    # Pior caso:   O(1) - verificação do estado (constante) através da função len(), que por sua vez é constante
    # Melhor caso: Ω(1) - idem, pois não depende do tamanho da fila
    # Caso médio:  Θ(1) - sempre constante, independentemente do estado da fila
    def esta_vazia(self) -> bool:
        return len(self._fila) == 0
