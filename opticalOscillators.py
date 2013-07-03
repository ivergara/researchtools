# -*- coding: utf-8 -*-
"""
Models optical responses (oscillators) of materials.

ToDo:
- Multiple units
- Clean import statements (raise)
"""

import numpy as np

class oscillatorModel(object):
    """Base class for all kinds of oscillators."""
    
    def __init__(self):
        pass
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function."""
        pass
    
    def refractionIndex(self):
        """Returns the complex refractive index."""
        pass
    
    def spectralWeight(self, window):
        """Calculates the area of the oscillator given its
           parameters."""
        pass
    
    def plasmaFrequency(self):
        """Calculates the square of plasma frequency in eV^2 of
        the oscillator given its parameters."""
        pass
    
class Lorentzian(oscillatorModel):
    """Lorentzian lineshape of the form 
    
        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}
        
        Where $A$ is the amplitude, $B$ the width, $E_c$ energy center. 
        All values given in $eV$
    """
    
    def __init__(self, amplitude, energy, width):
        """Defines a Lorenzian lineshape.
        
        input
        =====
        
        amplitude: Amplitude in eV
        energy: Energy center in eV
        width: width of the lineshape in eV
        """
        
        self.amplitude = amplitude
        self.energy = energy
        self.width = width
      
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        num = (self.amplitude*self.width)*self.energy
        den = self.energy**2-energy**2-1.j*self.width*energy
        
        return num/den
    
    def opticalConductivity(self, window):
        """Returns the optical conductivity of the oscillator.
        
        \sigma(E) = \epsilon_2(E)*\epsilon_0*E/\hbar^2
        """
        
        # Fix units!
        return np.imag(self.dielectricFunction(window))*window
        
    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')
        
        else:
            return self.amplitude*self.energy*self.width
            
class Gaussian(oscillatorModel):
    """Lorentzian lineshape."""
    
    def __init__(self, amplitude, energy, width):
        """Defines a Gaussian lineshape.
        
        input
        =====
        
        amplitude: Amplitude in eV
        energy: Energy center in eV
        width: width of the lineshape in eV
        """
        
#    def dielectricFunction(self, energy):
#        """Returns the complex dielectric function at the specified energy.
#        
#        input
#        =====
#        
#        energy: Specified (range) of values to return.
#        """
#        
#        def _realDF(self, energy):
#            pass
#    
#        def _imagDF(self, energy):
#            pass
#        
#        return _realDF(energy) + 1.j*_imagDF(energy)
