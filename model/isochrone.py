#
#
import numpy as np
from . import defs

class Isochrone(object):
    
    def __init__(self, age, metallicity, alpha_enhancement = 0.0, brand = 'Dartmouth'):
        """ Initialize isochrone object
            
            This class defines a stellar evolution model isochrone at a
            given age, metallicity, and alpha abundance enhancement. During
            the initialization routine, properties that can be determined
            before loading the actual isochrone data are assigned. 
            
            Note that additional isochrone or model track sets can be added
            and there is no real restriction to what options can be used.
            However, all tracks and isochrones must be downloaded by the 
            user from the original source and are not provided with this
            software package.
            
            Required Arguments:
            -------------------
            age                ::  age of the isochrone (in years).
            
            metallicity        ::  scaled-solar [Fe/H] (in dex)
            
            Optional Arguments:
            -------------------
            alpha_enhancement  ::  alpha abundance enhancement (in dex)
            
            brand              ::  isochrone series, options are:
                                     - 'Dartmouth' or 'DMESTAR' (Feiden+ 2014)
                                     - 'Dartmouth08' or 'DSEP'  (Dotter+ 2008)
                                     - 'Lyon' or 'BCAH98'       (Baraffe+ 1998)
                                     - 'Pisa'                   (Tognelli+ 2011)
                                     - 'Yale'                   (Spada+ 2013)
                                     - 'Siess' or 'SDF00'       (Siess+ 2000)
                                     - 'Padova'                 (Bressan+ 2012)
                                     - 'ATON97'                 (D'Antona & Mazitelli 1997)
                                     - 'ATON04'                 (Montalban+ 2004)
                                     - 'ATON09                  (Di Criscienzo+ 2009)
            
            Returns:
            --------
            Isochrone object.
                     
        """
        self.is_loaded = False
        
        # isochrone properties
        if age < 1.e6:
            print "\nRequested age has incorrect units. Input age in Yrs.\n"
        else:
            self.age = age
        self.feh   = metallicity
        self.afe   = alpha_enhancement
        self.brand = brand
        
        if self.brand == 'Dartmouth':
            self.column = {'eep': 0, 'mass': 1, 'logg': 2, 'teff': 3, 
                           'luminosity': 4, 'radius': 5}
    
        # isochrone location and file name
        feh_letter     = defs.plusMinus(self.feh)
        afe_letter     = defs.plusMinus(self.afe)
        
        iso_directory  = defs.iso_directory
        feh_directory  = '{:s}{:03.0f}'.format(feh_letter, abs(self.feh*100.))
        afe_directory  = 'a{:01.0f}'.format(abs(self.afe*10.))
        afe_file       = '{:s}{:01.0f}'.format(afe_letter, abs(self.afe*10.))
        self.directory = '{0}/{1}/{2}'.format(iso_directory, feh_directory,
                                              afe_directory)
        self.filename  = 'dmestar_{:05.0f}myr_feh{:s}_afe{:s}.iso'.format(
                                                                   self.age/1.e6,
                                                                   feh_directory,
                                                                   afe_file)
        self.filepath  = '{0}/{1}'.format(self.directory, self.filename)
        
        # check if isochrone file exists
        try:
            open(self.filepath)
            self.exists = True
        except:
            self.exists = False
    
    def loadIsochrone(self):
        """ Load isochrone from file 
        
        This routine loads numerical data from the specified isochrone 
        file. Header information is read using readIsochroneHeader() and
        is saved in a variable separate from the rest of the isochrone 
        information.       
        """
        if self.exists == False:
            print '\nIsochrone does not exist. Please create a new isochrone.\n'
        else:
            try:
                self.loadIsochroneHeader()
                self.isochrone = np.genfromtxt(self.filepath, comments='#')
                self.is_loaded = True
            except:
                print 'ERROR: Isochrone load failed.\n'
                self.is_loaded = False
    
    def returnIsochrone(self):
        """ Return isochrone numerical data """
        return self.isochrone
    
    def generateIsochrone(self, kind = 'simple'):
        """ Create a new isochrone from mass track library """
        from isogen import createIsochrone, createHeader
        if kind not in ['simple', 'complex']:
            print '\nType of isochrone generation specified is incorrect.'
            print 'Choose either \'simple\' or \'complex\'.'
        else:
            self.isochrone = createIsochrone(age = self.age, 
                                             metallicity = self.feh,
                                             alpha_enhancement = self.afe, 
                                             kind = kind)
            self.header    = createHeader(age = self.age, 
                                          metallicity = self.feh,
                                          alpha_abund = self.afe, 
                                          N = len(self.isochrone))
        
    def loadIsochroneHeader(self):
        """ Read isochrone file header """
        import fileinput as fi
        self.header_loaded = True
        self.header = [line for line in fi.input(self.filepath) if line[0] == '#']
    
    def returnIsochroneHeader(self):
        """ Return isochrone header information """
        if not self.header_loaded:
            self.loadIsochroneHeader()
        return self.header
        
    def parseIsochroneHeader(self):
        """ Parse data in isochrone header """
        
    def addColor(self, system = ''):
        """ Perform color-Teff transformation using requested system """
        import teffcolor as tc
        self.magnitudes = tc.transform(self.feh, self.afe, 
                                       self.isochrone[:, 2],
                                       self.isochrone[:, 4], 
                                       self.isochrone[:, 3],
                                       len(self.isochrone))
        self.isochrone = np.concatenate((self.isochrone, self.magnitudes), axis=1)
        self.addMagsToHeader()
        
    def addMagsToHeader(self):
        """ Add magnitude designation to header information """
        s = '{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}\n'.format('B', 'V', 'R', 'I', 'V', 'I', 'J', 'H', 'K')
        self.header[-1] = self.header[-1].rstrip()
        self.header[-1] += s
    
    def writeIsochrone(self):
        """ Write out isochrone data with magnitudes to a file """
        import os
        # check if directory exists
        try:
            os.stat(self.directory)
        except OSError:
            os.mkdir(self.directory)
        fout = open(self.filepath, 'w')
        for line in self.header:
            fout.write(line)
        np.savetxt(fout, self.isochrone, fmt='%10.6f')
        fout.close()
    
    def plotIsochrone():
        """ Plot different properties of an isochrone """
