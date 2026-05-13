from collections import deque
import heapq
import itertools


# ============================================================
# 8-PUZZLE COM BFS, DFS, CUSTO UNIFORME, GREEDY E A*
#
# Representacao do estado: tupla de 9 inteiros (0 a 8),
# onde 0 representa o espaco vazio. Exemplo:
# (1, 2, 3,
#  4, 0, 5,
#  6, 7, 8)
# ============================================================

# Contador global para desempate em filas de prioridade.
# Evita erro de comparacao quando duas prioridades sao iguais.
CONTADOR = itertools.count()


class No:
    # Estrutura basica de um no na arvore de busca.
    # Guarda o estado, ponteiro para o pai e metadados
    # usados para calcular custo, profundidade e imprimir caminho.
    def __init__(self, estado, pai=None, acao=None, custo=0, profundidade=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.profundidade = profundidade


def ler_estado(nome):
    # Le um estado valido do usuario.
    # Garante exatamente 9 numeros, todos entre 0 e 8 sem repeticao.
    print(f"\nDigite o {nome}.")
    print("Use 0 para representar o espaço vazio.")
    print("Exemplo: 1 2 3 4 0 5 6 7 8")
    
    while True:
        entrada = input(f"{nome}: ").strip().split()

        # Valida quantidade de elementos.
        if len(entrada) != 9:
            print("Erro: digite exatamente 9 números.")
            continue

        # Converte para inteiros (pode falhar se houver letras).
        try:
            numeros = tuple(map(int, entrada))
        except ValueError:
            print("Erro: digite apenas números.")
            continue

        # Confere se contem exatamente os numeros 0..8.
        if sorted(numeros) != list(range(9)):
            print("Erro: o estado deve conter os números de 0 a 8, sem repetição.")
            continue

        return numeros


def imprimir_estado(estado):
    # Imprime o tabuleiro 3x3, trocando 0 por '_' para legibilidade.
    for i in range(0, 9, 3):
        linha = estado[i:i + 3]
        print(" ".join("_" if x == 0 else str(x) for x in linha))
    print()


def posicoes_objetivo(estado_objetivo):
    # Mapeia cada valor para sua posicao no estado objetivo.
    # Ex: {valor: indice}.
    return {valor: indice for indice, valor in enumerate(estado_objetivo)}


def manhattan(estado, estado_objetivo):
    # Heuristica Manhattan: soma das distancias verticais + horizontais
    # de cada peca ate sua posicao no objetivo. Ignora o 0.
    pos_obj = posicoes_objetivo(estado_objetivo)
    distancia = 0

    for indice_atual, valor in enumerate(estado):
        # O espaco vazio nao conta na heuristica.
        if valor == 0:
            continue

        indice_objetivo = pos_obj[valor]

        linha_atual, coluna_atual = divmod(indice_atual, 3)
        linha_objetivo, coluna_objetivo = divmod(indice_objetivo, 3)

        distancia += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)

    return distancia


def obter_sucessores(estado):
    # Gera todos os sucessores validos, movendo o espaco vazio
    # em ate quatro direcoes (cima, baixo, esquerda, direita).
    sucessores = []

    # Localiza o indice do vazio (0).
    indice_zero = estado.index(0)
    linha, coluna = divmod(indice_zero, 3)

    # Cada movimento e definido por (nome, delta_linha, delta_coluna).
    movimentos = [
        ("Cima", -1, 0),
        ("Baixo", 1, 0),
        ("Esquerda", 0, -1),
        ("Direita", 0, 1)
    ]

    for acao, dl, dc in movimentos:
        nova_linha = linha + dl
        nova_coluna = coluna + dc

        # Verifica se o movimento permanece dentro do tabuleiro.
        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_indice = nova_linha * 3 + nova_coluna

            novo_estado = list(estado)
            novo_estado[indice_zero], novo_estado[novo_indice] = (
                novo_estado[novo_indice],
                novo_estado[indice_zero]
            )

            # Armazena a acao e o novo estado em formato imutavel (tupla).
            sucessores.append((acao, tuple(novo_estado)))

    return sucessores


def reconstruir_caminho(no):
    # Caminha pelos pais ate a raiz, depois inverte para obter
    # o caminho do estado inicial ate a solucao.
    caminho = []

    while no is not None:
        caminho.append(no)
        no = no.pai

    caminho.reverse()
    return caminho


def contar_inversoes(estado):
    # Conta pares invertidos (i < j, valores[i] > valores[j]).
    # Usado para verificar se o problema tem solucao no 8-puzzle.
    valores = [x for x in estado if x != 0]
    inversoes = 0

    for i in range(len(valores)):
        for j in range(i + 1, len(valores)):
            if valores[i] > valores[j]:
                inversoes += 1

    return inversoes


def problema_tem_solucao(inicial, objetivo):
    # Para tabuleiro 3x3, dois estados são compatíveis se possuem
    # a mesma paridade de inversões.
    return contar_inversoes(inicial) % 2 == contar_inversoes(objetivo) % 2


# ============================================================
# BUSCAS NÃO INFORMADAS
# ============================================================

