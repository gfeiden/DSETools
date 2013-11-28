#
#
from . import masstrack as dtrk
from . import defs

def createIsochrone(age = None, metallicity = None, alpha_enhancement = None, 
                    kind = 'simple'):
    """ Create isochrone from mass track library 
    
        Generate a new isochrone for a given age, metallicity, and alpha
        abundance enhancement. If mass tracks have already been computed
        for the requested metallicity and alpha enhancement, then the
        isochrone can be computed straight away. Otherwise, an interpolation
        must be performed over one or both of those variables to acquire
        the correct mass tracks. 
        
        INPUT
        -----
            age                 --- Age of the isochrone in years
            metallicity         --- Scaled-solar [Fe/H] in dex
            alpha_enhancement   --- Alpha abundance enhancement in dex
            kind                --- Type of isochrone to create:
                                        simple  - pull information from
                                                  mass tracks at a given 
                                                  age
                                        complex - use EEP formalism 
    """
    # Error check to ensure arguments are properly declared
    if None in [age, metallicity, alpha_enhancement]:
        print '\nNot all isochrone properties were specified. Please delcare:'
        print '\t- Age (in yrs)\n\t- [Fe/H] (in dex)\n\t- [a/Fe] (in dex)\n'
    
    if kind not in ['simple', 'complex']:
        print '\nIsochrone generation type not properly declared.\n'
    
    # determine whether an interpolation has to be performed first
    feh = metallicity
    afe = alpha_enhancement
    if feh not in dlib.feh_list:
        feh_in_grid = False
    else:
        feh_in_grid = True
    if afe not in dlib.afe_list:
        afe_in_grid = False
    else:
        afe_in_grid = True
    
    if False in [feh_in_grid, afe_in_grid]:
        interpolateMassTracks(metallicity = feh,
                              alpha_abund = afe,
                              skip_feh    = feh_in_grid, 
                              skip_afe    = afe_in_grid)
    else:
        pass
    
    if kind == 'simple':
        isochrone = generateSimpleIsochrone(age, feh, afe)
    else:
        isochrone = generateComplexIsochrone(age, feh, afe)
    
    return isochrone
    
def createHeader(age, metallicity, alpha_abund, N):
    """ Create the header for a new isochrone """
    Z_sun  = 0.018837
    Y      = 0.
    amlt   = 1.938
    Z      = Z_sun*10.**metallicity
    header = ['#MIX-LEN  Y       Z           [Fe/H] [a/Fe]\n']
    values = '# {:6.4f}{:8.4f} {:8.4e}   {:3.2f}{:6.2f}\n'.format(amlt, Y, Z,
                                                                 metallicity,
                                                                 alpha_abund)
    header.append(values)
    header.append('#AGE={:8.0f} EEPS={:4.0f}\n'.format(age/1.e6, N))
    header.append('#EEP  MASS      Log G     Log Teff    Log(L/Lo)    Log(R/Ro)\n')
    return header

def generateSimpleIsochrone(age, metallicity, alpha_abund):
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
    from scipy.interpolate import interp1d
    from numpy import empty, delete
    
    iso_cols = {0: 3, 1: 2, 2: 4, 3: 5}
    
    isochrone = empty([len(dlib.mass_list), 6])  # create an empty array
    
    j   = -1
    k   = 0
    eep = 0
    for mass in dlib.mass_list:
        track = dtrk.MassTrack(mass, metallicity, alpha_enhancement = alpha_abund)
        track.loadTrack(peel = False)
        
        try:
            len(track.track)
        except AttributeError:
            k += 1
            continue
        
        if len(track.track) < 100:
            k += 1
            continue  
        else:
            #print 'Processing M = {:4.2f} Mo'.format(mass)
            pass
                    
        j += 1
        isochrone[j, 0] = j
        isochrone[j, 1] = mass
        for i in range(4):
            curve = interp1d(track.track[:, 0], track.track[:, i + 1])
            
            try:
                isochrone[j, iso_cols[i]] = curve(age)
            except ValueError:
                j += -1
                k += 1
                break
                
    return delete(isochrone, [len(isochrone) - x - 1 for x in range(k)], 0)

def interpolateMassTracks(feh_new = None, afe_new = None, skip_feh = False,
                          skip_afe = True):
    """ Interpolate mass tracks in metallicity and/or alpha abundance
    """
    #import utils.fortinterp as fint
    import os
    if not skip_feh:
        feh_list = dlib.feh_list.insert(0, feh_new)
        feh_list.sort()
        i = feh_list.index(feh_new)
        if i == 0:
            i += 1
        elif i == len(feh_list) - 1:
            i += -1
        else:
            pass
        files = []
        feh_list = [feh_list[i - 1], feh_list[i + 1]]
        for mass in dlib.mass_list:
            for feh in feh_list:
                trk = dtrk.MassTrack(mass, feh)
                files.append(trk.filepath)
            del trk
            try: 
                open(files[0])
                open(files[1])
            except:
                break
            #fint.mass_track_interpolate(feh_list, feh_new, files, len(files[0]))
    else:
        pass
    
