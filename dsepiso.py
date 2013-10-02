#
#
import numpy as np

class Isochrone(object):
    
    def __init__(self, age, metallicity, alpha_enhancement = 0.0):
        """ Initialize DSEP isochrone """
        # isochrone properties
        if age < 1.e6:
            print "\nRequested age has incorrect units. Input age in Yrs.\n"
        else:
            self.age = age
        self.feh = metallicity
        self.afe = alpha_enhancement
    
        # isochrone location and file name [TO DO LATER]
        self.directory = '../p010/a0/'
        self.filename  = 'dmestar_{:05.0f}myr_fehp010.iso'.format(int(self.age/1.e6))
        self.filepath  = self.directory + self.filename
        
        # check if isochrone file exists
        try:
            open(self.filepath)
            self.file_exists = True
        except:
            self.file_exists = False
    
    def loadIsochrone(self):
        """ Load isochrone from file 
        
        This routine loads numerical data from the specified isochrone 
        file. Header information is read using readIsochroneHeader() and
        is saved in a variable separate from the rest of the isochrone 
        information.       
        """
        if self.file_exists == False:
            print '\nIsochrone does not exist. Generating new isochrone.\n'
        else:
            self.header    = self.loadIsochroneHeader()
            self.isochrone = np.genfromtxt(self.filepath, comments='#')
    
    def returnIsochrone(self):
        """ Return isochrone numerical data """
        return self.isochrone
    
    def createIsochrone(self, kind = 'simple'):
        """ Create a new isochrone from mass track library """
        import isogen
        if kind not in ['simple', 'complex']:
            print '\nType of isochrone generation specified is incorrect.'
            print 'Choose either \'simple\' or \'complex\'.'
        else:
            isogen.createIsochrone(age = self.age, 
                                   metallicity = self.feh,
                                   alpha_enhancement = self.afe, 
                                   kind = kind)
        
    def loadIsochroneHeader(self):
        """ Read isochrone file header """
        import fileinput as fi
        return [line for line in fi.input(self.filepath) if line[0] == '#']
    
    def returnIsochroneHeader(self):
        """ Return isochrone header information """
        loadIsochroneHeader()
        
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
        s1 = '{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}\n'.format(
            'B', 'V', 'R', 'I', 'V', 'I', 'J', 'H', 'K')
        self.header[-1] = self.header[-1].rstrip()
        self.header[-1] += s
    
    def writeColorIsochrone(self):
        """ Write out isochrone data with magnitudes to a file """
        fout = open(self.filename, 'w')
        for line in self.header:
            fout.write(line)
        np.savetxt(fout, self.isochrone, fmt='%10.6f')
        fout.close()
    
    def plotIsochrone():
        """ Plot different properties of an isochrone """