def busca_largura(inicial, objetivo):
    # BFS: explora por camadas usando fila.
    # Garante encontrar o menor numero de movimentos (custo uniforme).
    fronteira = deque([No(inicial)])
    visitados = {inicial}
    expandidos = 0

    while fronteira:
        # Remove o proximo no da fila (FIFO).
        no = fronteira.popleft()
        expandidos += 1

        # Se chegou ao objetivo, retorna o no e estatisticas.
        if no.estado == objetivo:
            return no, expandidos

        # Expande sucessores nao visitados.
        for acao, novo_estado in obter_sucessores(no.estado):
            if novo_estado not in visitados:
                visitados.add(novo_estado)
                filho = No(
                    estado=novo_estado,
                    pai=no,
                    acao=acao,
                    custo=no.custo + 1,
                    profundidade=no.profundidade + 1
                )
                fronteira.append(filho)

    return None, expandidos

def caminho_contem_estado(no, estado):
    # Verifica se um estado ja aparece no caminho atual (evita ciclos).
    atual = no

    while atual is not None:
        if atual.estado == estado:
            return True
        atual = atual.pai

    return False

# DFS com visitados por caminho
# essa versão evita voltar diretamente para o pai, mas ainda pode gerar ciclos mais longos. O limite de profundidade ajuda a evitar loops infinitos, mas pode impedir encontrar soluções mais profundas.
def busca_profundidade(inicial, objetivo, limite=30):
    # DFS com limite de profundidade.
    # Usa pilha (LIFO) e evita repetir estados no caminho atual.
    fronteira = [No(inicial)]
    expandidos = 0

    while fronteira:
        # Remove o ultimo no da pilha.
        no = fronteira.pop()

        if no.estado == objetivo:
            return no, expandidos

        # Limita a profundidade para evitar loops infinitos.
        if no.profundidade >= limite:
            continue

        expandidos += 1

        sucessores = obter_sucessores(no.estado)

        # Inverte para preservar uma ordem de expansao previsivel.
        for acao, novo_estado in reversed(sucessores):
            if caminho_contem_estado(no, novo_estado):
                continue

            filho = No(
                estado=novo_estado,
                pai=no,
                acao=acao,
                custo=no.custo + 1,
                profundidade=no.profundidade + 1
            )

            fronteira.append(filho)

    return None, expandidos


def busca_custo_uniforme(inicial, objetivo):
    # Custo uniforme: usa fila de prioridade pelo custo acumulado g(n).
    # Equivalente ao Dijkstra quando todos os custos sao 1.
    fronteira = []
    no_inicial = No(inicial)

    # (custo, contador, no) garante desempate estavel.
    heapq.heappush(fronteira, (0, next(CONTADOR), no_inicial))

    melhor_custo = {inicial: 0}
    expandidos = 0

    while fronteira:
        custo_atual, _, no = heapq.heappop(fronteira)

        # Ignora caminhos mais caros que o melhor conhecido.
        if custo_atual > melhor_custo[no.estado]:
            continue

        expandidos += 1

        if no.estado == objetivo:
            return no, expandidos

        for acao, novo_estado in obter_sucessores(no.estado):
            novo_custo = no.custo + 1

            # Atualiza se encontrou um caminho melhor para o estado.
            if novo_estado not in melhor_custo or novo_custo < melhor_custo[novo_estado]:
                melhor_custo[novo_estado] = novo_custo

                filho = No(
                    estado=novo_estado,
                    pai=no,
                    acao=acao,
                    custo=novo_custo,
                    profundidade=no.profundidade + 1
                )

                heapq.heappush(fronteira, (novo_custo, next(CONTADOR), filho))

    return None, expandidos


# ============================================================
# BUSCAS INFORMADAS
# ============================================================

def busca_gulosa(inicial, objetivo):
    # Greedy best-first: escolhe sempre o menor h(n).
    # Nao garante optimalidade, mas pode ser rapido.
    fronteira = []
    no_inicial = No(inicial)

    h = manhattan(inicial, objetivo)
    heapq.heappush(fronteira, (h, next(CONTADOR), no_inicial))

    visitados = set()
    expandidos = 0

    while fronteira:
        _, _, no = heapq.heappop(fronteira)

        # Evita reprocessar estados.
        if no.estado in visitados:
            continue

        visitados.add(no.estado)
        expandidos += 1

        if no.estado == objetivo:
            return no, expandidos

        for acao, novo_estado in obter_sucessores(no.estado):
            if novo_estado not in visitados:
                filho = No(
                    estado=novo_estado,
                    pai=no,
                    acao=acao,
                    custo=no.custo + 1,
                    profundidade=no.profundidade + 1
                )

                # Prioridade e somente a heuristica h(n).
                prioridade = manhattan(novo_estado, objetivo)
                heapq.heappush(fronteira, (prioridade, next(CONTADOR), filho))

    return None, expandidos


