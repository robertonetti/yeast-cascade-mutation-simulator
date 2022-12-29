
from Rearrangement import Rearrangement
from BinaryTree import Node

class Translocation(Rearrangement):
    """
    Translocation Class (subclass of Rearrangement)

    Attributes:
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

    Methods:
    -------
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Translocation, of the considered
        cell.
    """
    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current Translocation, in the considered
        cell. It takes the old sequence, and modifies it in order to add the Translocation.

        Parameters:
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
        parameters.

        Parameters:
        ----------
            ChrID (int): ID of the chromosome involved.
            InitPos (int): Initial position of the translocated sequence, before translocation.
            Length (int): Length of the translocated sequence.
            FinalPos (int): Initial position of the translocated sequence, after translocation.
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