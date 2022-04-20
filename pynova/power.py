import scipy.stats
from scipy.optimize import brentq

def power_anova_test(groups=None, n=None, between_var=None, within_var=None, sig_level=0.05, power=None):
    # Check for errors
    if sum(x is None for x in [groups, n, between_var, within_var, sig_level, power]) != 1:
        raise Exception("exactly one of 'groups', 'n', 'between_var', 'within_var', 'power', and 'sig_level' must be NoneType")
    if (groups is not None) and (groups < 2):
        raise Exception("number of groups must be at least 2")
        
    # Declare calculate_power function
    def calculate_power(grp, num, btw, wit, sig):
        ncp = (grp - 1) * num * (btw/wit)
        q = scipy.stats.f.ppf(1-sig, dfn=grp-1, dfd=(num-1) * grp)
        
        return 1 - scipy.stats.ncf.cdf(q, dfn=grp-1, dfd=(num-1) * grp, nc=ncp)
    
    # Calculate the argument with NoneType
    # POWER
    if power is None:
        return calculate_power(groups, n, between_var, within_var, sig_level)
    
    # GROUPS
    elif groups is None:
        grp_funct = lambda x: calculate_power(x, n, between_var, within_var, sig_level) - power

        groups = brentq(grp_funct, 2, 100)

        # Round to nearest int if off by a little
        if np.abs(1-(groups % 1)) < 1e-10:
            return round(groups)
        # else round down
        else:
            return int(groups)

    # N
    elif n is None:
        return -1
    
    # WITHIN_VAR
    elif within_var is None:
        return -1
    
    # BETWEEN_VAR
    elif between_var is None:
        return -1
    
    # SIG_LEVEL
    elif sig_level is None:
        return -1
    
    else:
        raise Exception("internal error")
        
    