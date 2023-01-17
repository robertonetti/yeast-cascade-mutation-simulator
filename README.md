# Yeast-Cascade-Mutation-Simulator
Yeast-Cascade-Mutation-Simulator simulates the duplication of a yeast cell up to a selected number of generations. The duplication process is accompanied by a cascade effect of mutations leading to a broad genomic spectrum at the end of cell growth.
### Motivation:
A single DNA damage event, such as a chromosome breakage in mitosis can be the cause of many mutational processes that occur as a cascade over numerous cell divisions. In addition, the process known as “adaptation to DNA damage” allows cell division despite DNA damages, probably provoking genome instability.

This project is designed to emulate the genome instability results obtained in experiments. Specifically, a single Wild Type yeast cell first suffers irreparable artificial DNA damage and then, through adaptation, begins to divide, producing the cascade effect of mutations mentioned above.

<!---
The further goal of the project is to build an algorithm that can reconstruct the history of the cascade process from the genomic spectrum resulting from the experiments. The role of the simulator will be to provide insights into the development of the algorithm and to test its capabilities.
--->

## Table of Contents:
1. Requirements;
2. Installation;
3. Implementation;
    1. Node Class;
    2. Classes relative to the cell structure;
    3. Implementation of the Simulator;
    4. Utility Class;
4. Usage;
    1. Chromosome data format and reading from file;
    2. Node and Wild Type Cell;
    3. Step 1 - Simulation;
    4. Step 2 - Reconstruction;
    5. Step 3 - Visualization;
    6. Usage of Utility Class;
5. Notebooks;
6. Roadmap.

