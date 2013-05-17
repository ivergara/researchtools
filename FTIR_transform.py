# -*- coding: utf-8 -*-
"""
Created on Thu Apr 04 12:28:03 2013

@author: vergara

ToDo

- add assert or exceptions
- modify for batch use
- modularize to make it compatible with a gui
- add unittest
"""

import csv, sys
import Tkinter

from tkFileDialog import askopenfilename, asksaveasfilename

try:
    from numpy import array
    from scipy.constants import physical_constants
except ImportError:
    print "numpy and scipy have to be present."
    
try:
    import guiqwt.pyplot as pyplot
    __plot = True
except ImportError:
    print "guiqwt module is not present, loading matplotlib instead"
    try:
        import matplotlib.pyplot as pyplot
        __plot = True
    except ImportError:
        print "No plotting capabilities."
        __plot = False
        
def plotWindow(wavelength, signal):
    """
    Plots the loaded spectra for visual inspection.
    """
    
    pyplot.figure("Loaded spectra")
    pyplot.plot(wavelength, signal)
    pyplot.show()

def loadSpectra(spectraFile, unitTransform):
    """
    Loads reflectivity or transmission spectra.
    inputs: 
        spectraFilename: location and mane of the spectra containing file.
        unitTransform: True/False regarding transformation of units.
    
    output: wavelengths in the specified unit and spectra as numpy arrays.
    """
    
    wavelength = []
    signal = []
    with open(spectraFile, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                #Takes the string from the first element and splits it
                row = row[0].split() 
                wavelength.append(float(row[0]))
                signal.append(float(row[1]))
            print "Successful read!"
                    
        except csv.Error, e:
            sys.exit("file %s, line %d: %s" % (input, reader.line_num, e))

    wavelength = array(wavelength)
    signal = array(signal)
    unitTransform = 'electron volt-inverse meter relationship'
    transform = physical_constants[unitTransform][0]/100
    
    if unitTransform:
        wavelength /= transform

    return array(wavelength), array(signal)
    
def main():

    root = Tkinter.Tk()
    root.withdraw() # hide the main GUI window

    angle = 0
    #thickness = None

    inputFilename = askopenfilename(defaultextension = '.dat',
                                    filetypes = [('all files', '.*'), 
                                                 ('text files', '.txt'), 
                                                 ('data files', '.dat')],
                                    title = "Select a measurement")
    
    print "Input filename: ", inputFilename
    
    dataType = raw_input("Define type T (Transmission) or R (Reflectivity): ")
    
    if dataType == 'T' or 't':
        #thickness = raw_input("Set thickness in micrometers: ")
        textType = 'pT'
    elif dataType == 'R' or 'r':
        angle = float(raw_input("Set angle in degrees: "))
        textType = 'pR'
        
    desc = raw_input("Enter a description (optional): ")
    unit = raw_input("Define output units 0 (cm-1) or 1 (eV): ")
    
    if unit:
        defline = ['eV']
    else:
        defline = ['1/cm']
    
    wavelength, signal = loadSpectra(inputFilename, unit)
        
    print "Measurement window: %s - %s" % (wavelength[0], wavelength[-1])
    
    if __plot:
        plot = raw_input("Do you want to plot the loaded data? (Y/N): ")
    
        if plot == 'Y' or 'y':
            plotWindow(wavelength, signal)
    
    lowWindow = float(raw_input("Enter lower window: "))
    highWindow = float(raw_input("Enter higher window: "))
    stride = raw_input("Enter the stride (optional): ")

    if stride == '':
        stride = 0
    else:
        stride = int(stride)
    
    length = len(wavelength)
    lIndex = min(range(length), key=lambda i: abs(wavelength[i]-lowWindow))
    hIndex = min(range(length), key=lambda i: abs(wavelength[i]-highWindow))
    
    wavelength = wavelength[lIndex:hIndex:stride]
    signal = signal[lIndex:hIndex:stride]
    
    outputFilename = asksaveasfilename(defaultextension=".dat", 
                                       title="Choose saving filename")    

    error = raw_input("Insert nominal error (default 10%): ")
    
    if error == '':
        error = 0.1
    else:
        error = float(error)
        
    errorSignal = array(signal)*error
    
    with open(outputFilename, 'wb') as f:
        writer = csv.writer(f, delimiter='\t') # Cols separated by <tab>
        try:
            writer.writerow(desc)
            writer.writerow(defline)

            for i in range(len(wavelength)): # Writes the data into the table
                writer.writerow([textType, 
                                 wavelength[i], 
                                 angle, 
                                 signal[i], 
                                 errorSignal[i]])

        except csv.Error, e:
            sys.exit("file %s, line %d: %s" % (input, writer.line_num, e))
    print "Transformation done!"
    
if __name__ == "__main__":
    
    loop = True

    while loop:    
        main()
        ch = raw_input("Press q or Q to quit.")
        if ch == 'q' or 'Q':
            loop = False