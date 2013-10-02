# Library of DSEP mass track masses, metallicities, and alpha enhancements.
#
import os

def plusMinus(x = 0.):
    if x < 0.:
        x = 'm'
    else:
        x = 'p'
    return x

model_directory = os.getenv('DSEP_MODEL_PATH')
trk_directory   = '{0}/trk'.format(model_directory)
iso_directory   = '{0}/iso'.format(model_directory)

mass_list = [0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26,
             0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46,
             0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.64, 0.66,
             0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80]
             
feh_list  = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1,
              0.0,  0.1,  0.2,  0.3,  0.4,  0.5] 
              
afe_list  = [0.0, 0.2, 0.4]


