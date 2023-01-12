from code.Rearrangement import Rearrangement
from code.BinaryTree import Node
from scipy.sparse import *
import numpy as np

class Duplication(Rearrangement):
    """
    Duplication Class (subclass of Rearrangement)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: 'Duplication'
    ChrID: int
        ID of the chromosome involved.
    InitPos: int
        Initial position of the duplicated sequence, before duplication.
    Length: int
        Length of the duplicated sequence.
    FinalPos: int
        Initial position of the inserted sequence, after duplication.

    Methods
    -------
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Duplication, of the considered
        cell.
    """
    def update_visual(self, chr):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involeved in the Deletion.
        """
        duplicated = chr.visual[self.InitPos : self.InitPos + self.Length] + 1
        new_vis = np.concatenate((chr.visual[: self.FinalPos], duplicated, chr.visual[self.FinalPos :]))
        if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")
        chr.visual = new_vis

    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current Duplication, in the considered
        cell. It takes the old sequence, and modifies it in order to add the Duplication.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, init_pos, end_pos, final_pos = self.ChrID, self.InitPos, self.InitPos + self.Length,\
                                              self.FinalPos
        dupl_seq = node.data.DNA.CHRs[chrID - 1].sequence[init_pos : end_pos]
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : final_pos]  \
            + dupl_seq + node.data.DNA.CHRs[chrID - 1].sequence[final_pos : ]
    
    def __init__(self, ChrID :int, InitPos :int, Length :int, FinalPos :int, cell = None, visual = False):
        """
        It defines the 'SubKind', and initializes 'ChrID', 'InitPos', 'Length', 'FinalPos' according 
        to the given parameters.  In the end updates the 'visual' array.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            InitPos (int): Initial position of the duplicated sequence, before duplication.
            Length (int): Length of the duplicated sequence.
            FinalPos (int): Initial position of the copied sequence, after duplication.
            cell (Cell): Cell involved in the Duplication.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        super().__init__()
        self.SubKind = "Duplication"
        self.ChrID = ChrID
        self.InitPos = InitPos
        self.Length = Length
        self.FinalPos = FinalPos
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrID - 1].length += self.Length
            if visual == True : self.update_visual(cell.DNA.CHRs[ChrID - 1])

    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, InitPos: {self.InitPos!r}, Length: {self.Length!r}, FinalPos: {self.FinalPos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, InitPos: {self.InitPos}, Length: {self.Length}, FinalPos: {self.FinalPos})"
