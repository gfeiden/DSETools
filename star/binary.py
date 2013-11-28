#
#
from ..utils.dtype import checkTuple

class Binary(object):
    
    def __init__(self, star1, star2, period):
        """ Instance of binary system from two star objects. """
        self.stars = [star1, star2]
        self.period = checkTuple(period)
        self.N_components = star1.N_components + star2.N_components
        
        try:
            self.total_mass = star1.mass[0] + star2.mass[0]
            self.mass_ratio = star2.mass[0]/star1.mass[0]
        except TypeError:
            print "WARNING: One or more masses not declared.\n"
            self.total_mass = None
            self.mass_ratio = None

        try:
            self.total_rad  = star1.radius[0] + star2.radius[0]
            self.rad_ratio  = star2.radius[0]/star1.radius[0]
        except TypeError:
            print "WARNING: One or more radii not declared.\n"
            self.total_rad  = None
            self.rad_ratio  = None

        try:
            self.temp_ratio = star2.Teff[0]/star1.Teff[0]
        except TypeError:
            print "WARNING: One or more Teffs not declared.\n"
            self.temp_ratio = None

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
