# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 09:54:07 2018

@author: Steven
"""
import matplotlib.pyplot as pp
import numpy as np

saveplot = 1
n=6                     #number of isotopes
start_test_num = 85     #used for naming test spectra

x_min = 0               #parameters for axes for plotting
y_min = 0
x_max = 1000
y_max = 400
bin_num_x = 500
bin_num_y = 200

#gaussian broadening parameters, from "Delayed-Gamma Signature Calculation for Neutron-Induced Fission and Activation Using MCNPX"
a_gauss = .0005797 #keV
b_gauss = .0007192 #keV
c_gauss = 1. #keV

spectrum_file_location = 'radioxenon_ml/spectrum_gen/'  #file location
file_end ='_coin.txt'

for i in range(0,n):    #plot all 6 radioxenon files
    if i == 0:
        isotope = '131m'
    elif i == 1:
        isotope = '133m'
    elif i == 2:
        isotope = '135'
    elif i == 3:
        isotope = '133gb'
    elif i == 4:
        isotope = '133xb'
    elif i == 5:
        isotope = '133xe'

    #read out coincidence data and scale by 1000 (to put into keV instead of MeV)
    c_data = np.loadtxt(spectrum_file_location+isotope+file_end, skiprows=1)    

    c_data[:,(2,3)] *= 1000
    
    #Gaussian broadening, a + b*sqrt(E + c*E^2)
    #c_data[:,(2,3)] = np.ceil(np.random.normal(c_data[:,(2,3)], a_gauss + b_gauss*sqrt(c_data[:,(2,3)] + c_gauss*c_data[:,(2,3)]^2))
    c_data[:,(2,3)] = np.ceil(np.random.normal(c_data[:,(2,3)], (0.17/2.35)*c_data[:,(2,3)]))
    if i==0:
        c_data_total = c_data[:,(2,3)]
    elif i>2:
        c_data_total = np.concatenate((c_data_total,c_data[0:np.int(np.ceil(np.shape(c_data)[0]/3)),(2,3)]),axis=0)
        if n==6:
            if i==3:
                spec133 = c_data[0:np.int(np.ceil(np.shape(c_data)[0]/3)),(2,3)]
            else:
                spec133 = np.concatenate((spec133,c_data[0:np.int(np.ceil(np.shape(c_data)[0]/3)),(2,3)]),axis=0)
        #print(np.shape(c_data[0:np.int(np.ceil(np.shape(c_data)[0]/3)),(2,3)]))
    else:
        c_data_total = np.concatenate((c_data_total,c_data[:,(2,3)]),axis=0)
    
    # pp.ax.set_title('axes title')
    fig = pp.figure()
    pp.xlabel('Summed energy deposited in PIPSBox (keV)')
    pp.ylabel('Summed energy deposited in SrI$_2$(Eu) (keV)')

    spectrum = pp.hist2d(c_data[:,3],c_data[:,2], bins=[bin_num_x,bin_num_y], range=[[x_min,x_max],[y_min,y_max]])
    """
    if i==0:
        spectrum_total = np.zeros(np.shape(spectrum[0]))
    spectrum_total = spectrum[0]+spectrum_total
    """
    pp.set_cmap('jet')
    pp.colorbar()
    pp.show()
    if saveplot == 1:
        if n==6:
            if i < 3:
                print(np.shape(c_data))
                fig.savefig('radioxenon_ml/test_files/'+isotope + '.svg', format='svg')
                np.savetxt('radioxenon_ml/test_files/test'+str(start_test_num+i) + '.csv', spectrum[0],'%6.0f', delimiter=',')
            elif i == 5:
                del fig
                fig = pp.figure()
                pp.xlabel('Summed energy deposited in PIPSBox (keV)')
                pp.ylabel('Summed energy deposited in SrI$_2$(Eu) (keV)')
                spectrum = pp.hist2d(spec133[:,1],spec133[:,0], bins=[bin_num_x,bin_num_y], range=[[x_min,x_max],[y_min,y_max]])
                pp.set_cmap('jet')
                pp.colorbar()
                pp.show()
                print(np.shape(spec133))
                fig.savefig('radioxenon_ml/test_files/'+ '133combined' + '.svg', format='svg')
                np.savetxt('radioxenon_ml/test_files/test'+str(start_test_num+3) + '.csv', spectrum[0],'%6.0f', delimiter=',')        
        else:
            fig.savefig('radioxenon_ml/test_files/'+isotope + '.svg', format='svg')
            np.savetxt('radioxenon_ml/test_files/test'+str(start_test_num+i) + '.csv', spectrum[0],'%6.0f', delimiter=',')                
            
     
# experimental spectrum
fig = pp.figure()
pp.xlabel('Summed energy deposited in PIPSBox (keV)')
pp.ylabel('Summed energy deposited in SrI$_2$(Eu) (keV)')
spectrum = pp.hist2d(c_data_total[:,1],c_data_total[:,0], bins=[bin_num_x,bin_num_y], range=[[x_min,x_max],[y_min,y_max]])
spectrum_exp=(spectrum[0]/n)
pp.set_cmap('jet')
pp.colorbar()
pp.show()
if saveplot == 1:    
    fig.savefig('radioxenon_ml/test_files/experimental.svg', format='svg')
    if n == 6:
        np.savetxt('radioxenon_ml/test_files/test'+str(start_test_num+4) + '.csv', spectrum_exp,'%6.0f', delimiter=',')
    else:
        np.savetxt('radioxenon_ml/test_files/test'+str(start_test_num+n) + '.csv', spectrum_exp,'%6.0f', delimiter=',')
    print(np.shape(c_data_total))