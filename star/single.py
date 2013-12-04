#
#

class Star(object):
    
    def __init__(self, name = None, mass = None, radius = None, Teff = None, 
                 luminosity = None, logg = None, metallicity = (0.0, 0.0), 
                 Fe_H = (0.0, 0.0), A_Fe = (0.0, 0.0)):
        """ New instance of star object 
        
            Creates an object with properties of a single star. Note that
            all properties should be given as a tuple or list, where the 
            first element is the value and the second element is the
            uncertainty. Thus, mass = (1.0, 0.1) would imply a star with
            1.0 +/- 0.1 Msun.
            
            Required Arguments:
            -------------------
            None
            
            Optional Arguments:
            -------------------
            name         ::  name of the star
            
            mass         ::  mass of star in solar masses
            
            radius       ::  radius of star in solar radii
            
            Teff         ::  effective temperature of star in Kelvin
            
            luminosity   ::  luminosity of star in solar luminosities
            
            logg         ::  log(g), surface gravity, of the star in cgs
            
            metallicity  ::  [M/H] of star in dex
            
            Fe_H         ::  [Fe/H] of star in dex
            
            A_Fe         ::  [alpha/Fe] of star in dex
            
            Returns:
            --------
            Star object.
        
        """
        from ..utils.dtype import checkTuple
        
        self.name = name
        self.mass = checkTuple(mass)
        self.radius = checkTuple(radius)
        self.Teff = checkTuple(Teff)
        self.luminosity = checkTuple(luminosity)
        self.logg = checkTuple(logg)
        self.metallicity = checkTuple(metallicity)
        self.Fe_H = checkTuple(Fe_H)
        self.A_Fe = checkTuple(A_Fe)
        
        self.properties = [self.mass, self.radius, self.Teff, self.luminosity, self.logg,
                           self.Fe_H]
        self.pdict      = {'mass': 0, 'radius': 1, 'teff': 2, 'luminosity': 3, 'logg': 4,
                           '[Fe/H]': 5}
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
        
    def fitIsochrone(self, isochrone, fit_using = 'mass'):
        """ Calculate residuals for star compared to a given isochrone 
        
            Required Arguments:
            -------------------
            isochrone  ::  isochrone object to compare against observations.
            
            Optional Arguments:
            -------------------
            fit_using  ::  stellar property to use as the fitting variable.
                           options - 'mass', 'radius', 'teff', 'luminosity', 
                                     'logg'
                                     
            Returns:
            --------
            comp_vars  ::  property in a given column for the following data
            
            theory     ::  theoretical predictions for given quantity
            
            error      ::  relative error for a given quantity
            
            nsigma     ::  number of standard deviations from observed value
            
        """
        from ..analysis.isofit import residuals
        return residuals(self, isochrone, independent = fit_using)
        
    def bestIsochrone(self, isochrone_brand = 'Dartmouth', fit_using = 'mass',
                      return_all = False):
        """ Find the best fit isochrone for the star 
        
            Required Arguments:
            -------------------
            None
            
            Optional Arguments:
            -------------------
            isochrone_brand  ::  isochrone set
            
            fit_using        ::  independent variable used to fit data
            
            Returns:
            --------
            
        """
        from ..analysis.isofit import bestFit
        return bestFit(self, isochrone_brand, fit_using = fit_using, 
                       return_all = return_all)
