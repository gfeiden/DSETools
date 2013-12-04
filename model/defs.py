# 
#
__all__ = ['plusMinus', 'getModelDirectory', 'getAgeRange', 'getMassRange',
           'getFeHRange', 'getAFeRange', 'getIsochroneCols', 'getLoggedQuantities']

# Dictionaries and data associated with various stellar evolution models
shell_env  = {'Dartmouth': 'DSEP_MODEL_PATH',
              'Lyon'     : 'BCAH_MODEL_PATH',
              'Pisa'     : 'PISA_MODEL_PATH'
             }

age_range  = {'Dartmouth': (1.0e9, 13.0e9, 2.5e8), 
              'Lyon'     : (6.0, 10.0, 0.1)
             }

mass_range = {'Dartmouth': [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 
                            0.24, 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 
                            0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 
                            0.56, 0.58, 0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 
                            0.72, 0.74, 0.76, 0.78, 0.80],
              'Lyon'     : [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45,
                            0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85,
                            0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.30,
                            1.40, 1.50]
             }

feh_range  = {'Dartmouth': [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, 
                            -0.2, -0.1,  0.0,  0.1,  0.2,  0.3,  0.4,  0.5],
              'Lyon'     : [0.0]
             }
              
afe_range  = {'Dartmouth': [0.0, 0.2, 0.4], 
              'Lyon'     : [0.0],
              'Pisa'     : [0.0]
             }

iso_column = {'Dartmouth': {'eep': 0, 'mass': 1, 'logg': 2, 'teff': 3, 
                            'luminosity': 4, 'radius': 5, 'Mv': 10, 'Mi': 11,
                            'Mj': 12, 'Mh': 13, 'Mk': 14},
              'Lyon'     : {'mass': 0, 'teff': 1, 'radius': 2, 'luminosity': 3,
                            'Mv': 4, 'Mr':  5, 'Mi':  6, 'Mj': 7, 'Mh': 8, 
                            'Mk': 9, 'ML': 10, 'Mm': 11}
             }
              
log_values = {'Dartmouth': ['teff', 'radius', 'luminosity'],
              'Lyon'     : ['luminosity']
             }


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
    from numpy import arange
    
    # search dictionary for tuple containing age limits (min, max, delta)
    age_limits = age_range[brand]
    
    # compute ages and unlog ages for certain brands
    ages = arange(age_limits[0], age_limits[1], age_limits[2])
    if brand in ['Lyon']:
        ages = 10.0**ages
        
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