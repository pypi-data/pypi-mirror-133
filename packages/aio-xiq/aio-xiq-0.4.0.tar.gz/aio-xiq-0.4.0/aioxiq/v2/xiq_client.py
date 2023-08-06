from .devices import XiqDevices
from .locations import XiqLocations
from .auth import XiqAuth


class XiqClient(XiqDevices, XiqLocations, XiqAuth):
    """
    General purpose XIQ client providing inventory functionality
    """

    pass
