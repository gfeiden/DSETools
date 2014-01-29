#
#
from scipy.interpolate import interp1d
import numpy as np

__all__ = ['resids', 'residuals', 'bestFit', 'saveLikelihoodData']

def resids(system, isochrone, output_file = None, mass_grid_space = 0.001):
    """ Calculate residuals between components of a system and an isochrone.
    
        This routine takes a system of stars and calculates the goodness
        of fit coefficient at each mass point along the isochrone. The fit
        is performed over all stellar properties at every mass point for
        some specified mass spacing along the isochrone. Residuals are 
        computed as relative error and number of standard deviations from
        known (specified) quantities.
        
        Required Arguments
        -------------------
        system       ::  stellar system object, either a star, binary, etc.
         
        isochrone    ::  stellar evolution isochrone object
        
    """
    if system.N_components == 1:
        system.stars = [system]
    
    # check if isochrone is load, if not, load it.
    if isochrone.is_loaded:
        pass
    else:
        isochrone.loadIsochrone()
    
    # get isochrone properties
    mass_col = isochrone.column['mass']
    teff_col = isochrone.column['teff']
    lumi_col = isochrone.column['luminosity']
    radi_col = isochrone.column['radius']
    
    mass_r = isochrone.isochrone[:, mass_col]
    masses = np.arange(min(mass_r), max(mass_r) - mass_grid_space, mass_grid_space)
    
    # interpolate masses onto isochrone for each model property (teff, radius, luminosity)
    icurve = interp1d(isochrone.isochrone[:, mass_col], isochrone.isochrone[:, teff_col])
    i_teff = icurve(masses)
    
    icurve = interp1d(isochrone.isochrone[:, mass_col], isochrone.isochrone[:, lumi_col])
    i_lumi = icurve(masses)
    
    icurve = interp1d(isochrone.isochrone[:, mass_col], isochrone.isochrone[:, radi_col])
    i_radi = icurve(masses)
    
    # compute residual at each point along the isochrone for each star
    for star in system.stars:

        try:
            mass_resid = (star.mass[0] - masses)/star.mass[0]
            mass_resid = np.column_stack((masses, mass_resid))
        except (ValueError, TypeError):
            mass_resid = None
        
        try:
            radius_resid = (star.radius[0] - i_radi)/star.radius[0]
            radius_resid = np.column_stack((i_radi, radius_resid))
        except (ValueError, TypeError):
            radius_resid = None
        
        try:
            teff_resid = (star.Teff[0] - i_teff)/star.Teff[0]
            teff_resid = np.column_stack((i_teff, teff_resid))
        except (ValueError, TypeError):
            teff_resid = None
        
        try:
            lumin_resid = (star.luminosity[0] - i_lumi)/star.luminosity[0]
            lumin_resid = np.column_stack((i_lumi, lumin_resid))
        except (ValueError, TypeError):
            lumin_resid = None
        
        try:
            mass_nusig = (masses - star.mass[0])/star.mass[1]
        except (ValueError, TypeError):
            mass_nusig = None
        
        try:
            radius_nusig = (i_radi - star.radius[0])/star.radius[1]
        except (ValueError, TypeError):
            radius_nusig = None
            
        try:
            teff_nusig = (i_teff - star.Teff[0])/star.Teff[1]
        except (ValueError, TypeError):
            teff_nusig = None
        
        try:
            lumin_nusig = (i_lumi - star.luminosity[0])/star.luminosity[1]
        except (ValueError, TypeError):
            lumin_nusig = None
        
        # compute goodness of fit coefficient for each mass point
        if system.stars.index(star) == 1:
            i_teff_diff = star_resids[prim_bstfit, 4] - i_teff
            try:
                tdiff_resid = (system.Teff_diff[0] - i_teff_diff)/system.Teff_diff[0]
                tdiff_resid = np.column_stack((i_teff_diff, tdiff_resid))
                tdiff_nusig = (system.Teff_diff[0] - i_teff_diff)/system.Teff_diff[1]
            except (ValueError, TypeError):
                tdiff_resid = None
            RMSD = np.sqrt((mass_nusig**2 + radius_nusig**2 + tdiff_nusig**2)/3.)
        else:
            tdiff_resid = None
            RMSD = np.sqrt((mass_nusig**2 + radius_nusig**2 + teff_nusig**2)/3.)
        
        # start stacking columns: prop, err, n_sigma
        try:
            star_resids = np.column_stack((star_resids, mass_resid))
        except NameError:
            star_resids = mass_resid
            
        star_resids = np.column_stack((star_resids, radius_resid))
        star_resids = np.column_stack((star_resids, teff_resid))
        if tdiff_resid != None:
            star_resids = np.column_stack((star_resids, tdiff_resid))
        else:
            pass
        star_resids = np.column_stack((star_resids, RMSD))
        
        # to allow for comparison of temperature difference
        prim_bstfit = np.nanargmin(star_resids[:,6])
    
    if output_file != None:
        np.savetxt(output_file.name, star_resids, fmt='%10.4e', delimiter = '  ' )
    else:
        pass
    
    return star_resids
    

