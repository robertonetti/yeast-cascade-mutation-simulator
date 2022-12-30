class DNA:
    """
    DNA Class
    
    Attributes
    ----------
    CHRs : list
        List containing the chromosomes of the cell.
    IDs : list
        List containing the IDs of the chromosome currently present in the cell.
    """
    def __init__(self, chromosomes):
        """
        It initializes the attribute 'CHRs' according to the parameter "chromosomes" given.

        Parameters
        ----------
            chromosomes (list): list of chromosomes (class Chromosome).
        """
        self.CHRs = chromosomes
        self.IDs = list(range(1, len(chromosomes) + 1))

    def __repr__(self):
        return f"DNA(number of chromosomes: {len(self.CHRs)!r})"

    def __str__(self):
        return f"Cell(number of chromosomes: {len(self.CHRs)})"