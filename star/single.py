#
#

class Star(object):
    
    def __init__(self, mass = None, radius = None, Teff = None, 
                 luminosity = None, metallicity = (0.0, 0.0), 
                 Fe_H = (0.0, 0.0), A_Fe = (0.0, 0.0)):
        """ New instance of star object """
        from ..utils.dtype import checkTuple

        self.mass = checkTuple(mass)
        self.radius = checkTuple(radius)
        self.Teff = checkTuple(Teff)
        self.luminosity = checkTuple(luminosity)
        self.metallicity = checkTuple(metallicity)
        self.Fe_H = checkTuple(Fe_H)
        self.A_Fe = checkTuple(A_Fe)
        
        logg = None
        self.logg = checkTuple(logg)
        
        self.properties = [self.mass, self.radius, self.Teff, self.luminosity, self.logg]
        self.pdict      = {'mass': 0, 'radius': 1, 'teff': 2, 'luminosity': 3, 'logg': 4}
        self.N_components = 1
    
    def dump(self):
        """ Dump star data to a binary file. """
        import pickle
        import datetime
        filename = 'star'
        fdump = open(filename, 'w')
        pickle.dump(self, fdump)
        fdump.close()

    def load(self, filename):
        """ Load star data from a pickle file. """
        import pickle
        fload = open(filename, 'r')
        pickle.load(fload)
        fload.close()
