# Heuristic Search Lab

Implementação em Python de algoritmos de busca não informada e informada aplicados ao **8-puzzle**.

O programa é interativo via terminal: o usuário informa o estado inicial e o objetivo e escolhe o algoritmo.

## Algoritmos implementados

### Busca não informada

- BFS / Busca em Largura
- DFS / Busca em Profundidade (limite padrão: 30)
- Busca de Custo Uniforme

### Busca informada

- Greedy / Busca Gulosa
- A* (com heurística Manhattan)

## 8-puzzle

O espaço vazio é representado por `0`.

Exemplo:

```text
1 2 3
4 0 5
6 7 8
```

O programa valida:

- se há exatamente 9 posições;
- se os números de 0 a 8 aparecem uma única vez;
- se o estado inicial é solucionável para o objetivo informado.

Heurística disponível:

- distância Manhattan (usada por Greedy e A*).

Se o usuário escolher Greedy ou A*, é perguntado se a heurística Manhattan deve ser usada. Se a resposta for "n", o programa executa Busca de Custo Uniforme.

## Como executar

No diretório do projeto:

```bash
python main.py
```

## Exemplo de uso

Entrada:

```text
estado inicial: 1 2 3 4 5 0 6 7 8
estado objetivo: 1 2 3 4 0 5 6 7 8
Escolha o algoritmo: 4
Usar heurística Manhattan? [s/n]: s
```

## Métricas exibidas

Para cada execução, o programa mostra:

- caminho solução (passo a passo);
- custo total da solução;
- profundidade / quantidade de movimentos;
- nós expandidos;
- g(n) para cada estado do caminho;
- h(n) para Greedy e A*;
- f(n) para A*.

## Estrutura

```text
heuristic-search-lab/
├── LICENSE
├── main.py
└── README.md
```

## Autor

Felipe Echeverria Vilhalva
