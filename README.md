# Heuristic Search Lab

Implementação de algoritmos de busca não informada e informada aplicados a problemas clássicos de IA, como o 8-puzzle e o mapa da Romênia.

## 📋 Descrição

Este projeto implementa diversos algoritmos de busca em espaço de estados para resolver problemas clássicos de Inteligência Artificial:

- **Algoritmos não informados**: BFS (Busca em Largura), DFS (Busca em Profundidade)
- **Algoritmos informados**: Busca de Custo Uniforme, Busca Gulosa (Greedy), A*
- **Problemas**: 8-Puzzle, Mapa da Romênia

## 🛠️ Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 📦 Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd heuristic-search-lab

# (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências (se houver)
pip install -r requirements.txt
```

## 🚀 Como Usar

```bash
# Execute um exemplo específico
python main.py

# Ou execute um módulo específico
python -m src.puzzles.eight_puzzle
python -m src.graphs.romania_map
```

## 📁 Estrutura do Projeto

```
heuristic-search-lab/
├── src/
│   ├── algorithms/           # Implementação dos algoritmos de busca
│   │   ├── uninformed.py     # BFS, DFS
│   │   ├── informed.py       # Greedy, A*
│   │   └── uniform_cost.py   # Busca de Custo Uniforme
│   ├── puzzles/
│   │   └── eight_puzzle.py   # Implementação do 8-Puzzle
│   ├── graphs/
│   │   └── romania_map.py    # Implementação do Mapa da Romênia
│   └── utils/
│       └── node.py           # Classe Node para representação de estados
├── tests/                    # Testes unitários
├── main.py                   # Script de execução principal
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

## 🎯 Algoritmos Implementados

### Busca Não Informada

- **BFS (Breadth-First Search)**: Expande nós por nível, garantindo a solução mais curta
- **DFS (Depth-First Search)**: Expande nós em profundidade, útil para problemas com espaço de estados limitado

### Busca Informada

- **Busca de Custo Uniforme**: Expande nós com menor custo acumulado
- **Busca Gulosa**: Utiliza heurística para expandir nó mais próximo do objetivo
- **A***: Combina custo real com heurística, garantindo solução ótima

## 🧩 Problemas Abordados

### 8-Puzzle
Puzzle deslizante 3x3 onde o objetivo é organizar os números de 1 a 8 em ordem crescente.

```
1 2 3
4 5 6
7 8 _
```

### Mapa da Romênia
Problema de planejamento de rota onde o objetivo é encontrar o caminho mais curto entre duas cidades.

## 📊 Exemplo de Uso

```python
from src.algorithms.uninformed import BFS
from src.puzzles.eight_puzzle import EightPuzzle

# Criar instância do puzzle
puzzle = EightPuzzle(initial_state=..., goal_state=...)

# Executar busca BFS
search = BFS()
solution = search.solve(puzzle)

print(f"Caminho para solução: {solution.path}")
print(f"Nós expandidos: {solution.expanded_nodes}")
print(f"Profundidade: {solution.depth}")
```

## 📈 Comparação de Algoritmos

O projeto permite comparar a performance de diferentes algoritmos:
- Número de nós expandidos
- Profundidade da solução
- Tempo de execução
- Custo da solução (se aplicável)

## 🤝 Contribuições

Este é um projeto educacional. Sinta-se livre para melhorar a implementação ou adicionar novos algoritmos/problemas.

## 📝 Licença

MIT

## 👨‍💻 Autor

Felipe Echeverria Vilhalva

## 📞 Contato
https://www.linkedin.com/in/felipevilhalva/
