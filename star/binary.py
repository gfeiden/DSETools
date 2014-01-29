#
#
from ..utils.dtype import checkTuple

class Binary(object):
    
    def __init__(self, star1, star2, period=(None, None), Teff_diff = (None, None)):
        """ Instance of binary system from two star objects. 
        
            Creates a binary star system from two single star objects 
            that orbit with a given period, semi-major axis, and 
            eccentricity.
            
            Required Arguments:
            -------------------
            star1            ::  star object of the primary component.
            
            star2            ::  star object of the secondary component.
            
            period           ::  period of the binary in days.
            
            Optional Arguments:
            -------------------
            semi_major_axis  ::  semi-major axis of the orbit in AU
            
            eccentricity     ::  eccentricity of the orbit
            
            Returns:
            --------
            Binary star object.
            
        """
        from numpy import sqrt
        self.stars = [star1, star2]
        self.period = checkTuple(period)
        self.N_components = star1.N_components + star2.N_components
        
        try:
            self.total_mass = star1.mass[0] + star2.mass[0]
            self.mass_ratio = star2.mass[0]/star1.mass[0]
            self.mrat_error = self.mass_ratio*sqrt((star2.mass[1]/star2.mass[0])**2 +
                                                   (star1.mass[1]/star1.mass[0])**2)
            self.mtot_error = star1.mass[1] + star2.mass[1]
        except TypeError:
            print "WARNING: One or more masses not declared.\n"
            self.total_mass = None
            self.mass_ratio = None

        try:
            self.rad_sum    = star1.radius[0] + star2.radius[0]
            self.rad_ratio  = star2.radius[0]/star1.radius[0]
            self.rsum_error = star1.radius[1] + star2.radius[1]
        except TypeError:
            print "WARNING: One or more radii not declared.\n"
            self.rad_sum    = None
            self.rad_ratio  = None

        try:
            self.temp_ratio = star2.Teff[0]/star1.Teff[0]
            self.trat_error = self.temp_ratio*sqrt((star2.Teff[1]/star2.Teff[0])**2 +
                                                   (star1.Teff[1]/star1.Teff[0])**2)
        except TypeError:
            print "WARNING: One or more Teffs not declared.\n"
            self.temp_ratio = None
            self.trat_error = None
        
        self.Teff_diff = checkTuple(Teff_diff)

        try:
            self.total_lum  = star1.luminosity[0] + star2.luminosity[0]
            self.lum_ratio  = star2.luminosity[0]/star1.luminosity[0]
        except TypeError:
            print "WARNING: One or more luminosities not declared.\n"
            self.total_lum  = None
            self.lum_ratio  = None

    def addTertiary(self, star, period):
        """ Add tertiary component to a binary system. """
        self.stars.append(star)
        self.outer_period = checkTuple(period)
        self.N_components += star.N_components

        try:
            self.total_lum[0] += star.luminosity[0]
        except:
            print "WARNING: One or more luminosities not specified."
            
    def bestIsochrone(self, isochrone_brand = 'Dartmouth', fit_using = 'mass'):
        """ Fits the system to multiple isochrones to find the best. """
        from ..analysis import isofit
        isofit.bestFit(self, isochrone_brand, independent = fit_using)
