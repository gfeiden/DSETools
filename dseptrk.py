#
#
import dseplib

class MassTrack(object):
    
    def __init__(self, mass, metallicity, alpha_enhancement = 0.0):
        """ Initialize DSEP mass track """
        self.mass = mass
        self.feh  = metallicity
        self.afe  = alpha_enhancement
        
        
    def inRange(self):
        # check that [Fe/H] and [a/Fe] are in range of track library
        if not -1.0 <= self.feh <= 0.5:
            print '\nRequested [Fe/H] = {:+6.2f} is out of range.\n'.format(self.feh)
            err_flag = True
        else:
            err_flag = False
            
        if not 0.0 <= self.afe <= 0.4:
            print '\nRequested [a/Fe] = {:+6.2f} is out of range.\n'.format(self.afe)
            err_flag = True
        else:
            err_flag = False
            
        return err_flag
        
    def inLibrary(self):
        """ Check track is in the pre-computed library.
        
            Confirms whether or not a mass track with the specified 
            properties already exists in the pre-computed library. The
            routine also checks user generated tracks that have been 
            computed in the past.
        """
        if self.mass not in dseplib.mass_list:
            self.mass_exists = False
        else:
            self.mass_exists = True
        
        if self.feh not in dseplib.feh_list:
            self.feh_exists = False
        else:
            self.feh_exists = True
        
        if self.afe not in dseplib.afe_list:
            self.afe_exists = False
        else:
            self.afe_exists = True
        
        if self.mass_exists and self.feh_exists and self.afe_exists:
            self.trk_exists = True
        else:
            self.trk_exists = False
        
