#
#
import dsepiso as diso
import dseptrk as dtrk
import dseplib as dlib

def createIsochrone(age = None, metallicity = None, alpha_enhancement = None,
                    kind = 'simple')
    """ Create isochrone from mass track library """
    if None in [age, metallicity, alpha_enhancement]:
        print '\nNot all isochrone properties were specified. Please delcare:'
        print '\t- Age (in yrs)\n\t- [Fe/H] (in dex)\n\t- [a/Fe] (in dex)\n'
    
    if kind not in ['simple', 'complex']:
        print '\nIsochrone generation type not properly declared.\n'

def generateNewIsochrone():
    """ Create new isochrone from given age, metallicity, and alpha 
        enhancement. 
        
        This routine creates a new Dartmouth model isochrone from the 
        pre-computed mass track library. If, mass tracks exist for the
        given metallicity and alpha enhancement, then an isochrone at
        the given age is computed directly. Otherwise, mass tracks must
        first be generated for the requested metallicity and alpha 
        enhancement. Interpolating in the mass tracks produces smoother
        results than interpolating in a pre-computed grid of isochrones
        at the cost of computational time.
    """
    

def interpolateNewIsochrone():
