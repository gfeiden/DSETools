# 
#
__all__ = ['plusMinus', 'getModelDirectory', 'getAgeRange', 'getMassRange',
           'getFeHRange', 'getAFeRange', 'getIsochroneCols', 'getLoggedQuantities']

# Dictionaries and data associated with various stellar evolution models
shell_env  = {'BAton'    : 'ATON_MODEL_PATH',
              'Dartmouth': 'DART_MODEL_PATH',
              'DMESTAR'  : 'DMES_MODEL_PATH',
              'DSEP08'   : 'DSEP_MODEL_PATH',
              'Lyon10'   : 'BCAH_MODEL_PATH',
              'Lyon19'   : 'BCAH_MODEL_PATH',
              'Pisa'     : 'PISA_MODEL_PATH',
              'Yale'     : 'YALE_MODEL_PATH'
             }

age_range  = {'Dartmouth': (1.0e9, 13.0e9, 2.5e8), 
              'DMESTAR'  : (1.0e6, 20.1e6, 1.0e5),
              'DSEP08'   : (1.0e6, 1.0e9),
              'Lyon10'   : (6.0, 10.0, 0.1),
              'Lyon19'   : (6.0, 10.0, 0.1)
             }

mass_range = {'BAton'    : [0.09, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 
                            0.80, 0.90, 1.00, 1.20, 1.40, 1.60, 1.80, 2.30, 
                            2.50, 2.80, 3.00, 3.30, 3.50, 3.80],
              'Dartmouth': [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 
                            0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 
                            0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 
                            0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 
                            0.72, 0.74, 0.76, 0.78, 0.80],
              'DMESTAR'  : [0.09, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40,
                            0.45, 0.50, 0.55, 0.65, 0.70, 0.75, 0.80, 0.85,
                            0.90, 0.95, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50,
                            1.60, 1.70, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30,
                            2.40, 2.50, 2.60, 2.70, 2.80, 2.90, 3.00, 3.10,
                            3.20, 3.30, 3.40, 3.50, 3.60, 3.70, 3.80, 3.90,
                            4.00, 4.10, 4.20, 4.30, 4.40, 4.50, 4.60, 4.70,
                            4.80, 4.90, 5.00],
              'DSEP08'   : [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
                            0.50, 0.55, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90,
                            0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30,
                            1.35, 1.40, 1.45, 1.50, 1.55, 1.60, 1.65, 1.70,
                            1.75, 1.80, 1.90, 2.00, 2.10, 2.20, 2.30, 2.40,
                            2.50, 2.60, 2.70, 2.80, 2.90, 3.00, 3.20, 3.40,
                            3.60, 3.80, 4.00, 4.20, 4.40, 4.60, 4.80, 5.00],
              'Lyon10'   : [0.020, 0.030, 0.040, 0.050, 0.055, 0.060, 0.070,
                            0.072, 0.075, 0.080, 0.090, 0.100, 0.110, 0.130,
                            0.150, 0.175, 0.200, 0.250, 0.300, 0.350, 0.400, 
                            0.450, 0.500, 0.550, 0.600, 0.650, 0.700, 0.750, 
                            0.800, 0.850, 0.900, 0.950, 1.000, 1.050, 1.100, 
                            1.150, 1.200, 1.300, 1.400, 1.500],
              'Lyon19'   : [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
                            0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85,
                            0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30,
                            1.40, 1.50],
              'Pisa'     : [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 
                            0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95,
                            1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 
                            1.80, 1.90, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00,
                            3.20, 3.40, 3.60, 3.80, 4.00, 4.50, 5.00, 5.50,
                            6.00, 6.50, 7.00],
              'Yale'     : [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
                            0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85,
                            0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25]
             }

feh_range  = {'BAton'    : [0.0],
              'Dartmouth': [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, 
                            -0.2, -0.1,  0.0,  0.1,  0.2,  0.3,  0.4,  0.5],
              'DMESTAR'  : [0.0],
              'DSEP08'   : [-0.5, 0.0, 0.20, 0.3, 0.5],
              'Lyon10'   : [0.0],
              'Lyon19'   : [0.0],
              'Pisa'     : [-1.80, -1.10, -0.80, -0.60, -0.50, -0.40, -0.30,
                            -0.25, -0.20, -0.10, -0.05,  0.00,  0.10,  0.20,
                             0.25,  0.30,  0.35,  0.40,  0.45],
              'Yale'     : [-1.5, -1.0, -0.5, 0.0, 0.3]
             }
              
afe_range  = {'BAton'    : [0.0],
              'Dartmouth': [0.0, 0.2, 0.4], 
              'DMESTAR'  : [0.0],
              'DSEP08'   : [-0.2, 0.0, 0.2, 0.4, 0.8],
              'Lyon10'   : [0.0],
              'Lyon19'   : [0.0],
              'Pisa'     : [0.0],
              'Yale'     : [0.0]
             }

