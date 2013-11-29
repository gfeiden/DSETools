#
#
from scipy.interpolate import interp1d

def residuals(system, isochrone, independent = 'mass'):
    """ Calculate residuals between components of a system and an isochrone. 
    
        This routine takes a system of stars and fits them to a stellar
        evolution isochrone. The fit is performed using a single independent
        variable against a number of dependent variables. From the fit, 
        residuals are calculated as relative error and number of standard
        deviations from known quantities.
        
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
        
        nsigma      ::  list of residuals calculated as number of standard
                        deviations from the known quantity. 
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
    nsigma = []    # unsigned relative errors for theoretical predictions
    for star in system.stars:
        star_theory = []
        star_error  = []
        star_sigma  = []
        for prop in comp_vars:
            j = star.pdict[independent]
            obs = star.properties[star.pdict[prop]]
            
            i = isochrone.column[prop]            
            if prop in ['teff', 'radius', 'luminosity']:
                icurve = interp1d(isochrone.isochrone[:, dcol], 
                                  isochrone.isochrone[:, i],
                                  kind = 'linear')
            else:
                icurve = interp1d(isochrone.isochrone[:, dcol], 
                                  isochrone.isochrone[:, i],
                                  kind = 'linear')
            
            try:
                model = icurve(star.properties[j][0])
                star_theory.append(float(model))
            except ValueError:
                model = None
                star_theory.append(None)
            except TypeError:
                model = None
                star_theory.append(None)
            
            try:
                star_error.append((obs[0] - model)/obs[0])
            except ValueError:
                star_error.append(None)
            except TypeError:
                star_error.append(None)
            
            try:
                star_sigma.append((obs[0] - model)/obs[1])
            except ValueError:         
                star_sigma.append(None)
            except TypeError:
                star_sigma.append(None)
            
        theory.append(star_theory)
        errors.append(star_error)
        nsigma.append(star_sigma)
    
    ## compute goodness of fit
    #gof = []
    #for i in range(len(comp_vars)):
        #column_total = 0.
        #for row in chi_sq:
            #try:
                #column_total += row[i]
            #except TypeError:
                #column_total = None
        #gof.append(column_total)
        
    return comp_vars, theory, errors, nsigma

def bestFit(system, isochrone_brand, independent = 'mass'):
    """ Finds the best fit isochrone for a system of stars """
    return