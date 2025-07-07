class AlgoritmosOrdenacao:
    """
    Classe que implementa algoritmos de ordenação.
    """

    """
Módulo que implementa algoritmos de ordenação: bubble_sort e quick_sort.
"""


def bubble_sort(lista, key=lambda x: x):
    """
    Implementa o Bubble Sort para ordenar uma lista de objetos com base em uma chave.

    Complexidade:
        - Melhor caso: O(n)
        - Caso médio: O(n^2)
        - Pior caso: O(n^2)
    """
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(lista[j]) > key(lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

def quick_sort(lista, key=lambda x: x, inicio=0, fim=None):
    """
    Implementa o Quick Sort para ordenar uma lista de elementos com base em uma chave.

    Parâmetros:
        lista (list): Lista de elementos a ser ordenada.
        key (function): Função que define o critério de ordenação.
        inicio (int): Índice inicial da sublista.
        fim (int): Índice final da sublista.

    Complexidade de Tempo:
        - Melhor caso: O(n log n)
        - Caso médio: O(n log n)
        - Pior caso: O(n²)

    Complexidade de Espaço:
        - O(log n) no caso médio (pilha de recursão).
    """
    if fim is None:
        fim = len(lista) - 1
    if inicio < fim:
        pivo_index = particionar(lista, key, inicio, fim)
        quick_sort(lista, key, inicio, pivo_index - 1)
        quick_sort(lista, key, pivo_index + 1, fim)

def particionar(lista, key, inicio, fim):
    """
    Função auxiliar do Quick Sort que faz a partição da lista.

    Complexidade: O(n)
    """
    pivo = key(lista[fim])
    i = inicio - 1
    for j in range(inicio, fim):
        if key(lista[j]) <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[fim] = lista[fim], lista[i + 1]
    return i + 1
