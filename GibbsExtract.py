"""
GibbsExtract.py
Export equilibrium constants Kp for Disassocation and Ionization reactions for a specified range of Prange and Trange.
The default is [5000,20000] at 10,000 elements. This should be the same at Matlab for consistency.

"""

print("Executing Code")

import csv
from csv import writer

import math
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt 

from ElementConst import Hydrogen, DiHydrogen, HydrogenP, Electron
import TempFuncs

#Set Const
R = 8.314 #kj/kmol-K
g0 = 9.81 #m/s^2
MW_H2 = 2 #kg/kmol
MW_Hp = 1.008 #kg/kmol
#Set Maximums
TRange = np.linspace(5000,20000,10000) #K
PRange = [1] #bar

#Get required Species
Hp = HydrogenP.Species(); N_Hp = 1
H2 = DiHydrogen.Species();  N_H2 = 1
H = Hydrogen.Species();     N_H = 2
e_minus = Electron.Species(); N_e = 1

#Single Case
T_single = 298
G_diss = 2*TempFuncs.getGibbs(H,T_single) - TempFuncs.getGibbs(H2,T_single)
lnkp_Diss = -G_diss/(T_single*R)
kp_Diss = math.e**(lnkp_Diss)

G_ion = TempFuncs.getGibbs(e_minus,T_single) + TempFuncs.getGibbs(Hp,T_single) - TempFuncs.getGibbs(H,T_single)
lnkp_ion = -G_ion/(T_single*R)
kp_ion = math.e**(lnkp_ion)
print("Single case Run \n Kp_Diss: {a} \n Kp_Ion: {b}".format(a = kp_Diss, b = kp_ion))

#PREPARE DATA
for P in PRange:
    Patm = P * 0.986923 #atm
    Kp_Dict = {}
    Kp_DissList = []
    Kp_IonList = []
    for T in TRange:
        #print("Current T: ", T)
        #DISSASSOCIATION EQUATION
        G1 = 2*TempFuncs.getGibbs(H,T) - TempFuncs.getGibbs(H2,T)
        lnk_p1 = -(G1/(T*R))
        k_p1 = math.e**(lnk_p1)
        
        #IONIZATION EQUATION
        G2 = TempFuncs.getGibbs(e_minus,T) + TempFuncs.getGibbs(Hp,T) - TempFuncs.getGibbs(H,T)
        lnk_p2 = -(G2/(T*R))
        k_p2 = math.e**(lnk_p2)
        
        if T == 298.15:
            print("Current T: ", T)
            print("Dissassociation Kp", k_p1)
            print("Ionization Kp", k_p2)

        Kp_Dict[T] = [k_p1, k_p2]

    #To CSV!
    with open('KpVals.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in Kp_Dict.items():
            writer.writerow([key, value[0], value[1]])
print("Finished.")