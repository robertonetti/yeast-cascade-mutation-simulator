from code.Mutation import Mutation
from code.BinaryTree import Node
import numpy as np

class PointReplacement(Mutation):
    """
    Pontwise Replacement Class (subclass of Mutation)

    Attributes
    SubKind: str
        Subkind of Rearrangement. In this case: Pointwise Replacement
    ChrID: int
        ID of the chromosome involved.
    Pos: int
        Position of the replaced DNA base.

    Methods
    -------
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current PointwiseReplacement, of the 
        considered cell.
    """
    def update_visual(self, node: Node):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involved in the Deletion.
        """
        chr = node.data.DNA.CHRs[self.ChrID - 1]
        chr.visual[self.Pos] += 1

    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current PointwiseReplacement, in the 
        considered cell. It takes the old sequence, and modifies it in order to add the
        PointwiseReplacement.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, repl_pos = self.ChrID, self.Pos
        old_base = str(node.data.DNA.CHRs[chrID - 1].sequence[repl_pos])
        bases = ["A","G","C","T"]
        bases.remove(old_base)
        new_base = np.random.choice(bases)
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : repl_pos] + new_base + node.data.DNA.CHRs[chrID - 1].sequence[repl_pos + 1 : ]
    
    def __init__(self, ChrID :int, Pos :int, cell = None):
        """
        It defines the 'SubKind', and initializes 'ChrID' and 'Pos' according to the given 
        parameters. In the end updates the 'visual' array.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): position of the replaced DNA base.
            cell (Cell): Cell involved in the Deletion.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        super().__init__()
        self.SubKind = "Pointwise Replacement"
        self.ChrID = ChrID
        self.Pos = Pos
        if cell != None:
            cell.events.append(self)
            

    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, Pos: {self.Pos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, Pos: {self.Pos})"