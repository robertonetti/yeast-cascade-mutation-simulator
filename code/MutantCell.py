from DNA import DNA
from Cell import Cell

class MUT_Cell(Cell):
    """
    Mutant Cell Class (subclass of Cell)

    Attributes
    ----------
    kind: str
        It describes the kind of cell: 'Mutant' in this case.
    generation: int
        Generation to which the cell belongs.
    DNA: DNA
        It contains the DNA of the cell. In particular its chromosomes and their sequences.
    events: list
        List of the new events occurred in the cell in the corresponding generation.
    """
    def __init__(self, DNA :DNA, events = [], generation = 0):
        """
        It defines the kind of the cell as "Mutant", and initializes its 'generation', 'DNA' and 
        'events' depending on the given parameters.

        Parameters
        ----------
            DNA (DNA):
                Contains the DNA of the cell. In particular its chromosomes and their sequences.
            events (list):
                List of the new events occurred in the cell in the corresponding generation.
                (default: [])
            generation (int):
                Generation which the cell belongs to.
                (default: 0O)
        """
        self.kind = "Mutant"
        self.generation = generation
        self.DNA = DNA
        self.events = events

    def __repr__(self):
        return f"Cell(kind: {self.kind!r}, generation: {self.generation!r}, number of events: {len(self.events)!r})"

    def __str__(self):
        return f"Cell(kind: {self.kind}, generation: {self.generation}, number of events: {len(self.events)})"

