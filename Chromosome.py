from Parameters import chromosome_table

class Chromosome:
    """
    Chromosome Class
    
    Attributes:
    ----------
    ID : int
        ID of the considered chromosome.
    length : int
        Length of the considered chromosome.
    sequence : str
        DNA sequence of the considered chromosome.
    """
    def __init__(self, ID):
        """
        Checks if the "ID" of the chromosome is among the possible ones. Then initializes the "ID"
        and its "length" based on the given vector "chromosome_lenghts".

        Parameters:
        ----------
            ID (int): ID of the considered chromosome.

        Raises:
        ------
            Exception
                If the chromosome ID is larger than the number of chromosomes.
            Exception
                The chromosome ID cannot be 0.
        """
        if ID > len(chromosome_table) : raise Exception(f"ID is too large. \
            ID can be from 1 to: {len(chromosome_table)}")
        if ID <= 0 : raise Exception(f"ID cannot be 0. \
            ID can be from 1 to: {len(chromosome_table)}")
        self.ID = ID
        self.length = len(chromosome_table[ID - 1][1])

    sequence = None

    def __repr__(self):
        return f"Chromosome(ID: {self.ID!r}, length: {self.length!r}, sequence: {self.sequence!r})"

    def __str__(self):
        return f"Chromosome(ID: {self.ID}, length: {self.length}, sequence: {self.sequence})"