## 1. Requirements:
This project requires the following libraries:
- Numpy (https://numpy.org);
- copy (https://docs.python.org/3/library/copy.html);
- matplotlib.pyplot (https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html);
- subprocess (https://docs.python.org/3/library/subprocess.html).

## 2. Installation:
To run the project, simply download the **code** folder. It contains all the necessary files.

## 3. Implementation:

### 3.1. Node Class:
The simulation is implemented on a binary tree structure, where each node stores one cell and all the related information. The node is defined as a class (**Node**) which has three attributes: **left_child**, **right_child** and **data** (see Binary Tree.py). 
To the **left_child** and **right_child** attributes are assigned one node respectively, and represent the two children nodes of the parent node. The last attribute **data**, contains the corresponding cell.
From the parent node (containing the initial Wild Type cell), all other nodes in the tree can be accessed (see **3.2. Usage**).

### 3.2. Classes relative to the cell structure:
In this section I will very quickly explain the structure of the various classes in the project used to collect the information contained in each cell.
The fundamental class is **Cell** which has two subclasses **WT_Cell** (Wild Type) and **MUT_Cell** (Mutated Cell). Both subclasses have an attribute called **DNA**, which is a class in turn containing a list of the different **Chromosomes**.
In addition, only the **MUT_Cell** has as another attribute a list of **Event** representing the mutation events that happened to the respective cell in its cycle. The **Event** class has two subclasses, the first called **Mutation** is in turn subdivided into: **PointwiseDeletion**, **PointwiseInsertion** and **PointwiseReplacement**. These are mutational events involving a single DNA base.
The other subclass of **Event** is **Rarrangement**, which is divided into:
**Deletion**, **Insertion**, **Translocation**, **TranslocationReciprocation** and **Duplication**. They can involve many DNA bases and more than one chromosome.
#### Simulator & Utility classes:
![Simulator](images/Simulator.png)
#### Cells, DNA & events classes:
![Cells](images/Cells.png)
#### Binary tree classes:
![Nodes](images/Nodes.png)

### 3.3. Implementation of the Simulator:
The simulation is accessible through the **Simulator** class and is divided in the following way: \
**Step 1 (Simulation)**: effective simulation of the cell divisions; \
**Step 2 (Reconstruction)**: reconstruction of the mutated sequences of the last cell generation or the cell at the end of a selected pathway, starting from **Step 1**;
**Step 3 (Visualization)**: here we use the information collected during **Step 1**, to visualize (for each chromosome of the last generaiton of cells) the number of "cumulated mutations/rearrangements".\

#### 3.3.1. Step 1 (Simulation):
In this step we start initializing a Wild Type cell (**WT_Cell** class) and a node (**Node** class). After initializing the the cell according to the given parameters, we assign it to the node. The node will be the root of the binary tree. Next we simulate the cell division up to the selected number of generations. After each cell division we randomly extract the number of mutations/rearrangements (from a Poisson distribution as default) occurring in the two doughter cells. For each mutational event we then extract its type (according to some weights) among the possible: **Deletion**, **Insertion**, **Translocation**, **TranslocationReciprocation**, **Duplication**, **PointwiseDeletion**, **PointwiseInsertion** and **PointwiseReplacement**. The events will be stored in the attribute: **MUT_Cell.events**.
After **Step 1**, a binary tree is obtained that stores at each node the events that occurred in the corresponding cell between the previous and the next division.

#### 3.3.2. Step 2 (Reconstruction):
The purpose of **Step 2** is to use the event lists collected in **Step 1** to reconstruct the DNA sequences that actually have mutated (in the last generation of cells) from the Wild Type.
This process is carried out starting form the root node, using the contained WT cell to reconstruct the two daughters, and repeating the procedure up to the last generation of cell.

#### 3.3.3. Step 3 (Data Visualization):
The aim of **Step 3** is to give a representation of the number of "cumulated mutations/rearrangements" of each sequence. The process is carried out as in **Step 2** starting from the root and expanding up to the leaves. The data visualization consists of highlighting the positions of the resulting chromosomes that have undergone multiple rearrangements/mutations, as can be seen in the following image:

![Visualization](images/Visualization.png)

The implementation of this process is carried out in the following way. To each chromosome of the WT cell is assigned an array of zeros of the same length of its sequence (called **visual**). Following the hierarchy of the cell duplications, this array is modified in its length according to the occurred mutations/rearrangements, and in the in the positions where an event occured we increase by one the value of the entries.
We end up with an array for each chromosome, where the larger the value of the entry the higher the number of events cumulated in that position.

### 3.4. Utility class:
The class **Utility** contains different methods necessary for both simulation and testing: methods that communicate with zsh for RAM usage, probability distributions methods, for WT sequences initialization and to read from file.

## 4. Usage:

### 4.1. Chromosome data format and reading from file:
The simulator takes as imput the WT chromosome sequences in the following format called **chromosome table**: 
a list of sequences of tuples, ordered from the first chromosome to the last one. Each tuple is composed by two entries: (chromosome ID: int, DNA sequence: str). 

#### 4.1.1. Reading from file:
It is possible to give the simulator the **chromosome_table** from outside reading from an external file. The file (**chromosome_list.txt**) should be a txt file that contains one DNA sequence of the corresponding chromosome for each raw.

##### Example (reading from file):
```python 
import sys
sys.path.insert(1, '../code') 
from Utility import Utility
# reading the "chromosme_list.txt" file and initializing the chromosome_table"
chromosome_table = Utility.read_file()
```

#### 4.1.2. Initialize chromosome table with random sequences:
If the chromosome sequences are not given from an external file, it is possible to define them randomly through the function **Utility.random_seq_initializer**. This function returns a random chromosome_table given the an array of the sequence length of each chromosome.
```python 
import sys
sys.path.insert(1, '../code') 
from Utility import Utility

chromosome_lengths = [int(5e4), int(45e4), int(4e4)] # lengths of the chromosome sequences (ordered)
chromosome_table = Utility.random_seq_initializer(chromosome_lengths) 
```

### 4.2. Node and Wild Type Cell:
The structure of the binary tree is due to the definition of the class **Node**, and the fact that each node has two doughter nodes as attributes. The third attribute (**data**) contains the respective cell. 

##### Example (Node and WT cell):
In this example we first initialize the **Node** object 'parent'. Then we define its attributes as two other **Node** objects, and assign a WT cell to the attribute **data**.

```python 
import sys
sys.path.insert(1, '../code') 
from Binary Tree import Node
from Utility import Utility
from WTCell import WT_Cell

parent = Node() #define the parent node
parent.left, parent.right = Node(), Node() #define the doughter nodes
# Initialize WT cell and assign it to 'parent.data'
chromosome_table = Utility.read_file()
parent.data = WT_Cell(chromosome_table)
```

### 4.3. Step 1 - Simulation:
The **Step 1** of the simulation is launched when defining an object of the class **Simulation**. This object will contain many attributes, among which the root node of the binary tree, from which the all tree is accessible.

##### Example (Step 1 - Simulation):
In this example we consider a WT cell with two chromosomes and a two-generation simulation. Once the object of the **Simulation** class has been initialized, we show how to access to the simulated binary tree.
```python 
import sys
sys.path.insert(1, '../code') 
from Simulator import Simulator
from Utility import Utility

# number of generations to be simulated
number_of_generations = 2 

# randomly initialize the chromosomes and their sequences
chromosome_lengths = [int(5e4), int(6e4)] # list containing the lengths of the chromosomes
chromosome_table = Utility.random_seq_initializer(chromosome_lengths) #creates a list containing one tuple (ID, sequence) for each chromosome

# Step 1 (Simulation)
simul = Simulator(chromosome_table, number_of_generations, visual=False)
# access the parent node and all nodes in the tree
print(simul.parent.data) # WT cell
print(simul.parent.left) # left daughter of the first generation
print(simul.parent.left.right) # and so on ...
```
### 4.4. Step 2 - Reconstruction:
Once the **Simulation** object has been initialized, the result is a binary tree containing for each node a cell and the list of mutations/rearrangements occured in its cycle. The actual DNA sequence is still not visible. In order to se the actual mutated sequence it is necessary to run the "reconstruction process". The output of the process is to add the mutated sequence on the last generation of cells. These cells are then accessible from the attribute **Simulation.leaves**.

##### Example 1 (Complete Reconstruction):
The following example shows how all cells of the last generation are reconstructed.
```python 
import sys
sys.path.insert(1, '../code') 
from Simulator import Simulator
from Utility import Utility

# Step 1 (Simulation)
number_of_generations = 2 
chromosome_lengths = [int(20), int(20)] 
chromosome_table = Utility.random_seq_initializer(chromosome_lengths)
simul = Simulator(chromosome_table, number_of_generations)

# Step 2 (Reconstruction)
simul.run_reconstruction(simul.parent, number_of_generations) # reconstructs last generation
print(f"CHR1,  WT: {chromosome_table[0][1]}")
print(f"CHR1, MUT: {simul.parent.left.right.data.DNA.CHRs[0].sequence}")
```

Instead of the complete reconstruction, it is possible to only reconstruct the sequence corresponding to a selected path in the cell duplication process. The result is the reconstruction of only the mutated sequence of the leaf of the selected path. 

##### Example 2 (Path Reconstruction):
In this example, only the leaf corresponding to the given path was reconstructed. Note that in the path: \
0 = left doughter \
1 = right doughter 

```python 
import sys
sys.path.insert(1, '../code') 
from Simulator import Simulator
from Utility import Utility

# Step 1 (Simulation)
number_of_generations = 2 
chromosome_lengths = [int(20), int(20)] 
chromosome_table = Utility.random_seq_initializer(chromosome_lengths)
simul = Simulator(chromosome_table, number_of_generations)

# Step 2 (Path Reconstruction)
path = [0, 1] # select the path
leaf = simul.path_reconstructor(path) #reconstruction of the leaf corresponding to the selected path
print(f"CHR1,  WT: {chromosome_table[0][1]}")
print(f"CHR1, leaf: {leaf.data.DNA.CHRs[0].sequence}")
```

### 4.4. Step 3 - Visualization:
As in **Step 2**, after the initialization of the **Simulation** object the **visual** arrays are empty. In order to see them it is necessary to run the "visualization process". The output of the process is to add the **visual** arrays to the last generation of cells. These cells are then accessible from the attribute **Simulation.leaves**.

##### Example (Visualization):
The following example shows how to run the 'visualization process'.
```python 
import sys
sys.path.insert(1, '../code') 
from Simulator import Simulator
from Utility import Utility

# Step 1 (Simulation)
number_of_generations = 5
chromosome_lengths = [int(20), int(20)] 
chromosome_table = Utility.random_seq_initializer(chromosome_lengths)
simul = Simulator(chromosome_table, number_of_generations)

# Step 2 (Visualization)
simul.run_visualization(simul.parent, number_of_generations)
print(f"last generation - CHR1 - visual: {simul.leaves[0].DNA.CHRs[0].visual}")
```

### 3.5. Parameters of the Simulator:
 - **chromosome_table**: List of chromosome sequences with their respective chromosome ID. Each element in the list is a tuple;
 - **number_of_generations**: represents the number of generations you want to simulate in **Step 1**;
 - **average_events_number**: average number of events occurring in a cell during duplication;
 - **cumulative_list**: list containing the values of the cumulative distribution of the event type;
 - **n_events_distrib**: probability distribution of the number of events (default: Poisson distribution);
 - **del_len_distrib**: probability distribution of the Deletion length;
 - **ins_len_distrib**: probability distribution of the Insertion length;
 - **transl_len_distrib**: probability distribution of the Translocation length;
 - **rec_transl_len_distrib**: probability distribution of the Reciprocal Translocation length;
 - **dupl_len_distrib**: probability distribution of the Duplication length;

**Note**: the probability distributions of the Rearrangements length can be chosen between: **discrete truncated uniform** and **discrete truncated exponential**. In the last case it is possible to choose the parameter $\tau$ of the truncated exponential distribution:\
$p(n) = \frac{1}{Z} \cdot e^{-\frac{n}{\tau}}$  where  $Z = e^{-\frac{a}{\tau}} - e^{-\frac{b}{\tau}}$. Truncated in the interval $[a,b]$.
 
 In case the **chromosome_table** is not given (see "Utility Class"):
 - **chromosome_lengths**: ordered list containing the lengths of the chromosomes considered;
 - **chromosome_number**: total number of chromosomes considered;

### 3.6. Usage of Utility Class:
Utility is a class that contains several useful methods: some for testing process RAM usage, others that define probability distributions, and still others that help build a random **chromosome_table** (see "Parameters").

### 3.6.1. Methods for RAM usage:
These methods are useful for calculating RAM usage during simulation. It is important to note that they were written to communicate with macOS zsh and to identify the process ID (pid) of "python3.8". They can be easily adapted for use with another operating system and another version of python.

### 3.6.2. Probability Distributions Methods:
These methods implement probability distributions and can be passed as a parameter to the simulation. The first two (**int_trunc_exp**, **int_trunc_uniform**) use the inverse cumulative method to draw the number of events from truncated distributions, while the last one draws the number of events from a Poisson distribution.

### 3.6.3. Methods for Chromosome Sequences Initialization:
The role of these methods is to create a random **chromosomal_table** (see Parameters) when it cannot be given from outside.



## Roadmap:
- [x] documentation;
- [x] github repository;
- [x] RAM usage test;
- [x] elapsed time test;
- [x] data and results representation;
- [ ] test of the regimes for different parameters;
- [ ] application to real yeast cells.


# TO DO: 
- [x] create a different function for visualization;
- [x] update documentation of Simulator to consider the previous point;
- [x] check the functions that compute stats for cumulated mutation;
- [x] update documentation of Simulator to consider the previous point;
- [x] check if you can remove the parameter "chromosome_table" when calling "reconstructor()";
- [x] create program to read from file;
- [x] create folder for Jupyter notebooks;
- [x] eliminate repeated attributes in class diagrams;
- [ ] substutute left and right with left_child & right_child in the code;
- [ ] rename the Binary Tree file as BinaryTree;
- [ ] create chapter "Usage" with all the examples;
- [ ] create chapter "Implementation" with class structure, implementation of the Simulator etc.. ;
- [ ] create chapter "Visualization";
