class Chromosome:
    """
    Chromosome Class
    
    Attributes
    ----------
    ID : int
        ID of the considered chromosome.
    length : int
        Length of the considered chromosome.
    visual : list 
        Array of the same length of the chromosome sequence. It contains an integer for each DNA base 
        in the sequence, indicating how many times that base was involved in a Rearrangement/Mutataion.
    sequence : str
        DNA sequence of the considered chromosome.
    """
    def __init__(self, ID, length):
        """
        Checks if the "ID" of the chromosome is among the possible ones. Then initializes the "ID", 
        "length" and its "visual", based on the given vector "chromosome_lenghts".

        Parameters
        ----------
            ID (int): ID of the considered chromosome.
            length (int): length of the considered chromosome.
            visual (bool): True if the visualizaiton is active. False if not.

        Raises
        ------
            Exception
                The chromosome ID cannot be 0.
        """
        if ID <= 0 : raise Exception(f"ID cannot be smaller than 0!")
        self.ID = ID
        self.length = length
        
    sequence = None
    visual = None

    def __repr__(self):
        return f"Chromosome(ID: {self.ID!r}, length: {self.length!r}, sequence: {self.sequence!r})"

    def __str__(self):
        return f"Chromosome(ID: {self.ID}, length: {self.length}, sequence: {self.sequence})"
