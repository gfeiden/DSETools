#
#
from . import binary

class Triple(object):
    
    def __init__(self, binary, tertiary, outer_period):
        """ Combine single star and binary to create triple. """
        self.addTertiary(tertiary, outer_period)

class Quadruple(object):
    
    def __init__(self, binary1, binary2, period):
        """ Construct quadruple system from two binaries. """
        pass
