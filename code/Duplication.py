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
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Duplication, of the considered
        cell.
    """

    def update_visual(self, chr):
        new_vis = chr.visual.todense().tolist()[0]
        duplicated = np.array(new_vis[self.InitPos : self.InitPos + self.Length]) + 1
        duplicated = duplicated.tolist()
        new_vis = new_vis[: self.FinalPos] + duplicated + new_vis[self.FinalPos :]
        if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")

        if self.InitPos - 1 >= 0: 
            print(f"InitPos: {self.InitPos}, len(new_vis): {len(new_vis)}")
            new_vis[self.InitPos - 1] += 1
        if self.InitPos  < len(new_vis): new_vis[self.InitPos] += 1
        chr.visual = lil_matrix(new_vis)






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
    
    def __init__(self, ChrID :int, InitPos :int, Length :int, FinalPos :int, cell = None):
        """
        It defines the 'SubKind', and initializes 'ChrID', 'InitPos', 'Length', 'FinalPos' according 
        to the given parameters.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            InitPos (int): Initial position of the duplicated sequence, before duplication.
            Length (int): Length of the duplicated sequence.
            FinalPos (int): Initial position of the copied sequence, after duplication.
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
            self.update_visual(cell.DNA.CHRs[ChrID - 1])

    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, InitPos: {self.InitPos!r}, Length: {self.Length!r}, FinalPos: {self.FinalPos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, InitPos: {self.InitPos}, Length: {self.Length}, FinalPos: {self.FinalPos})"