def busca_a_estrela(inicial, objetivo):
    # A*: combina custo real g(n) e heuristica h(n).
    # Com Manhattan (admissivel), A* encontra solucao otima.
    fronteira = []
    no_inicial = No(inicial)

    f = manhattan(inicial, objetivo)
    heapq.heappush(fronteira, (f, next(CONTADOR), no_inicial))

    melhor_custo = {inicial: 0}
    expandidos = 0

    while fronteira:
        _, _, no = heapq.heappop(fronteira)

        # Descarta se ja existe um caminho melhor conhecido.
        if no.custo > melhor_custo[no.estado]:
            continue

        expandidos += 1

        if no.estado == objetivo:
            return no, expandidos

        for acao, novo_estado in obter_sucessores(no.estado):
            novo_custo = no.custo + 1

            if novo_estado not in melhor_custo or novo_custo < melhor_custo[novo_estado]:
                melhor_custo[novo_estado] = novo_custo

                filho = No(
                    estado=novo_estado,
                    pai=no,
                    acao=acao,
                    custo=novo_custo,
                    profundidade=no.profundidade + 1
                )

                # f(n) = g(n) + h(n)
                h = manhattan(novo_estado, objetivo)
                f = novo_custo + h

                heapq.heappush(fronteira, (f, next(CONTADOR), filho))

    return None, expandidos


# ============================================================
# MENU PRINCIPAL
# ============================================================

def escolher_algoritmo():
    # Menu simples para selecionar o algoritmo.
    print("\nAlgoritmos disponíveis:")
    print("1 - BFS / Busca em Largura")
    print("2 - DFS / Busca em Profundidade")
    print("3 - Greedy / Busca Gulosa")
    print("4 - A*")
    print("5 - Custo Uniforme")

    while True:
        opcao = input("Escolha o algoritmo: ").strip()

        if opcao in {"1", "2", "3", "4", "5"}:
            return opcao

        print("Opção inválida.")


def main():
    # Fluxo principal: leitura dos estados, validacao,
    # escolha do algoritmo, execucao e impressao do caminho.
    print("=" * 60)
    print("8-PUZZLE - BUSCAS EM INTELIGÊNCIA ARTIFICIAL")
    print("=" * 60)

    # Entrada dos estados.
    estado_inicial = ler_estado("estado inicial")
    estado_objetivo = ler_estado("estado objetivo")

    print("\nEstado inicial:")
    imprimir_estado(estado_inicial)

    print("Estado objetivo:")
    imprimir_estado(estado_objetivo)

    # Verifica se a configuracao e solucionavel.
    if not problema_tem_solucao(estado_inicial, estado_objetivo):
        print("Este problema não possui solução.")
        return

    opcao = escolher_algoritmo()

    usar_heuristica = False

    # Para Greedy e A*, pergunta se deve usar a heuristica.
    # Sem heuristica, esses metodos viram custo uniforme.
    if opcao in {"3", "4"}:
        resposta = input("Usar heurística Manhattan? [s/n]: ").strip().lower()

        if resposta == "s":
            usar_heuristica = True
        else:
            print("\nSem heurística. Executando Busca de Custo Uniforme.")
            opcao = "5"

    # Executa o algoritmo escolhido.
    if opcao == "1":
        nome = "BFS / Busca em Largura"
        solucao, expandidos = busca_largura(estado_inicial, estado_objetivo)

    elif opcao == "2":
        nome = "DFS / Busca em Profundidade"
        solucao, expandidos = busca_profundidade(estado_inicial, estado_objetivo)

    elif opcao == "3" and usar_heuristica:
        nome = "Greedy / Busca Gulosa com Manhattan"
        solucao, expandidos = busca_gulosa(estado_inicial, estado_objetivo)

    elif opcao == "4" and usar_heuristica:
        nome = "A* com Manhattan"
        solucao, expandidos = busca_a_estrela(estado_inicial, estado_objetivo)

    else:
        nome = "Busca de Custo Uniforme"
        solucao, expandidos = busca_custo_uniforme(estado_inicial, estado_objetivo)

    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    print(f"Algoritmo usado: {nome}")
    print(f"Nós expandidos: {expandidos}")

    # Se nao encontrou solucao, encerra.
    if solucao is None:
        print("Nenhuma solução encontrada.")
        return

    caminho = reconstruir_caminho(solucao)

    print(f"Custo da solução: {solucao.custo}")
    print(f"Profundidade da solução: {solucao.profundidade}")
    print(f"Quantidade de movimentos: {len(caminho) - 1}")

    print("\nCaminho encontrado:\n")

    for i, no in enumerate(caminho):
        if no.acao is None:
            print(f"Passo {i}: Estado inicial")
        else:
            print(f"Passo {i}: mover espaço vazio para {no.acao}")

        # g(n): custo acumulado desde o inicio.
        print(f"g(n) = {no.custo}")

        # h(n) e f(n) sao mostrados somente quando ha heuristica.
        if opcao in {"3", "4"}:
            h = manhattan(no.estado, estado_objetivo)
            print(f"h(n) = {h}")

            if opcao == "4":
                print(f"f(n) = g(n) + h(n) = {no.custo + h}")

        imprimir_estado(no.estado)


if __name__ == "__main__":
    main()