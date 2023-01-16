from code.Mutation import Mutation
from code.BinaryTree import Node
import numpy as np

class PointDeletion(Mutation):
    """
    Pontwise Deletion Class (subclass of Mutation)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: Pointwise Deletion
    ChrID: int
        ID of the chromosome involved.
    Pos: int
        Position of the deleted DNA base.

    Methods
    -------
    update_visual(self, chr: Chromosome):
        Updates the "visual" array of the chromosome.
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current PointwiseDeletion, of the 
        considered cell.
    """

    def update_visual(self, node: Node):
        """
        Updates the "visual" array of the chromosome.

        Parameters
        ----------
            chr (Chromosome): chromosome involeved in the Deletion.
        """
        chr = node.data.DNA.CHRs[self.ChrID - 1]
        new_vis = np.concatenate((chr.visual[: self.Pos], chr.visual[self.Pos + 1 :]))
        #if len(new_vis) != chr.length: raise Exception(f"visual {len(new_vis)}, chr {chr.length}")
        if self.Pos - 1 >= 0: 
            new_vis[self.Pos - 1] += 1
        if self.Pos  < len(new_vis): new_vis[self.Pos] += 1
        chr.visual = new_vis

    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current PointwiseDeletion, in the 
        considered cell. It takes the old sequence, and modifies it in order to add the
        PointwiseDeletion.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrID, del_pos = self.ChrID, self.Pos
        node.data.DNA.CHRs[chrID - 1].sequence = node.data.DNA.CHRs[chrID - 1].sequence[ : del_pos]\
             +  node.data.DNA.CHRs[chrID - 1].sequence[del_pos + 1 : ]
    
    def __init__(self, ChrID :int, Pos :int, cell = None):
        """
        It defines the 'SubKind', and initializes 'ChrID' and 'Pos' according to the given 
        parameters.In the end updates the 'visual' array and cheks if the chromosome is deleted.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): position of the deleted DNA base.
            cell (Cell): Cell involved in the PointwiseDeletion.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        super().__init__()
        self.SubKind = "Pointwise Deletion"
        self.ChrID = ChrID
        self.Pos = Pos
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrID - 1].length -= 1
            if cell.DNA.CHRs[ChrID - 1].length == 0:
                cell.DNA.IDs.remove(ChrID)
                print(f"(generation: {cell.generation}) Chromosome {ChrID} has been removed! \n The event was a {self}.\n")

    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID!r}, Pos: {self.Pos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrId: {self.ChrID}, Pos: {self.Pos})"