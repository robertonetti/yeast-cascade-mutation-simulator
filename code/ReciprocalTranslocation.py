from code.Rearrangement import Rearrangement
from code.BinaryTree import Node
import numpy as np

class ReciprocalTranslocation(Rearrangement):
    """
    Reciprocal Translocation Class (subclass of Rearrangement)

    Attributes
    ----------
    SubKind: str
        Subkind of Rearrangement. In this case: 'Translocation'
    ChrIDs: tuple
        IDs of the chromosomes involved. First the one from which the sequence is deleted, and 
        second the one in which is inserted.
    InitPos: int
        Initial position (on the first chromosome) of the translocated sequence, before 
        translocation.
    Length: int
        Length of the translocated sequence.
    FinalPos: int
        Initial position (on the second chromosome) of the translocated sequence, after 
        translocation.

    Methods
    -------
    reconstruct(self, node: Node)
        Reconstruction of the DNA sequence involved in the current ReciprocalTranslocation, of the 
        considered cell.
    """





    def update_visual(self, chrs: tuple):
        translocated = chrs[0].visual[self.InitPos : self.InitPos + self.Length] + 1
        new_vis_1 = np.concatenate((chrs[0].visual[: self.InitPos], chrs[0].visual[self.InitPos + self.Length :]))
        new_vis_2 = np.concatenate((chrs[1].visual[: self.FinalPos], translocated, chrs[1].visual[self.FinalPos :]))
        if len(new_vis_1) != chrs[0].length: raise Exception(f"chr 1: visual={len(new_vis_1)}, chr_len={chrs[0].length}")
        if self.InitPos - 1 >= 0: new_vis_1[self.InitPos - 1] += 1
        if self.InitPos  < len(new_vis_1): new_vis_1[self.InitPos] += 1
        if len(new_vis_2) != chrs[1].length: raise Exception(f"chr 2: visual={len(new_vis_2)}, chr_len={chrs[0].length}")
        chrs[0].visual, chrs[1].visual = new_vis_1, new_vis_2









    def reconstruct(self, node: Node):
        """
        Reconstruction of the DNA sequence involved in the current ReciprocalTranslocation, in the 
        considered cell. It takes the old sequence, and modifies it in order to add the 
        ReciprocalTranslocation.

        Parameters
        ----------
            node (Node): node containing the involved cell.
        """
        chrIDs, init_pos, end_pos, final_pos = self.ChrIDs, self.InitPos, self.InitPos + self.Length, self.FinalPos
        transl_seq = node.data.DNA.CHRs[chrIDs[0] - 1].sequence[init_pos : end_pos]
        node.data.DNA.CHRs[chrIDs[0] - 1].sequence = node.data.DNA.CHRs[chrIDs[0] - 1].sequence[ : init_pos] \
             +  node.data.DNA.CHRs[chrIDs[0] - 1].sequence[end_pos : ]
        node.data.DNA.CHRs[chrIDs[1] - 1].sequence = node.data.DNA.CHRs[chrIDs[1] - 1].sequence[ : final_pos] \
            + transl_seq + node.data.DNA.CHRs[chrIDs[1] - 1].sequence[final_pos : ]

    def __init__(self, ChrIDs :tuple, InitPos :int, Length :int, FinalPos :int, cell = None):
        """
        It defines the 'SubKind', and initializes 'ChrID', 'InitPos', 'Length', 'FinalPos' according
        to the given parameters.

        Parameters
        ----------
            ChrID (int): IDs of the chromosomes involved. First the one from which the sequence is 
                         deleted, and second the one in which is inserted.
            InitPos (int): Initial position (on the first chromosome) of the translocated sequence,
                           before translocation.
            Length (int): Length of the translocated sequence.
            FinalPos (int): Initial position (on the second chromosome) of the translocated sequence,
                            after translocation.
        """
        super().__init__()
        self.SubKind = "Reciprocal Translocation"
        self.ChrIDs = ChrIDs
        self.InitPos = InitPos
        self.Length = Length
        self.FinalPos = FinalPos
        if cell != None:
            cell.events.append(self)
            cell.DNA.CHRs[ChrIDs[0] - 1].length -= self.Length
            cell.DNA.CHRs[ChrIDs[1] - 1].length += self.Length
            chrs = (cell.DNA.CHRs[ChrIDs[0] - 1], cell.DNA.CHRs[ChrIDs[1] - 1])
            self.update_visual(chrs)
            if cell.DNA.CHRs[ChrIDs[0] - 1].length == 0:
                cell.DNA.IDs.remove(ChrIDs[0])
                print(f"(generation: {cell.generation}) Chromosome {ChrIDs[0]} has been removed! The events was a {self}.")

    def __repr__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrIds: {self.ChrIDs!r}, InitPos: {self.InitPos!r}, Length: {self.Length!r}, FinalPos: {self.FinalPos!r})"

    def __str__(self):
        return f"Event->{self.kind}->{self.SubKind}(ChrIds: {self.ChrIDs}, InitPos: {self.InitPos}, Length: {self.Length}, FinalPos: {self.FinalPos})"