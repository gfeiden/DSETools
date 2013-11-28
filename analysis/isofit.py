#
#
from scipy.interpolate import interp1d

def isofit(system, isochrone, independent = 'mass'):
    """ Fit components of a system to an isochrone. 
    
        This routine takes a system of stars and fits them to a stellar
        evolution isochrone. The fit is performed using a single independent
        variable against a number of dependent variables.
        
        Required Arguments:
        -------------------
        system      ::  stellar system object, either a star, binary, etc.
         
        isochrone   ::  stellar evolution isochrone object
        
        
        Optional Arguments:
        -------------------
        independent ::  independent variable used to interpolate in isochrone
        
        
        Returns:
        --------
        comp_vars   ::  list of strings that identify which variable is in 
                        which column of the following output lists.
        
        theory      ::  list of theoretical predictions for the given 
                        independent variable (one star per row).
                        
        errors      ::  list of signed relative errors for theoretical 
                        predictions for each star (one star per row).
        
        gof         ::  list of chi squared value for goodness of fit of
                        the isochrone to all stars in the system.
    
    """
    if system.N_components == 1:
        system.stars = [system]
    
    # check if isochrone is loaded
    if isochrone.is_loaded:
        pass
    else:
        isochrone.loadIsochrone()
        
    # comparison order
    comp_vars = ['mass', 'teff', 'radius', 'luminosity', 'logg']
    
    if independent.lower() in ['mass', 'm']:
        independent = 'mass'
        dcol = isochrone.column[independent]
        comp_vars.pop(comp_vars.index(independent))
    elif independent.lower() in ['teff', 't_eff', 'temp', 't']:
        independent = 'teff'
        dcol = isochrone.column[independent]
        comp_vars.pop(comp_vars.index(independent))
    elif independent.lower() in ['luminosity', 'lum', 'l']:
        independent = 'luminosity'
        dcol = isochrone.column[independent]
        comp_vars.pop(comp_vars.index(independent))
    elif independent.lower() in ['radius', 'rad', 'r']:
        independent = 'radius'
        dcol = isochrone.column[independent]
        comp_vars.pop(comp_vars.index(independent))
    elif independent.lower() in ['logg', 'gravity']:
        independent = 'logg'
        dcol = isochrone.column[independent]
        comp_vars.pop(comp_vars.index(independent))
    else:
        print "ERROR: Invalid independent variable.\n"
        return None
    
    theory = []    # theoretical predictions for observed stars
    errors = []    # relative errors (O - E)/E of theoretical predicitons
    chi_sq = []    # unsigned relative errors for theoretical predictions
    for star in system.stars:
        star_theory = []
        star_error  = []
        star_chisq  = []
        for prop in comp_vars:
            j = star.pdict[independent]
            obs = star.properties[star.pdict[prop]]
            
            i = isochrone.column[prop]
            icurve = interp1d(isochrone.isochrone[:, dcol], isochrone.isochrone[:, i],
                              kind = 'linear')
            
            try:
                theory = icurve(star.properties[j])
                star_theory.append(theory)
                star_error.append((obs[0] - theory)/obs[0])
                star_chisq.append((obs[0] - theory)**2/obs[0])
            except ValueError:
                star_theory.append(None)
                star_error.append(None)
                star_chisq.append(None)
            except TypeError:
                star_theory.append(None)
                star_error.append(None)
                star_chisq.append(None)
            
        theory.append(star_theory)
        errors.append(star_error)
        chi_sq.append(star_chisq)
    
    # compute goodness of fit 
    gof = []
    for i in range(len(comp_vars)):
        column_total = 0.
        for row in chi_sq:
            column_total += row[i]
        gof.append(column_total)
        
    return comp_vars, theory, errors, gof