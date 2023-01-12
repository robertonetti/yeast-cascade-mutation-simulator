from code.Cell import Cell
from code.DNA import DNA
from code.Chromosome import Chromosome

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
    def __init__(self, n_chromosomes, chromosome_table, generation = 0, visual = False):
        """
        Defines the kind of the cell as "Wild Type", and initializes its generation and DNA 
        depending on the given parameters.

        Parameters
        ----------
            n_chromosomes (int):
                Number of Chromosomes composing in the cell DNA.
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
            generation (int):
                Generation which the cell belongs to. (default: 0)
            visual (bool):
                True if the visualizaiton is active. False if not.
        """
        self.kind = "Wild Type"
        self.generation = generation
        self.DNA = DNA([Chromosome(id, len(chromosome_table[id - 1][1]), visual=visual) for id in range(1, n_chromosomes + 1)])

    def __repr__(self):
        return f"Cell(kind: {self.kind!r}, generation: {self.generation!r})"

    def __str__(self):
        return f"Cell(kind: {self.kind}, generation: {self.generation})"