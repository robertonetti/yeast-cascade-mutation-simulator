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
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Insertion, of the considered
        cell.
    """
    def update_visual(self, node: Node):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involeved in the Deletion.
        """
        chr = node.data.DNA.CHRs[self.ChrID - 1]
        inserted = np.zeros(self.Length) + 1
        new_vis = np.concatenate((chr.visual[: self.Pos], inserted, chr.visual[self.Pos :]))
        #if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")
        chr.visual = new_vis

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
        parameters. In the end updates the 'visual' array.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): Initial position of the inserted sequence.
            Length (int): Length of the inserted sequence.
            cell (Cell): Cell involved in the Insertion.
            visual (bool): True if the visualizaiton is active. False if not.
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
