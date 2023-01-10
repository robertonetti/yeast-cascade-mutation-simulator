from scipy.sparse import *

class Chromosome:
    """
    Chromosome Class
    
    Attributes
    ----------
    ID : int
        ID of the considered chromosome.
    length : int
        Length of the considered chromosome.
    sequence : str
        DNA sequence of the considered chromosome.
    """
    def __init__(self, ID, length):
        """
        Checks if the "ID" of the chromosome is among the possible ones. Then initializes the "ID"
        and its "length" based on the given vector "chromosome_lenghts".

        Parameters
        ----------
            ID (int): ID of the considered chromosome.
            length (int): length of the considered chromosome.

        Raises
        ------
            Exception
                The chromosome ID cannot be 0.
        """
        if ID <= 0 : raise Exception(f"ID cannot be smaller than 0!")
        self.ID = ID
        self.length = length
        self.visual = lil_matrix((1, length))
    sequence = None

    def __repr__(self):
        return f"Chromosome(ID: {self.ID!r}, length: {self.length!r}, sequence: {self.sequence!r})"

    def __str__(self):
        return f"Chromosome(ID: {self.ID}, length: {self.length}, sequence: {self.sequence})"
