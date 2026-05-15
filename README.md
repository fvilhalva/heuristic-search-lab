# Heuristic Search Lab

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-brightgreen)](#)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Implementação em Python de algoritmos de busca (informada e não informada) aplicados ao **8-puzzle**.

Este repositório contém uma versão educativa e interativa do 8-puzzle cujo objetivo é demonstrar e comparar o comportamento de diferentes algoritmos de busca: BFS, DFS, Busca de Custo Uniforme, Greedy e A* (com heurística Manhattan), além de uma versão IDA*.

**Principais características**

- Implementações didáticas dos algoritmos de busca mais comuns.
- Verificações de validade do problema (tamanho, elementos e paridade/inversões).
- Saída detalhada com métricas: custo, profundidade, nós expandidos, g(n), h(n) e f(n) quando aplicável.
- Interação via terminal para facilitar testes manuais.

## Algoritmos implementados

### Busca não informada

- BFS / Busca em Largura
- DFS / Busca em Profundidade (limite padrão configurável)
- Busca de Custo Uniforme

### Busca informada

- Greedy / Busca Gulosa (com heurística Manhattan)
- A* (com heurística Manhattan)
- IDA* (Iterative Deepening A*)

## Sobre o 8-puzzle

O espaço vazio é representado por `0`. Cada estado é uma tupla de 9 inteiros contendo exatamente os números de 0 a 8 sem repetição.

Exemplo de estado (formato interno, fila por linha):

```text
1 2 3
4 0 5
6 7 8
```

Validações realizadas pelo programa:

- Há exatamente 9 posições.
- Os números 0..8 aparecem exatamente uma vez.
- O estado inicial é solucionável a partir do estado objetivo (verificação por paridade de inversões).

Heurística disponível:

- Distância Manhattan (utilizada em Greedy, A* e IDA* como estimativa).

Observação: caso o usuário opte por Greedy ou A*, é possível optar por não usar a heurística; nesse caso a implementação recai em Busca de Custo Uniforme.

## Uso

1. Clone o repositório ou faça o download dos arquivos.
2. Execute no diretório do projeto:

```bash
python main.py
```

O programa é interativo e solicitará que você informe o `estado inicial` e o `estado objetivo` no formato de 9 números separados por espaço, usando `0` para o espaço vazio.

Exemplo de entrada interativa:

```text
estado inicial: 1 2 3 4 5 0 6 7 8
estado objetivo: 1 2 3 4 0 5 6 7 8
Escolha o algoritmo: 4
Usar heurística Manhattan? [s/n]: s
```

## Métricas e saída

Ao finalizar a busca, o programa exibe:

- Caminho solução (lista de estados passo a passo).
- Custo total da solução (`g(n)` do nó final).
- Profundidade / quantidade de movimentos.
- Número de nós expandidos durante a busca.
- Valores `g(n)` para cada estado do caminho.
- Valores `h(n)` para Greedy, A* e IDA* quando a heurística é usada.
- Valores `f(n) = g(n) + h(n)` para A*.

Essas métricas ajudam a comparar a eficiência dos algoritmos em termos de exploração de espaço e qualidade da solução.

## Estrutura do projeto

```text
heuristic-search-lab/
├── LICENSE
├── main.py        # Implementação principal e interface interativa
├── README.md      # Este arquivo
└── tests/         # Testes unitários para funções e algoritmos
	└── test_main.py
```

## Testes

Há um conjunto de testes unitários em `tests/test_main.py`. Para executá-los use:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam funções base (heurística, sucessores, validação de solubilidade), além de casos simples para as implementações dos algoritmos.

## Benchmark (exemplo rápido)

Se quiser comparar rapidamente o tempo de execução entre algoritmos em um caso simples, você pode usar `time` ou `python -m timeit`. Exemplo com `time` no Linux/macOS:

```bash
time python - <<'PY'
from time import perf_counter
import main

start = perf_counter()
main.busca_largura((1,2,3,4,5,6,7,0,8),(1,2,3,4,5,6,7,8,0))
end = perf_counter()
print('BFS time:', end - start)
PY
```

Para benchmarks mais consistentes crie um pequeno script `bench.py` que execute cada algoritmo várias vezes e calcule média e desvio padrão. Exemplo mínimo de comando:

```bash
python -m timeit -s "import main; A=(1,2,3,4,5,6,7,0,8); B=(1,2,3,4,5,6,7,8,0)" "main.busca_largura(A,B)"
```

Resultados dependem fortemente do estado testado e da máquina; use casos maiores e múltiplas repetições para avaliações significativas.

## Contribuição

Contribuições são bem-vindas. Para colaborar:

1. Abra uma issue descrevendo a sugestão ou bug.
2. Faça um fork e crie uma branch com a sua alteração.
3. Envie um pull request explicando as mudanças e incluindo testes quando apropriado.

Sugestões de melhorias:

- Implementar outras heurísticas (ex.: número de tiles fora de posição).
- Adicionar visualização passo a passo mais rica (ex.: saída gráfica ou web).
- Otimizações de desempenho e perfilamento.

## Licença

Este projeto está disponível sob a licença no arquivo `LICENSE`.

## Autor

Felipe Echeverria Vilhalva