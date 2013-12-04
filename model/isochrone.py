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
            
        self.age     = age
        self.Fe_H    = metallicity
        self.A_Fe    = alpha_enhancement
        self.brand   = brand        
        self.column  = defs.getIsochroneCols(self.brand)
        
        # locate isochrone directory
        iso_directory  = defs.getModelDirectory(brand) + '/iso'
        
        # generate location and name of isochrone files
        if self.brand in ['Dartmouth', 'DMESTAR']:
            feh_letter     = defs.plusMinus(self.Fe_H)
            afe_letter     = defs.plusMinus(self.A_Fe)
            
            feh_directory  = '{:s}{:03.0f}'.format(feh_letter, abs(self.Fe_H*100.))
            afe_directory  = 'a{:01.0f}'.format(abs(self.A_Fe*10.))
            afe_file       = '{:s}{:01.0f}'.format(afe_letter, abs(self.A_Fe*10.))
        
            self.directory = '{0}/{1}/{2}'.format(iso_directory, feh_directory,
                                                  afe_directory)
            self.filename  = 'dmestar_{:05.0f}myr_feh{:s}_afe{:s}.iso'.format(
                                                                   self.age/1.e6,
                                                                   feh_directory,
                                                                   afe_file)
            self.comm_rows = 0
        elif self.brand in ['Lyon', 'BCAH98']:
            age            = 10.0**round(np.log10(self.age), 1)
            amlt_directory = 'a19'
            self.directory = '{0}/{1}'.format(iso_directory, amlt_directory)
            self.filename  = 'bcah98_{:05.0f}_mh00_amlt{:s}.iso'.format(
                                                               age/1.e6,
                                                               amlt_directory[1:])
            self.comm_rows = 4
        else:
            print 'ERROR: Incorrect isochrone brand specified.'
            self.directory = ''
            self.filename  = ''
                  
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
            file. Header information is read using readIsochroneHeader() 
            and is saved in a variable separate from the rest of the isochrone 
            information.
            
            Required Arguments:
            -------------------
            None
            
            
            Optional Arguments:
            -------------------
            None
            
            
            Returns:
            --------
            Properties of isochrone object called 'isochrone' and 'header'.
            
        """
        if self.exists == False:
            print '\nIsochrone does not exist. Please create a new isochrone.\n'
        else:
            try:
                self.loadIsochroneHeader()
                self.isochrone = np.genfromtxt(self.filepath, comments = '#', 
                                               skiprows = self.comm_rows)
                self.is_loaded = True
                self.unlogColumns()
            except TypeError:
                print 'ERROR: Isochrone load failed.\n'
                self.is_loaded = False
                
    def unlogColumns(self):
        """ Unlog columns containing logged quantities 
        
        """
        logged = defs.getLoggedQuantities(self.brand) 
        for prop in logged:
            i = self.column[prop]
            self.isochrone[:, i] = 10.0**self.isochrone[:, i]
        #print '\nQuantities successfully unlogged.\n'
    
    
    def returnIsochrone(self):
        """ Return isochrone numerical data """
        return self.isochrone
    
    
    def generateIsochrone(self, kind = 'simple'):
        """ Create a new isochrone from mass track library """
        from .isogen import createIsochrone, createHeader
        if kind not in ['simple', 'complex']:
            print '\nType of isochrone generation specified is incorrect.'
            print 'Choose either \'simple\' or \'complex\'.'
        else:
            createIsochrone(self, kind = kind)
            createHeader(self, N = len(self.isochrone))
    
    
    def loadIsochroneHeader(self):
        """ Read isochrone file header """
        import fileinput as fi
        self.header_loaded = True
        if self.comm_rows == 0:
            self.header = [line for line in fi.input(self.filepath) if line[0] == '#']
        else:
            self.header = []
    
    
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
        self.magnitudes = tc.transform(self.Fe_H, self.A_Fe, 
                                       self.isochrone[:, 2],
                                       self.isochrone[:, 4], 
                                       self.isochrone[:, 3],
                                       len(self.isochrone))
        self.isochrone = np.concatenate((self.isochrone, self.magnitudes), axis=1)
        self.addMagsToHeader()
    
    
    def addMagsToHeader(self):
        """ Add magnitude designation to header information """
        s = '{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}\n'.format('B', 
                                                                             'V', 'R', 'I', 
                                                                             'V', 'I', 'J', 
                                                                             'H', 'K')
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
