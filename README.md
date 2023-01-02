# Yeast-Cascade-Mutation-Simulator
Yeast-Cascade-Mutation-Simulator simulates the duplication of a yeast cell up to a selected number of generations. The duplication process is accompanied by a cascade effect of mutations leading to a broad genomic spectrum at the end of cell growth.
### Motivation:
A single DNA damage event, such as a chromosome breakage in mitosis can be the cause of many mutational processes that occur as a cascade over numerous cell divisions. In addition, the process known as “adaptation to DNA damage” allows cell division despite DNA damages, probably provoking genome instability.

This project is designed to emulate the genome instability results obtained in experiments. Specifically, a single Wild Type yeast cell first suffers irreparable artificial DNA damage and then, through adaptation, begins to divide, producing the cascade effect of mutations mentioned above.

The further goal of the project is to build an algorithm that can reconstruct the history of the cascade process from the genomic spectrum resulting from the experiments. The role of the simulator will be to provide insights into the development of the algorithm and to test its capabilities.

## Table of Contents:
- Requirements;
- Installation;
- Usage;

## Requirements:
This project requires the following libraries:
- Numpy (https://numpy.org);
- copy (https://docs.python.org/3/library/copy.html);

## Installation:
To run the project is sufficient to download all the files and put them togheter in the same folder.

## Usage:
### Data Structure:
The core structure of the simulation is composed by a binary tree. Each object **node** in the tree is thought as a class containing three attributes: **node.left**, **node.right** and **node.data** (see Binary Tree.py). The first and the second attribute are node themselves and represent the two doughter nodes of the parent one. The last attribute **node.data**, contains the corresponding cell.\
From the parent node (containing the initial Wild Type cell) is possible to access all the other nodes in the tree.
#### Example:
```python 
from Binary Tree import Node

parent = Node() #define the parent node
parent.left, parent.right = Node(), Node() #define the doughter nodes
```

### Classes Structure:

### Structure of the simulator:
The simulation is divided in two main steps: \
**Step 1**: effective simulation of the cell divisions; \
**Step 2**: reconstruction of the mutated sequences of the last generation of cells.