iso_column = {'BAton'    : {'mass': 0, 'luminosity': 1, 'teff': 2, 'logg': 3},
              'Dartmouth': {'eep': 0, 'mass': 1, 'logg': 2, 'teff': 3, 
                            'luminosity': 4, 'radius': 5, 'Mv': 10, 'Mi': 11,
                            'Mj': 12, 'Mh': 13, 'Mk': 14},
              'DMESTAR'  : {'mass': 0, 'teff': 1, 'logg': 2, 'luminosity': 3,
                            'radius': 4},
              'DSEP08'   : {'mass': 0, 'teff': 1, 'logg': 2, 'luminosity': 3},
              'Lyon10'   : {'mass': 0, 'teff': 1, 'logg': 2, 'luminosity': 3, 
                            'Mv': 4, 'Mr':  5, 'Mi':  6, 'Mj': 7, 'Mh': 8, 
                            'Mk': 9, 'ML': 10, 'Mm': 11},
              'Lyon19'   : {'mass': 0, 'teff': 1, 'radius': 2, 'luminosity': 3,
                            'Mv': 4, 'Mr':  5, 'Mi':  6, 'Mj': 7, 'Mh': 8, 
                            'Mk': 9, 'ML': 10, 'Mm': 11},
              'Pisa'     : {'luminosity': 0, 'teff': 1, 'mass': 2},
              'Yale'     : {'mass': 0, 'luminosity': 1, 'radius': 2, 'logg': 3,
                            'teff': 4}
             }
              
log_values = {'BAton'    : ['teff', 'luminosity'],
              'Dartmouth': ['teff', 'radius', 'luminosity'],
              'DMESTAR'  : ['teff', 'radius', 'luminosity'],
              'DSEP08'   : ['teff', 'luminosity'],
              'Lyon10'   : ['luminosity'],
              'Lyon19'   : ['luminosity'],
              'Pisa'     : ['luminosity', 'teff'],
              'Yale'     : ['luminosity', 'radius', 'teff']
             }

yaleXZMap  = {-1.5: (0.74865, 0.00054), -1.0: (0.74574, 0.00171), 
              -0.5: (0.73671, 0.00535),  0.0: (0.70952, 0.01631),
               0.3: (0.67336, 0.03090)}

pisaZMap   = {-1.80: 0.0002, -1.10: 0.0010, -0.80: 0.0020, -0.60: 0.0030,
              -0.50: 0.0040, -0.40: 0.0050, -0.30: 0.0060, -0.25: 0.0070,
              -0.20: 0.0080, -0.10: 0.0090, -0.05: 0.0100,  0.00: 0.0125,
               0.10: 0.0150,  0.20: 0.0175,  0.25: 0.0200,  0.30: 0.0225,
               0.35: 0.0250,  0.40: 0.0275,  0.45: 0.0300}


def plusMinus(x):
    """ Determine whether value is positive (p) or negative (m) 
    
        The purpose of the routine is to assign a string prefix to a value,
        either 'p' or 'm', based on whether or not the value is positive
        or negative. This simple assignment is necessary for generating 
        names of stellar evolution mass track and isochrone files where 
        'p' and 'm' are substituted for '+' and '-' (plus and minus).
    
        Required Arguments:
        -------------------
        x       ::  real or integer value.
        
        
        Optional Arguments:
        -------------------
        None
        
        
        Returns:
        --------
        prefix  ::  either 'p' or 'm' for positive or negative, respectively.
    
    """
    if x < 0.:
        return 'm'
    else:
        return 'p'
    

def getMassRange(brand):
    """ Get range of track msases for model brand """
    return mass_range[brand]


def getAgeRange(brand):
    """ Get range of isochrone ages for model brand 
    
        Required Arguments:
        -------------------
        brand  ::  modeling group.
        
        
        Optional Arguments:
        -------------------
        None
        
        
        Returns:
        --------
        ages   ::  array of ages for which isochrones are computed.
    
    """
    from numpy import arange, append
    
    # search dictionary for tuple containing age limits (min, max, delta)
    #age_limits = age_range[brand]
    
    # hard code age range properties (temporary)
    if brand in ['Lyon', 'Lyon10', 'Lyon19']:
        ages = 10.0**arange(6.0, 10.1, 0.1)
    elif brand in ['DMESTAR', 'DSEP14', 'DSEP08', 'DSEP']:
        ages = arange(1.0e6, 20.0e6, 1.0e5) 
        ages = append(ages, arange(2.0e7, 1.001e8, 5.0e6))
    elif brand in ['Pisa']:
        ages = arange(1.0e6, 20.0e6, 1.0e6)
        ages = append(ages, arange(2.0e7, 1.001e8, 5.0e6))
    elif brand in ['Yale', 'Yale13', 'BAton']:
        ages = arange(1.0e6, 2.0e7, 2.0e5)
        ages = append(ages, arange(2.0e7, 1.0e8, 5.0e6))
    else:
        ages = 0.0
        
    return ages


def getFeHRange(brand):
    """ Get range of metallicities for model brand """
    return feh_range[brand]


def getAFeRange(brand):
    """ Get range of [alpha/Fe] for model brand """
    return afe_range[brand]


def getModelDirectory(brand):
    """ Get shell environment variable for a given model brand """
    from os import getenv
    return getenv(shell_env[brand])


def getIsochroneCols(brand):
    return iso_column[brand]


def getLoggedQuantities(brand):
    return log_values[brand]