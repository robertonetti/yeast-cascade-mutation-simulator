from Event import Event

class Mutation(Event):
    """
    Mutation Class (sublass of Event)

    Attributes:
    ----------
    kind : str
        Kind of event: in this case 'Mutation'.
    chr_id : int
        ID of the involved chromosome.

    Subclasses:
    ----------
        PointwiseInsertion
        PointwiseDeletion
        PointwiseReplacement
    """
    def __init__(self):
        """
        It initializes the kind to 'Mutation' and the chromosome ID to 'None'.
        """
        self.kind = "Mutation"
        self.chr_id = None