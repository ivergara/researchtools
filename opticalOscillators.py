# -*- coding: utf-8 -*-
"""
Models optical responses (oscillators) of materials.

"""

from math import log, sqrt

import numpy as np

import scipy.constants as constants
from scipy.constants import physical_constants

class oscillatorModel(object):
    """Base class for all kinds of oscillators."""
    
    def __init__(self):
        pass
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function."""
        pass
    
    def opticalConductivity(self, window):
        """Returns the optical conductivity of the oscillator.
        
        \sigma(E) = \epsilon_2(E)*\epsilon_0*E/\hbar^2
        """
        
        # Fix units!
        _hbar = physical_constants['natural unit of action in eV s'][0]
        _preFactor = constants.epsilon_0/_hbar

        return _preFactor*np.imag(self.dielectricFunction(window))*window
    
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
    
    .. math::
    
        \epsilon(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}
        
        Where:
        $A$ is the amplitude (dimensionless), 
        $B$ the width (eV), 
        $E_c$ energy center (eV).         
    """
    
    def __init__(self, amplitude, energy, width):
        """Defines a Lorenzian lineshape.
        
        input
        =====
        
        amplitude: Amplitude (dimensionless)
        energy: Energy center (eV)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert energy >= 0
        assert width >= 0
        
        self.amplitude = amplitude
        self.energy = energy
        self.width = width
        
    def __repr__(self):
        return 'Lorentzian lineshape' #print also the parameters!
        
    def __str__(self):
        return 'Lorentzian'
      
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        num = (self.amplitude*self.width)*self.energy
        den = self.energy**2-energy**2-1.j*self.width*energy
        
        return num/den
        
    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')
        
        else:
            _hbar = physical_constants['natural unit of action in eV s'][0]
            _preFactor = constants.epsilon_0*constants.pi/8/_hbar**2
            return _preFactor*self.amplitude*self.energy*self.width

class Drude(oscillatorModel):
    """Drude lineshape of the form 
    
    .. math::
    
        \epsilon(E) = -\frac{AB}{E^2+\imath BE}
        
        Where:
        $A$ is the amplitude (eV), 
        $B$ the width (eV).         
    """
    
    def __init__(self, amplitude, width):
        """Defines a Drude lineshape.
        
        input
        =====
        
        amplitude: Amplitude (eV)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert width >= 0
        
        self.amplitude = amplitude
        self.width = width
        
    def __repr__(self):
        return 'Drude lineshape' #print also the parameters!
        
    def __str__(self):
        return 'Drude'
      
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        num = -(self.amplitude*self.width)
        den = energy**2+1.j*self.width*energy
        
        return num/den
        
    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')
        
        else:
            _hbar = physical_constants['natural unit of action in eV s'][0]
            _preFactor = constants.epsilon_0*constants.pi/2/_hbar**2
            return _preFactor*self.amplitude*self.width
            
class Gaussian(oscillatorModel):
    """Gaussian lineshapeof the form 
    
    .. math::
    
        \epsilon_2(E) = \frac{ABE_c}{E_c^2-E^2-\imath BE}
        
        Where:
        $A$ is the amplitude (dimensionless), 
        $B$ the width (eV), 
        $E_c$ energy center (eV),
        
        and \epsilon_1 is determined by Kramer-Kronig consistency.
    """
    
    def __init__(self, amplitude, energy, width):
        """Defines a Gaussian lineshape as described in
        D. De Sousa Meneses, J. Non-Cryst. Solids 351 no.2 (2006) 769-776
        
        input
        =====
        
        amplitude: Amplitude (dimensionless)
        energy: Energy center (eV)
        width: width of the lineshape (eV)
        """
        
        assert amplitude >= 0
        assert energy >= 0
        assert width >= 0
                
        self.amplitude = amplitude
        self.energy = energy
        self.width = width
        
    def __repr__(self):
        return 'Gaussian lineshape' #print also the parameters!
        
    def dielectricFunction(self, energy):
        """Returns the complex dielectric function at the specified energy.
        The real part is calculated to be Kramer-Kronig consistent with
        the imaginary part
        
        input
        =====
        
        energy: Specified (range) of values to return.
        """
        
        def _realDF(imaginatyPart):
            #Add KK consistent part
            return 0
    
        def _imagDF(energy):
            sigma = self.width/(2*sqrt(log(2)))
            e1 = np.exp(-((energy-self.energy)/sigma)**2)
            e2 = np.exp(-((energy+self.energy)/sigma)**2)
            
            return self.amplitude*(e1-e2)
        
        _imaginaryPart = _imagDF(energy)
        _realPart = _realDF(_imaginaryPart)
        
        return _realPart + 1.j*_imaginaryPart
        
    def spectralWeight(self, window = None):
        """Returns the spectral weight of the oscillator.
        
        If the parameter window is specified, a partial weight is calculated.
        """

        if window:
            raise NotImplementedError('Not implemented yet')
        
        else:
            _hbar = physical_constants['natural unit of action in eV s'][0]
            _preFactor = constants.epsilon_0*sqrt(constants.pi)/4*(log(2))/_hbar**2
            return _preFactor*self.amplitude*self.energy*self.width

if __name__ == '__main__':
    G1 = Gaussian(0.3,1,0.9)
    L1 = Lorentzian(0.3,1,0.9)
    
    import matplotlib.pyplot as plt
    x = np.arange(0,2,0.01)
    plt.plot(x,L1.opticalConductivity(x))
    plt.plot(x,G1.opticalConductivity(x))
    plt.xlabel('Energy (eV)')
    plt.ylabel('Optical Conductivity')
    plt.show()