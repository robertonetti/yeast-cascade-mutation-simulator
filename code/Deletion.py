from code.Rearrangement import Rearrangement
from code.BinaryTree import Node
import numpy as np


class Deletion(Rearrangement):
    """
    Deletion Class (subclass of Rearrangement)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: 'Deletion'.
    ChrID: int
        ID of the involved chromosome.
    Pos: int
        Initial position of the deleted sequence.
    Length: int
        Length of the deleted sequence.

    Methods
    -------
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current Deletion, of the considered
        cell.
    """
    def update_visual(self, node: Node):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involved in the Deletion.
        """
        chr = node.data.DNA.CHRS[self.ChrID - 1]
        new_vis = np.concatenate((chr.visual[: self.Pos], chr.visual[self.Pos + self.Length :]))
        if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")
        if self.Pos - 1 >= 0: 
            new_vis[self.Pos - 1] += 1
        if self.Pos  < len(new_vis): new_vis[self.Pos] += 1
        chr.visual = new_vis

    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current Deletion, in the considered
        cell. It takes the old sequence, and modifies it in order to add the Deletion.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, init_pos, final_pos = self.ChrID, self.Pos, self.Pos + self.Length
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : init_pos] +  node.data.DNA.CHRs[chrID - 1].sequence[final_pos : ]
    


    



    def __init__(self, ChrID :int, Pos :int, Length :int, cell = None):
        """
        Defines the 'SubKind', and initializes 'ChrID', 'Pos' and 'Length' according to the given
        parameters. In the end updates the 'visual' array and cheks if the chromosome is deleted.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): Initial position of the deleted sequence.
            Length (int): Length of the deleted sequence.
            cell (Cell): Cell involved in the Deletion.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        super().__init__()
        self.SubKind = "Deletion"
        self.ChrID = ChrID
        self.Pos = Pos
        self.Length = Length
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrID - 1].length -= self.Length
            if cell.DNA.CHRs[ChrID - 1].length == 0:
                cell.DNA.IDs.remove(ChrID)
                print(f"(generation: {cell.generation}) Chromosome {ChrID} has been removed! \n The event was a {self}.\n")
                
    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, Pos: {self.Pos!r}, Length: {self.Length!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, Pos: {self.Pos}, Length: {self.Length})"