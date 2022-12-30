from Event import Event

class Rearrangement(Event):
    """
    Rearrangement Class (sublass of Event)

    Attributes
    ----------
    kind : str
        Kind of event: in this case Rearrangement.
    chr_id : int
        ID of the involved chromosome.

    Subclasses
    ----------
        Insertion
        Deletion
        Translocation
        ReciprocalTranslocation
        Duplication
    """
    def __init__(self):
        """
        It initializes the kind to 'Rearrangement' and the chromosome ID to 'None'.
        """
        self.kind = "Rearrangement"
        self.chr_id = None