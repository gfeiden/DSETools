#
from . import isochrone as diso
from . import masstrack as dlib
from numpy import arange

ages = arange(1.75e9, 13.6e9, 1.e9)
afe  = 0.

for age in ages:
    for feh in dlib.feh_list:
        print 'Age = {:6.0f}  [Fe/H] = {:+4.1f}\n'.format(age/1.e6, feh)
        iso = diso.Isochrone(age, feh)
        iso.generateIsochrone()
        iso.addColor()
        iso.writeIsochrone()

        
