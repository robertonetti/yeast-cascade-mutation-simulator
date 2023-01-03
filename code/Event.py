class Event:
    """
    Event Class
    
    Attributes
    ----------
    kind : str
        It defines the kind of the event. (default: None)

    Subclasses
    ----------
        Rearrangement
        Mutation
    """
    def __init__(self):
        """
        It initializes the event kind to 'None'.
        """
        self.kind = None

    def __repr__(self):
        return f"Event(Kind: {self.kind!r})"

    def __str__(self):
        return f"Event(Kind: {self.kind})"