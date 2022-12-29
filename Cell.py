# CELL
class Cell:
    """
    Generic Cell Class

    Attributes:
    ----------
    kind: str
        Kind of the cell: 'Wild Type' or 'Mutant'. (default: None)
    generation: int
        Generation to which the cell belongs. (default: None)
    DNA: DNA
        It contains the DNA of the cell. In particular its chromosomes and their sequences. 
        (default: None)

    Subclasses:
    ----------
    WT_Cell
    MUT_Cell
    """
    def __init__(self):
        """
        Initializes 'kind', 'generation' and 'DNA' to None.   
        """
        self.kind = None
        self.generation = None
        self.DNA = None

    def __repr__(self):
        return f"Cell(kind: {self.kind!r}, generation: {self.generation!r})"

    def __str__(self):
        return f"Cell(kind: {self.kind}, generation: {self.generation})"
