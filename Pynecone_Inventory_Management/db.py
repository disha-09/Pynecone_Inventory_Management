import pynecone as pc

class Inventory(pc.Model, table=True):
    """A table of inventory."""
    category: str
    quantity: str
    created_at: str