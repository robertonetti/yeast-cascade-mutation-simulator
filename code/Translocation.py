from Rearrangement import Rearrangement
from BinaryTree import Node
import numpy as np 

class Translocation(Rearrangement):
    """
    Translocation Class (subclass of Rearrangement)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: Translocation
    ChrID: int
        ID of the chromosome involved.
    InitPos: int
        Initial position of the translocated sequence, before translocation.
    Length: int
        Length of the translocated sequence.
    FinalPos: int
        Initial position of the translocated sequence, after translocation.

    Methods
    -------
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Translocation, of the considered
        cell.
    """

    def update_visual(self, node: Node):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involved in the Deletion.
        """
        chr = node.data.DNA.CHRs[self.ChrID - 1]
        translocated = chr.visual[self.InitPos : self.InitPos + self.Length] + 1
        new_vis = np.concatenate((chr.visual[: self.InitPos], chr.visual[self.InitPos + self.Length :]))
        new_vis = np.concatenate((new_vis[: self.FinalPos], translocated, new_vis[self.FinalPos :]))
        #if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")
        if self.InitPos - 1 >= 0: new_vis[self.InitPos - 1] += 1
        if self.InitPos  < len(new_vis): new_vis[self.InitPos] += 1
        chr.visual = new_vis
    
    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current Translocation, in the considered
        cell. It takes the old sequence, and modifies it in order to add the Translocation.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, init_pos, end_pos, final_pos = self.ChrID, self.InitPos, self.InitPos + self.Length, self.FinalPos
        transl_seq = node.data.DNA.CHRs[chrID - 1].sequence[init_pos : end_pos]
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : init_pos] +  node.data.DNA.CHRs[chrID - 1].sequence[end_pos : ]
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : final_pos] + transl_seq + node.data.DNA.CHRs[chrID - 1].sequence[final_pos : ]

    def __init__(self, ChrID :int, InitPos :int, Length :int, FinalPos :int, cell = None):
        """
        Defines the SubKind, and initializes ChrID, InitPos, Length, FinalPos according to the given
        parameters. In the end updates the 'visual' array.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            InitPos (int): Initial position of the translocated sequence, before translocation.
            Length (int): Length of the translocated sequence.
            FinalPos (int): Initial position of the translocated sequence, after translocation.
            cell (Cell): Cell involved in the Deletion.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        super().__init__()
        self.SubKind = "Translocation"
        self.ChrID = ChrID
        self.InitPos = InitPos
        self.Length = Length
        self.FinalPos = FinalPos
        if cell != None:
            cell.events.append(self)
    
    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, InitPos: {self.InitPos!r}, Length: {self.Length!r}, FinalPos: {self.FinalPos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, InitPos: {self.InitPos}, Length: {self.Length}, FinalPos: {self.FinalPos})"