def residuals(system, isochrone, independent = 'mass', compare_to = []):
    """ Calculate residuals between components of a system and an isochrone. 
    
        This routine takes a system of stars and fits them to a stellar
        evolution isochrone. The fit is performed using a single independent
        variable against a number of dependent variables. From the fit, 
        residuals are calculated as relative error and number of standard
        deviations from known quantities.
        
        Required Arguments:
        -------------------
        system       ::  stellar system object, either a star, binary, etc.
         
        isochrone    ::  stellar evolution isochrone object
        
        
        Optional Arguments:
        -------------------
        independent  ::  independent variable used to interpolate in isochrone
        
        compare_to   ::  variables to perform comparison over
        
        
        Returns:
        --------
        comp_vars    ::  list of strings that identify which variable is in 
                         which column of the following output lists.
        
        theory       ::  list of theoretical predictions for the given 
                         independent variable (one star per row).
                        
        errors       ::  list of signed relative errors for theoretical 
                         predictions for each star (one star per row).
        
        nsigma       ::  list of residuals calculated as number of standard
                         deviations from the known quantity. 
        
        likelihood   ::  likelihood estimator for the given isochrone.
        
    """
    if system.N_components == 1:
        system.stars = [system]
    
    # check if isochrone is loaded
    if isochrone.is_loaded:
        pass
    else:
        isochrone.loadIsochrone()
        
    # comparison variables
    if len(compare_to) == 0: 
        comp_vars = ['mass', 'teff', 'radius', 'luminosity', 'logg']
    else:
        comp_vars = compare_to.append(independent.lower())
    
    # select independent variable
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
    
    # Comparison to known observational properties
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
            
            try:
                i = isochrone.column[prop]
            except KeyError:
                continue
            icurve = interp1d(isochrone.isochrone[:, dcol], 
                              isochrone.isochrone[:, i], kind = 'linear')
            
            try:
                model = icurve(star.properties[j][0])
                star_theory.append(float(model))
            except (ValueError, TypeError):
                model = None
                star_theory.append(model)
            
            try:
                star_error.append((obs[0] - model)/obs[0])
            except (ValueError, TypeError, ZeroDivisionError):
                star_error.append(None)
            
            try:
                star_sigma.append((obs[0] - model)/obs[1])
            except (ValueError, TypeError, ZeroDivisionError):         
                star_sigma.append(None)
         
        # comparison to known metallicity (convert to Z/X values)
        star_theory.append(isochrone.Fe_H)
        try:
            zx_star = 10.**(star.Fe_H[0] - 1.636)
            zx_iso  = 10.**(isochrone.Fe_H - 1.636)
            star_error.append((zx_star - zx_iso)/zx_star)
        except (ValueError, TypeError, ZeroDivisionError):
            star_error.append(None)
        
        try:
            zx_err  = 10.**(star.Fe_H[0] + star.Fe_H[1] - 1.636) - zx_star
            star_sigma.append((zx_star - zx_iso)/zx_err)
        except (ValueError, TypeError, ZeroDivisionError):
            star_sigma.append(None)
            
        theory.append(star_theory)
        errors.append(star_error)
        nsigma.append(star_sigma)
    
    comp_vars.append('[Fe/H]')
    
    # likelihood estimator based on all specified properties.
    chi_2 = 0.
    pre   = 1.
    for i in range(len(comp_vars)):
        for row in nsigma:
            try:
                pre    = pre/(sqrt(2.*pi)*star.properties[star.pdict[comp_vars[i]]][1])
            except (TypeError, ValueError, ZeroDivisionError, IndexError):
                continue
            
            try:
                chi_2 += row[i]**2
            except (TypeError, ValueError, IndexError):
                #print "WARNING: Skipping {0} in likelihood calculation".format(comp_vars[i])
                continue
    likelihood = pre*exp(-chi_2/2.)
        
    return comp_vars, theory, errors, nsigma, likelihood


