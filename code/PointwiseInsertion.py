from code.Mutation import Mutation
from code.BinaryTree import Node
import numpy as np

class PointInsertion(Mutation):
    """
    Pontwise Insertion Class (subclass of Mutation)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: Pointwise Insertion
    ChrID: int
        ID of the chromosome involved.
    Pos: int
        Position of the inserted DNA base.

    Methods
    -------
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current PointwiseInsertion, of the 
        considered cell.
    """


    def update_visual(self, chr):
        inserted = np.array([1])
        new_vis = np.concatenate((chr.visual[: self.Pos], inserted, chr.visual[self.Pos :]))
        if len(new_vis) != chr.length: raise Exception(f"P.Insertion: visual {len(new_vis)}, chr {chr.length}")
        
        chr.visual = new_vis










    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current PointwiseInsertion, in the 
        considered cell. It takes the old sequence, and modifies it in order to add the
        PointwiseInsertion.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, ins_pos = self.ChrID, self.Pos
        ins_base = np.random.choice(["A","G","C","T"])
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : ins_pos] + ins_base + node.data.DNA.CHRs[chrID - 1].sequence[ins_pos : ]

    def __init__(self, ChrID :int, Pos :int, cell = None):
        """
        Defines the 'SubKind', and initializes 'ChrID' and 'Pos' according to the given parameters.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): position of the inserted DNA base.
        """
        super().__init__()
        self.SubKind = "Pointwise Insertion"
        self.ChrID = ChrID
        self.Pos = Pos
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrID - 1].length += 1
            self.update_visual(cell.DNA.CHRs[ChrID - 1])

    
    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, Pos: {self.Pos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, Pos: {self.Pos})"
