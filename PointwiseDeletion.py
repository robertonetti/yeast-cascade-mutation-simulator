from Mutation import Mutation
from BinaryTree import Node

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
    reconstruct(self, node: Node):
        Reconstruction of the DNA sequence involved in the current PointwiseDeletion, of the 
        considered cell.
    """
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
        parameters.

        Parameters
        ----------
            ChrID (int): ID of the chromosome involved.
            Pos (int): position of the deleted DNA base.
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