# Heuristic Search Lab

Implementação em Python de algoritmos de busca não informada e informada aplicados ao **Mapa da Romênia** e ao **8-puzzle**.

O programa possui entrada interativa pelo terminal: o professor pode escolher o problema, digitar estado inicial/objetivo e escolher o algoritmo.

## Algoritmos implementados

### Busca não informada

- BFS / Busca em Largura
- DFS / Busca em Profundidade, com limite configurável
- Busca de Custo Uniforme

### Busca informada

- Greedy / Busca Gulosa
- A*

## Problemas implementados

### Mapa da Romênia

O mapa está representado como grafo ponderado. Cada cidade é um estado e cada estrada é uma transição com custo em quilômetros.

A heurística usada para Greedy e A* é a distância em linha reta até Bucharest, conforme o exemplo clássico da disciplina.

Observação: se o objetivo digitado não for Bucharest, a heurística retorna `0`, para manter a correção do algoritmo. Nesse caso, A* se comporta como Busca de Custo Uniforme.

### 8-puzzle

O espaço vazio é representado por `0` ou `_`.

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

Heurísticas disponíveis:

- peças fora do lugar;
- distância Manhattan;
- heurística zero.

## Como executar

No diretório do projeto:

```bash
python main.py
```

Menu principal:

```text
1 - Resolver Mapa da Romênia
2 - Resolver 8-Puzzle
3 - Rodar demonstração rápida
0 - Sair
```

## Exemplo: Mapa da Romênia

Entrada:

```text
Escolha uma opção: 1
Cidade inicial [Arad]: Arad
Cidade objetivo [Bucharest]: Bucharest
Escolha o algoritmo: 5
```

Saída esperada para A*:

```text
Caminho: Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
Custo total: 418
```

## Exemplo: 8-puzzle

Entrada:

```text
Escolha uma opção: 2
Estado inicial: 1 2 3 4 5 0 6 7 8
Estado objetivo [1 2 3 4 0 5 6 7 8]: 1 2 3 4 0 5 6 7 8
Heurística: 2
Algoritmo: 5
```

O programa aceita também:

```text
123450678
1,2,3,4,5,0,6,7,8
1 2 3 4 5 _ 6 7 8
```

## Métricas exibidas

Para cada execução, o programa mostra:

- caminho solução;
- custo total;
- profundidade / número de passos;
- nós expandidos;
- tamanho máximo da fronteira;
- tempo de execução;
- ordem de expansão dos estados.

## Estrutura

```text
heuristic-search-lab/
├── main.py
├── requirements.txt
├── src/
│   ├── algorithms/
│   │   ├── informed.py
│   │   ├── uniform_cost.py
│   │   └── uninformed.py
│   ├── graphs/
│   │   └── romania_map.py
│   ├── puzzles/
│   │   └── eight_puzzle.py
│   └── utils/
│       ├── node.py
│       └── search_result.py
└── README.md
```

## Autor

Felipe Echeverria Vilhalva
