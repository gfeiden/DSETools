#
#
import numpy as np
from . import defs

class MassTrack(object):
    
    def __init__(self, mass, metallicity, alpha_enhancement = 0.0):
        """ Initialize DSEP mass track. """
        self.mass = mass
        self.feh  = metallicity
        self.afe  = alpha_enhancement
        
        # generate a file name for the track
        feh_letter = defs.plusMinus(self.feh)
        afe_letter = defs.plusMinus(self.afe)
        
        track_directory = defs.getModelDirectory('Dartmouth') + '/trk'
        feh_directory   = '{:s}{:03.0f}'.format(feh_letter, abs(self.feh*100.))
        afe_directory   = 'a{:01.0f}'.format(abs(self.afe*10.))
        
        self.directory  = '{0}/{1}/{2}'.format(track_directory,\
                                                 feh_directory,\
                                                 afe_directory)
        self.filename   = 'm{:04.0f}_GS98_{:s}{:.0f}_{:s}{:01.0f}_T60.iso'.format(
                           self.mass*1000., feh_letter, abs(self.feh*100.),
                           afe_letter, abs(self.afe*10.))
        self.filepath   = '{0}/{1}'.format(self.directory, self.filename)
        
    def loadTrack(self, peel = True):
        """ Load stellar evolution mass track into an array.
            
            The file associated with the mass track object is loaded if
            the file exists. Otherwise, the program will throw an error.
            By default, the routine will peel the columns from a larger
            track file to generate individual properties. This option 
            can be turned off, in which case the routine will save the 
            entire track file to one large array.
            
            INPUT
            -----
                peel    --- determine whether or not to save the track 
                            file to one large array or as individual 
                            properties (OPTIONAL).
                      
        """
        try:
            self.track = np.genfromtxt(self.filepath, comments='#')
            flag = 0
        except:
            print '\nERROR: File {0} not found.\n'.format(self.filepath)
            flag = 1
        if flag == 0 and peel:
            self.peelTrack()     
            
    def peelTrack(self, save_full_track = False):
        """ Peel columns off of large mass track array. """
        self.age       = self.track[:, 0]   # age [yrs]
        self.logT      = self.track[:, 1]   # log(Teff) [K]
        self.logg      = self.track[:, 2]   # log(g) [cgs]
        self.logL      = self.track[:, 3]   # log(L/Lsun)
        self.radius    = self.track[:, 4]   # log(R/Rsun)
        self.He_core   = self.track[:, 5]   # mass fraction of helium in core
        self.Z_core    = self.track[:, 6]   # mass fraction of Z in core
        self.Z_X_env   = self.track[:, 7]   # Z/X at the surface
        self.Lum_H     = self.track[:, 8]   # luminosity due to H burning
        self.Lum_He    = self.track[:, 9]   # luminosity due to He burning
        self.M_He_core = self.track[:, 10]  # mass of helium core (Mstar)
        self.M_CO_core = self.track[:, 11]  # mass of carbon/oxygen core (Mstar)
        self.k2        = self.track[:, 12]  # apsidal motion constant
        self.turnover  = self.track[:, 14]  # convective turnover time [day]
        if save_full_track:
            pass
        else:
            del self.track
        
    def inRange(self):
        # check that [Fe/H] and [a/Fe] are in range of track library
        if not min(defs.feh_list) <= self.feh <= max(defs.feh_list):
            print '\nRequested [Fe/H] = {:+6.2f} is out of range.\n'.format(self.feh)
            in_range = False
        else:
            in_range = True
            
        if not min(defs.afe_list) <= self.afe <= max(defs.afe_list):
            print '\nRequested [a/Fe] = {:+6.2f} is out of range.\n'.format(self.afe)
            in_range = False
        else:
            in_range = True         
        return in_range
        
    def inLibrary(self):
        """ Check track is in the pre-computed library.
        
            Confirms whether or not a mass track with the specified 
            properties already exists in the pre-computed library. The
            routine also checks user generated tracks that have been 
            computed in the past.
        """
        if self.mass not in defs.mass_list:
            self.mass_exists = False
        else:
            self.mass_exists = True
        
        if self.feh not in defs.feh_list:
            self.feh_exists = False
        else:
            self.feh_exists = True
        
        if self.afe not in defs.afe_list:
            self.afe_exists = False
        else:
            self.afe_exists = True
        
        if self.mass_exists and self.feh_exists and self.afe_exists:
            self.in_library = True
        else:
            self.in_library = False
        
