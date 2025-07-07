class AlgoritmosOrdenacao:
    """
    Classe que implementa algoritmos de ordenação.
    """

    @staticmethod
    def bubble_sort(lista, key=lambda x: x):
        """
        Implementa o Bubble Sort para ordenar uma lista de objetos com base em uma chave.

        Complexidade:
            - Melhor caso: O(n)
            - Caso médio: O(n^2)
            - Pior caso: O(n^2)
        """
        n = len(lista)
        # Percorre toda a lista
        for i in range(n):
            # Últimos i elementos já estão ordenados
            for j in range(0, n - i - 1):
                # Compara elementos adjacentes
                if key(lista[j]) > key(lista[j + 1]):
                    # Troca se estiver fora de ordem
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]

    @staticmethod
    def particionar(lista, key, inicio, fim):
        """
        Função auxiliar do Quick Sort que faz a partição da lista.
        Escolhe o último elemento como pivô e rearranja a lista de modo que
        todos os elementos menores que o pivô fiquem à esquerda e os maiores à direita.

        Complexidade: O(n)
        """
        pivo = key(lista[fim])
        i = inicio - 1
        # Percorre a sublista
        for j in range(inicio, fim):
            # Se o elemento atual é menor ou igual ao pivô
            if key(lista[j]) <= pivo:
                i += 1
                # Troca elementos
                lista[i], lista[j] = lista[j], lista[i]
        # Coloca o pivô na posição correta
        lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
        return i + 1

    @staticmethod
    def quick_sort(lista, key=lambda x: x, inicio=0, fim=None):
        """
        Implementa o algoritmo Quick Sort para ordenar uma lista de elementos com base em uma chave.

        Parâmetros:
            lista (list): Lista de elementos a ser ordenada.
            key (function): Função que define o critério de ordenação.
            inicio (int): Índice inicial da sublista.
            fim (int): Índice final da sublista.

        Complexidade de Tempo:
            - Melhor caso: O(n log n)
            - Caso médio: O(n log n)
            - Pior caso: O(n²) (quando a lista já está ordenada/invertida)
        Complexidade de Espaço:
            - O(log n) no caso médio (devido à pilha de recursão)
        """
        if fim is None:
            fim = len(lista) - 1
        if inicio < fim:
            # Particiona a lista e obtém o índice do pivô
            pivo_index = AlgoritmosOrdenacao.particionar(lista, key, inicio, fim)
            # Ordena recursivamente os elementos antes e depois do pivô
            AlgoritmosOrdenacao.quick_sort(lista, key, inicio, pivo_index - 1)
            AlgoritmosOrdenacao.quick_sort(lista, key, pivo_index + 1, fim)

# Função compatível com import direto
# Permite usar quick_sort(lista) diretamente sem instanciar a classe

def quick_sort(lista, key=None):
    """
    Ordena a lista in-place usando Quick Sort.

    Complexidade de Tempo:
        - Melhor caso: O(n log n)
        - Caso médio: O(n log n)
        - Pior caso: O(n²)
    Complexidade de Espaço:
        - O(log n) no caso médio (pilha de recursão)
    """
    if key is None:
        key = lambda x: x
    AlgoritmosOrdenacao.quick_sort(lista, key)
    return lista
