from Cell import Cell
from DNA import DNA
from Chromosome import Chromosome

# WT CELL
class WT_Cell(Cell):
    """
    Mutant Cell Class (subclass of Cell)

    Attributes
    ----------
    kind: str
        Describes the kind of cell: 'Wild Type' in this case.
    generation: int
        Generation which the cell belongs to. Usually Wild Type cells have 'generation = 0'.
    DNA: DNA
        Contains the DNA of the cell. In particular its chromosomes and their sequences.
    """
    def __init__(self, chromosome_table, generation = 0):
        """
        Defines the kind of the cell as "Wild Type", and initializes its generation and DNA 
        depending on the given parameters.

        Parameters
        ----------
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
            generation (int):
                Generation which the cell belongs to. (default: 0)
            visual (bool):
                True if the visualizaiton is active. False if not.
        """
        self.kind = "Wild Type"
        self.generation = generation
        self.DNA = DNA([Chromosome(id, len(chromosome_table[id - 1][1])) for id in range(1, len(chromosome_table) + 1)])

    def __repr__(self):
        return f"Cell(kind: {self.kind!r}, generation: {self.generation!r})"

    def __str__(self):
        return f"Cell(kind: {self.kind}, generation: {self.generation})"