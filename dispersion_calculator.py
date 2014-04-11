# -*- coding: utf-8 -*-
"""

Computes the lower and upper boundaries of two (or more) particle 
dispersion E(k)

"""

from collections import defaultdict
from numpy import arange

def computeDispersionBoundary(firstDispersion, secondDispersion = None):
    """
    Takes one dispertion relation and computes the two-particle continuum 
    boundaries for such excitation. If a second dispersion relation is 
    provided, it computes the boundary between the two given sets.
    
    input: 
        list of touples describing the dispersion
        relation [(k1,E1), (k2,E2), ..., (kn,En)]
        
    output:
        list of touples describing the lower and upper
        bounds of the continuum
    """
    
    if not secondDispersion:
        secondDispersion = firstDispersion[::1]

    dispersionContinuum = defaultdict(list)
    
    for pair1 in firstDispersion:
        for pair2 in secondDispersion:
            k = round(abs(pair1[0]-pair2[0]), 4) # momentum
            E = pair1[1]+pair2[1]                # energy
            dispersionContinuum[k].append(E)
            
    lowerBound = []
    upperBound = []
    
    for (key, value) in dispersionContinuum.iteritems():
        lowerBound.append((key, min(value)))
        upperBound.append((key, max(value)))
        
    return (lowerBound, upperBound)
        
if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    import operator
    from numpy import sin
    
    k = arange(0,1,0.01)
    E1 = k
    
    print("Testing two-particle dispersion boundaries from elementary excitation")
    
    disp1 = zip(k,E1)
    
    out = computeDispersionBoundary(disp1)
    
    #Sorting the pairs given their k value
    low = out[0].sort(key=operator.itemgetter(0))
    high = out[1].sort(key=operator.itemgetter(0))
    
    #Composing two list from the colelction of 2-touples
    low = zip(*out[0])
    high = zip(*out[1])
    
    plt.plot(k,E1)
    plt.plot(low[0], low[1], 'g-')
    plt.plot(high[0], high[1], 'r-')
    
    plt.show()
    
    print("Testing two-particle dispersion boundaries")
    
    E2 = arange(2,0,-0.01)
    disp2 = zip(k,E2)
    
    out = computeDispersionBoundary(disp1, disp2)
    
    #Sorting the pairs given their k value
    low = out[0].sort(key=operator.itemgetter(0))
    high = out[1].sort(key=operator.itemgetter(0))
    
    #Composing two list from the colelction of 2-touples
    low = zip(*out[0])
    high = zip(*out[1])
    
    plt.plot(k,E1)
    plt.plot(low[0], low[1], 'b-')
    plt.plot(high[0], high[1], 'k-')
    
    plt.show()