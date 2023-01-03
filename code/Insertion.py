from code.Rearrangement import Rearrangement
from code.BinaryTree import Node
import numpy as np

class Insertion(Rearrangement):
    """
    Insertion Class (subclass of Rearrangement)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: 'Insertion'.
    ChrID: int
        ID of the chromosome involved.
    Pos: int
        Initial position of the inserted sequence.
    Length: int
        Length of the inserted sequence.

    Methods
    -------
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Insertion, of the considered
        cell.
    """
    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current Insertion, in the considered
        cell. It takes the old sequence, and modifies it in order to add the Insertion.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, init_pos, new_seq = self.ChrID, self.Pos, ''.join(np.random.choice(["A","G","C","T"],\
                                 self.Length))
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : init_pos] \
                                 + new_seq + node.data.DNA.CHRs[chrID - 1].sequence[init_pos : ]

    def __init__(self, ChrID :int, Pos :int, Length :int, cell = None):
        """
        It defines the 'SubKind', and initializes 'ChrID', 'Pos' and 'Length' according to the given
        parameters.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): Initial position of the inserted sequence.
            Length (int): Length of the inserted sequence.
        """
        super().__init__()
        self.SubKind = "Insertion"
        self.ChrID = ChrID
        self.Pos = Pos
        self.Length = Length
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrID - 1].length += self.Length
    
    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, Pos: {self.Pos!r}, Length: {self.Length!r})"

    def __str__(self):
        return f"Event->{self.kind} ->{self.SubKind}(ChrId: {self.ChrID}, Pos: {self.Pos}, Length: {self.Length})"
