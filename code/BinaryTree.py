import copy 

class Node():
    """
    Class of the Node of a Binary Tree. By defining the node with a left attribute and a right 
    attribute (which are nodes in turn) it is possible to access the entire Binary Tree of which the
    current node is the root. 

    Attributes
    ----------
    data: Cell 
        It is the content of the node. In this case a cell.
    generation: int
        It is the number corresponding to the generation of the node.
    left_child: Node
        Left doughter node of the current node.
    right_child: Node
        Right doughter node of the current node.

    Methods
    -------
    copy_chr_sequences(self, parent)
        Copies the DNA sequences of the cell contained in the parent node and adds them to the cell
        contained in the doughter node.
    """
    def copy_chr_sequences(self, parent):
        """
        Copies the DNA sequences of the parent cell, in the current doughter node.

        Paremeters
        ----------
            parent (Node): parent node from which the DNA sequences are copied.
        """
        n_seqs = len(parent.data.DNA.CHRs)
        for i in range(n_seqs):
            self.data.DNA.CHRs[i].sequence = copy.deepcopy(parent.data.DNA.CHRs[i].sequence)
            
    def __init__(self, data = None, generation = 0):
        """
        It initializes the 'data' and 'generation' according to the given parameters.

        Parameters:
        ----------
            data (Cell): it is the content of the node: in this case a Cell.
                         (default: None)
            generation (int): it is the number corresponding to the generation of the node. 
                              (default: 0)
        """
        self.data = data
        self.generation = generation

    left_child = None
    right_child = None
    
    def __repr__(self):
        return f"{self.data}\n      --- {type(self.right_child)}\n      --- {type(self.left_child)}"

    def __str__(self):
        return f"{self.data}\n      --- {type(self.right_child)}\n      --- {type(self.left_child)}"