def bestFit(system, isochrone_brand, fit_using = 'mass', compare_to = [],
            return_all = False):
    """ Finds the best fit isochrone for a system of stars 
    
        Given a stellar system (single star, binary, or multiple), this
        routine will find the stellar evolution isochrone that best fits
        all N stars. The "best fit" is determined by a maximum likelihood
        method, where the statistical likelihood is computed for each 
        isochrone.
        
        Note, to return likelihood for every isochrone, set return_all 
        flag to True.
        
        Required Arguments:
        -------------------
        system           ::  stellar system object.
        
        isochrone_brand  ::  string of the particular model set.
        
        Optional Arguments:
        -------------------
        fit_using        ::  independent variable for fitting data to models.
        
        compare_to       ::  variables to perform comparison over.
        
        Returns:
        --------
        fit_data[row]    ::  properties of the best fit isochrone.
        
        row              ::  (optional) row in fit_data that contains data
                             for the best fit isochrone.
        
        fit_data         ::  (optional) likelihood data for each individual 
                             isochrone.
        
    """
    from ..model import isochrone, defs
    
    # get properties of the model set
    feh_range = defs.getFeHRange(isochrone_brand)
    afe_range = defs.getAFeRange(isochrone_brand)
    age_range = defs.getAgeRange(isochrone_brand)
    
    # compute residuals/likelihoods for each isochrone in the model set
    #
    #-- Currently set up to output properties for a single star, though
    #   binary likelihoods are calculated
    #   Probably have to consider two output files or one long output?
    fit_data = []
    maximum  = 0.
    i = 0
    row = i
    for afe in afe_range:
        for feh in feh_range:
            for age in age_range:
                #print "Working on:", age, feh, afe
                iso = isochrone.Isochrone(age, feh, alpha_enhancement = afe,
                                          brand = isochrone_brand)
                resids = residuals(system, iso, independent = fit_using, 
                                   compare_to = compare_to)
                fit_data.append([age/1.e3, feh, afe, resids[4], resids[1][0][0],
                                 resids[1][0][1], resids[1][0][2], resids[1][0][3]])
                if resids[4] > maximum:
                    maximum = resids[4]
                    row = i
                i += 1
            #-- age loop
        #-- Fe/H loop
    #-- A/Fe loop
    
    if return_all:
        return row, fit_data
    else:
        return fit_data[row]
    

def saveLikelihoodData(data, filename = 'likelihood.dat'):
    """ Write likelihood data to a file 
    
    """
    file_out = open(filename, 'w')
    
    # write file header
    file_out.write('#\n# Best fit on line {:.0f} \n#\n'.format(data[0] + 3))
    
    # write data to file (add space between metallicities)
    feh = data[1][0][1]
    for line in data[1]:
        if line[1] != feh:
            file_out.write('\n')
            feh = line[1]
        try:
            s = '{:6.3f}{:7.1f}{:5.1f}{:16.4e}{:14.6f}{:14.6f}{:14.6f}{:14.6f}\n'.format(
                line[0], line[1], line[2], line[3], line[4], line[5], line[6],
                line[7])
            file_out.write(s)
        except ValueError:
            continue
    