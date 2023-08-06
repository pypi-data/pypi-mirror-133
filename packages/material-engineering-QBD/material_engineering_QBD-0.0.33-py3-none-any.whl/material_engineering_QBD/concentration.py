import units_QBD as uqbd
import numpy

def p(energy__grid, ldos, F_v, T):
    de = energy__grid[1] - energy__grid[0]
    p = []
    for energies in ldos:
        p.append(0)
        for i in range(0,len(energies)):
            p[-1] += de * energies[i] / (1 + numpy.exp((F_v - energy__grid[i]) / uqbd.K_B[0] / T)) 
    return p

def n(energy__grid, ldos, F_c, T):
    de = energy__grid[1] - energy__grid[0]
    n = []
    for energies in ldos:
        n.append(0)
        for i in range(0,len(energies)):
            n[-1] += de * energies[i] / (1 + numpy.exp((energy__grid[i] - F_c) / uqbd.K_B[0] / T)) 
    return n
