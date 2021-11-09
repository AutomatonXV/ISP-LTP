"""
Compute the reaction H2 -> [H] + [H2] + [H+] + [e-]
Requires Alpha_BAR[P] and Beta_BAR[P] CSV from Matlab.

"""

#import
import csv
import math
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt 

import colorsys

from ElementConst import Hydrogen, DiHydrogen, HydrogenP, Electron
import TempFuncs

#Def Constants
R = 8.314 #kj/kmol-k
g0 = 9.81 #ms^-2
T0 = 298.15 #K

#init class
class ImpulseCalculator:
    def __init__(self, Pch=1):
        self.P_ch = Pch #Chamber pressure, in bars.
        self.Temp = [] #Temperature list, in K
        self.V_Ex = [] #Exit velocity list, in m/s. Normalize by g_0 for Isp in s.
        self.IspDict = {}
        self.AlphaBetaDict = {}
        self.Alpha_File = "Alpha_BAR"+str(self.P_ch)
        self.Beta_File = "Beta_BAR"+str(self.P_ch)
        self.AlphaList = []
        self.BetaList = []
        #Load in Species
        self.Hp = HydrogenP.Species(); self.N_Hp = 1
        self.H2 = DiHydrogen.Species();  self.N_H2 = 1
        self.H = Hydrogen.Species();     self.N_H = 2
        self.e_minus = Electron.Species(); self.N_e = 1
    
    def extractEqConstants():
        pass
    


    def computeIsp_Equilibrium(self, TRange):
        #Calculate Equilibrium Isp

        #Check dimensions.
        if len(TRange) != len(self.AlphaList) or len(TRange) != len(self.BetaList):
            raise ValueError("Alpha or Beta list is not the same size as Trange")

        #Reset Trange and V_Ex
        self.Temp = []
        self.V_Ex = []
        Index = 0
        for T in TRange:
            Alpha = self.AlphaList[Index]
            Beta = self.BetaList[Index]

            #_1 means reactant, 2 means product
            #Dihydrogen Enthalpies
            _,h_H2_2,_ = TempFuncs.getPropertyAtTemp(self.H2,T)
            _,h_H2_1,_ = TempFuncs.getPropertyAtTemp(self.H2,T0)
            #Hydrogen Enthalpies
            _,h_H_2,_ = TempFuncs.getPropertyAtTemp(self.H,T)
            #Ionic Hydrogen Enthalpies
            _,h_Hp_2,_ = TempFuncs.getPropertyAtTemp(self.Hp,T)
            #Electron enthalpy
            _,h_e_2,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T)

            #At equlibrium condition
            #Moles of species
            #Moles of species (normalize by moltot!!)
            mol_Hp = 2*Alpha*Beta
            mol_e = mol_Hp #2 * Alpha * Beta
            mol_H = ( 2*Beta*(1-Alpha) )
            mol_H2 = (1-Beta)
            molTot = mol_Hp + mol_e + mol_H + mol_H2
            
            #mole fractions
            y_Hp = mol_Hp/molTot
            y_e = mol_e/molTot
            y_H = mol_H/molTot
            y_H2 = mol_H2/molTot

            #molecular weight average
            MW_Avg = y_H2*self.H2.M + y_H*self.H.M + y_Hp*self.Hp.M + y_e*self.e_minus.M  
            #Mass of species #m = mM
            mass_Hp = mol_Hp*self.Hp.M
            mass_e = mol_e*self.e_minus.M #This should be so small its negligeable
            mass_H = mol_H*self.H.M
            mass_H2 = mol_H2*self.H2.M
            massTot= mass_Hp + mass_H + mass_e + mass_H2

            #Mass fractions
            x_Hp = y_Hp*self.Hp.M/MW_Avg
            x_e = y_e*self.e_minus.M/MW_Avg
            x_H = y_H*self.H.M/MW_Avg           
            x_H2 = y_H2*self.H2.M/MW_Avg
            
            #delta_H = (mol_H2)*h_H2_2 + (mol_H)*h_H_2 + (mol_Hp)*h_Hp_2 + (mol_e)*h_e_2
            #Q = delta_H*1000*0.5 #At the end its all H2, so divide by MH_H2 
            H = (x_H2*h_H2_2/self.H2.M) + (x_H*h_H_2/self.H.M) + (x_Hp*h_Hp_2/self.Hp.M) + (x_e*h_e_2/self.e_minus.M)
            H_ref = (h_H2_1/self.H2.M)
            delta_H = H - H_ref
            V = math.sqrt(2*(delta_H)*1000)
            self.V_Ex.append(V); self.Temp.append(T)
            
            Index = Index+1
        TempV = self.V_Ex
        TempT = self.Temp
        self.V_Ex = np.array(TempV)
        self.Temp = np.array(TempT)
        self.DictFormat()
        return self.V_Ex, self.Temp

    def computeIsp_Frozen(self,TRange):
        if len(TRange) != len(self.AlphaList) or len(TRange) != len(self.BetaList):
            raise ValueError("Alpha or Beta list is not the same size as Trange. Have you loaded alpha/beta list?")
        
        self.Temp = []
        self.V_Ex = []
        Index = 0
        lockAlpha = self.AlphaList[0]
        lockBeta = self.BetaList[0]

        #1 bar, 5000, molfracs: H = 0.95497, H2 = 0.04503
        #reversing to get alpha and beta
        #1-molfracH2 = beta
        #2b(1-a) = molfrac_H -> 1-a = H/2b -> 1-H/2b = a
        #lockBeta = 1-0.04503
        #lockAlpha = 1-0.95497/(2*lockBeta)
        
        
        for T in TRange:
            Alpha = self.AlphaList[Index] #lockAlpha
            Beta =  self.BetaList[Index] #lockBeta
            Cp_H2_2,h_H2_2,_ = TempFuncs.getPropertyAtTemp(self.H2,T)
            Cp_H2_1,h_H2_1,_ = TempFuncs.getPropertyAtTemp(self.H2,T0) #corresponds to enthalpy of formation
            #Hydrogen Enthalpies
            Cp_H_2,h_H_2,_ = TempFuncs.getPropertyAtTemp(self.H,T)
            Cp_H_1,h_H_1,_ = TempFuncs.getPropertyAtTemp(self.H,T0) #this corresponds to enthalpy of formation
            #Ionic Hydrogen Enthalpies
            Cp_Hp_2,h_Hp_2,_ = TempFuncs.getPropertyAtTemp(self.Hp,T)
            Cp_Hp_1,h_Hp_1,_ = TempFuncs.getPropertyAtTemp(self.Hp,T0)

            #Electron enthalpy
            Cp_e_2,h_e_2,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T)
            Cp_e_1,h_e_1,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T0)
            
            #Moles of species (normalize by moltot!!)
            mol_Hp = 2*Alpha*Beta
            mol_e = mol_Hp #2 * Alpha * Beta
            mol_H = ( 2*Beta*(1-Alpha) )
            mol_H2 = (1-Beta)
            molTot = mol_Hp + mol_e + mol_H + mol_H2
            
            #mole fractions
            y_Hp = mol_Hp/molTot
            y_e = mol_e/molTot
            y_H = mol_H/molTot
            y_H2 = mol_H2/molTot

            #molecular weight average
            MW_Avg = y_H2*self.H2.M + y_H*self.H.M + y_Hp*self.Hp.M + y_e*self.e_minus.M  
            #Mass of species #m = mM
            mass_Hp = mol_Hp*self.Hp.M
            mass_e = mol_e*self.e_minus.M #This should be so small its negligeable
            mass_H = mol_H*self.H.M
            mass_H2 = mol_H2*self.H2.M
            massTot= mass_Hp + mass_H + mass_e + mass_H2

            #Mass fractions
            x_Hp = y_Hp*self.Hp.M/MW_Avg
            x_e = y_e*self.e_minus.M/MW_Avg
            x_H = y_H*self.H.M/MW_Avg           
            x_H2 = y_H2*self.H2.M/MW_Avg
            
            #NEW
            H = (x_H2*h_H2_2/self.H2.M) + (x_H*h_H_2/self.H.M) + (x_Hp*h_Hp_2/self.Hp.M) + (x_e*h_e_2/self.e_minus.M)
            H_Froz = (x_H2*h_H2_1/self.H2.M) + (x_H*h_H_1/self.H.M) + (x_Hp*h_Hp_1/self.Hp.M) + (x_e*h_e_1/self.e_minus.M)
            
            delta_H = H - H_Froz
            V = math.sqrt(2*delta_H*1000 )
            self.V_Ex.append(V); self.Temp.append(T)

            if T == 15000:
                print("MW AVERAGE: ",MW_Avg)
            Index+=1
        
        TempV = self.V_Ex
        TempT = self.Temp
        self.V_Ex = np.array(TempV)
        self.Temp = np.array(TempT)
        self.DictFormat()
        return self.V_Ex, self.Temp





    def findClosestT(self, ReqT):
        ClosestTemp = None
        for T in self.Temp:
            if ClosestTemp == None:
                ClosestTemp = T
            if abs(ReqT-T) < abs(ReqT-ClosestTemp):
                ClosestTemp = T
        return ClosestTemp

    def GetIspAt(self, ReqT):
        T_Key = self.findClosestT(ReqT)
        if T_Key == None: return ValueError("T IS NOT FOUND")
        Isp = self.IspDict[T_Key]
        return Isp

    def PrintOutputAt(self,ReqT):
        T_Key = self.findClosestT(ReqT)
        if T_Key == None:
            raise ValueError("T IS NOT FOUND")

        Isp = self.IspDict[T_Key]
        AlphaBeta = self.AlphaBetaDict[T_Key]
        Alpha,Beta = AlphaBeta[0], AlphaBeta[1]
        #Moles of species
        mol_Hp = 2*Alpha*Beta
        mol_e = mol_Hp #2 * Alpha * Beta
        mol_H = ( 2*Beta*(1-Alpha) )
        mol_H2 = (1-Beta)
        molTot = mol_Hp + mol_e + mol_H + mol_H2

        mass_Hp = mol_Hp*self.Hp.M
        mass_e = mol_e*self.e_minus.M
        mass_H = mol_H*self.H.M
        mass_H2 = mol_H2*self.H2.M
        massTot = mass_H + mass_H2 + mass_Hp + mass_e

        print("Temperature: ", T_Key)
        print("ISP", Isp)
        print("Alpha: ",Alpha)
        print("Beta: ", Beta)
        print("Mass frac H2", mass_H2/massTot)
        print("Mass frac H", mass_H/massTot)
        print("Mass frac Hp", mass_Hp/massTot)
        print("Mass frac e", mass_e/massTot)

        # print("Mol frac H2", mol_H2/molTot)
        # print("Mol frac H", mol_H/molTot)
        # print("Mol frac Hp", mol_Hp/molTot)


  


    def DictFormat(self):
        #Format Temp (key) to Isp (val) for easiness
        i = 0
        for T in self.Temp:
            self.IspDict[T] = self.V_Ex[i]
            self.AlphaBetaDict[T] = [self.AlphaList[i], self.BetaList[i]]
            i+=1

    def LoadAlphaBeta(self):
        #Into method to avoid init crash
        with open(self.Alpha_File) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    self.AlphaList.append(float(x))

        with open(self.Beta_File) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    self.BetaList.append(float(x))

    def computeIsp_TempLock(self,PList,Temperature):
        #Special method
        #at locked temperature Temp, calculate Pressure vs Isp
        
        #Get required Species
        Hp = HydrogenP.Species(); N_Hp = 1
        H2 = DiHydrogen.Species();  N_H2 = 1
        H = Hydrogen.Species();     N_H = 2
        e_minus = Electron.Species(); N_e = 1
        
        AlphaList = []
        BetaList = []
        g0 = 9.81

        with open("Alpha_BAR_"+str(Temperature)+"K") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    AlphaList.append(float(x))

        with open("Beta_BAR_"+str(Temperature)+"K") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    BetaList.append(float(x))
        
        Isp = []
        Index = 0
        for P in PList:
            Alpha = AlphaList[Index]
            Beta = BetaList[Index]
            T = Temperature
            #_1 means reactant, 2 means product
            #Dihydrogen Enthalpies
            _,h_H2_2,_ = TempFuncs.getPropertyAtTemp(self.H2,T)
            _,h_H2_1,_ = TempFuncs.getPropertyAtTemp(self.H2,T0)
            #Hydrogen Enthalpies
            _,h_H_2,_ = TempFuncs.getPropertyAtTemp(self.H,T)
            #Ionic Hydrogen Enthalpies
            _,h_Hp_2,_ = TempFuncs.getPropertyAtTemp(self.Hp,T)
            #Electron enthalpy
            _,h_e_2,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T)

            #At equlibrium condition
            #Moles of species
            #Moles of species (normalize by moltot!!)
            mol_Hp = 2*Alpha*Beta
            mol_e = mol_Hp #2 * Alpha * Beta
            mol_H = ( 2*Beta*(1-Alpha) )
            mol_H2 = (1-Beta)
            molTot = mol_Hp + mol_e + mol_H + mol_H2
            
            #mole fractions
            y_Hp = mol_Hp/molTot
            y_e = mol_e/molTot
            y_H = mol_H/molTot
            y_H2 = mol_H2/molTot

            #molecular weight average
            MW_Avg = y_H2*self.H2.M + y_H*self.H.M + y_Hp*self.Hp.M + y_e*self.e_minus.M  
            #Mass of species #m = mM
            mass_Hp = mol_Hp*self.Hp.M
            mass_e = mol_e*self.e_minus.M #This should be so small its negligeable
            mass_H = mol_H*self.H.M
            mass_H2 = mol_H2*self.H2.M
            massTot= mass_Hp + mass_H + mass_e + mass_H2

            #Mass fractions
            x_Hp = y_Hp*self.Hp.M/MW_Avg
            x_e = y_e*self.e_minus.M/MW_Avg
            x_H = y_H*self.H.M/MW_Avg           
            x_H2 = y_H2*self.H2.M/MW_Avg
            
            #delta_H = (mol_H2)*h_H2_2 + (mol_H)*h_H_2 + (mol_Hp)*h_Hp_2 + (mol_e)*h_e_2
            #Q = delta_H*1000*0.5 #At the end its all H2, so divide by MH_H2 
            H = (x_H2*h_H2_2/self.H2.M) + (x_H*h_H_2/self.H.M) + (x_Hp*h_Hp_2/self.Hp.M) + (x_e*h_e_2/self.e_minus.M)
            H_ref = (h_H2_1/self.H2.M)
            delta_H = H - H_ref
            V = math.sqrt(2*(delta_H)*1000)
            IspEquil = V/g0

            if Index >=1:
                LastIsp = Isp[Index-1]
                if LastIsp < IspEquil:
                    IspEquil = LastIsp
            Isp.append(IspEquil)
            Index+=1

            if P == 0.1 or P == 1.09 or P == 10:
                print("AT PRESSURE P = "+str(P))
                print("Alpha = "+str(Alpha))
                print("Beta =  "+str(Beta))
                print("=========")
        return Isp

    def computeIsp_TempLockFrozen(self,PList,Temperature):
        #Special method
        #at locked temperature Temp, calculate Pressure vs Isp
        
        #Get required Species
        Hp = HydrogenP.Species(); N_Hp = 1
        H2 = DiHydrogen.Species();  N_H2 = 1
        H = Hydrogen.Species();     N_H = 2
        e_minus = Electron.Species(); N_e = 1
        
        AlphaList = []
        BetaList = []
        g0 = 9.81

        with open("Alpha_BAR_"+str(Temperature)+"K") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    AlphaList.append(float(x))

        with open("Beta_BAR_"+str(Temperature)+"K") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                #each row is a list
                for x in row:
                    #goign through each element
                    BetaList.append(float(x))
        
        Isp = []
        Index = 0
        for P in PList:
            Alpha = AlphaList[Index]
            Beta = BetaList[Index]
            T = Temperature
            #_1 means reactant, 2 means product
            #Dihydrogen Enthalpies
            Cp_H2_2,h_H2_2,_ = TempFuncs.getPropertyAtTemp(self.H2,T)
            Cp_H2_1,h_H2_1,_ = TempFuncs.getPropertyAtTemp(self.H2,T0) #corresponds to enthalpy of formation
            #Hydrogen Enthalpies
            Cp_H_2,h_H_2,_ = TempFuncs.getPropertyAtTemp(self.H,T)
            Cp_H_1,h_H_1,_ = TempFuncs.getPropertyAtTemp(self.H,T0) #this corresponds to enthalpy of formation
            #Ionic Hydrogen Enthalpies
            Cp_Hp_2,h_Hp_2,_ = TempFuncs.getPropertyAtTemp(self.Hp,T)
            Cp_Hp_1,h_Hp_1,_ = TempFuncs.getPropertyAtTemp(self.Hp,T0)

            #Electron enthalpy
            Cp_e_2,h_e_2,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T)
            Cp_e_1,h_e_1,_ = TempFuncs.getPropertyAtTemp(self.e_minus,T0)
            
            #Moles of species (normalize by moltot!!)
            mol_Hp = 2*Alpha*Beta
            mol_e = mol_Hp #2 * Alpha * Beta
            mol_H = ( 2*Beta*(1-Alpha) )
            mol_H2 = (1-Beta)
            molTot = mol_Hp + mol_e + mol_H + mol_H2
            
            #mole fractions
            y_Hp = mol_Hp/molTot
            y_e = mol_e/molTot
            y_H = mol_H/molTot
            y_H2 = mol_H2/molTot

            #molecular weight average
            MW_Avg = y_H2*self.H2.M + y_H*self.H.M + y_Hp*self.Hp.M + y_e*self.e_minus.M  
            #Mass of species #m = mM
            mass_Hp = mol_Hp*self.Hp.M
            mass_e = mol_e*self.e_minus.M #This should be so small its negligeable
            mass_H = mol_H*self.H.M
            mass_H2 = mol_H2*self.H2.M
            massTot= mass_Hp + mass_H + mass_e + mass_H2

            #Mass fractions
            x_Hp = y_Hp*self.Hp.M/MW_Avg
            x_e = y_e*self.e_minus.M/MW_Avg
            x_H = y_H*self.H.M/MW_Avg           
            x_H2 = y_H2*self.H2.M/MW_Avg
            
            #NEW
            H = (x_H2*h_H2_2/self.H2.M) + (x_H*h_H_2/self.H.M) + (x_Hp*h_Hp_2/self.Hp.M) + (x_e*h_e_2/self.e_minus.M)
            H_Froz = (x_H2*h_H2_1/self.H2.M) + (x_H*h_H_1/self.H.M) + (x_Hp*h_Hp_1/self.Hp.M) + (x_e*h_e_1/self.e_minus.M)
            
            delta_H = H - H_Froz
            V = math.sqrt(2*delta_H*1000 )
            IspEquil = V/g0

            if Index >=1:
                LastIsp = Isp[Index-1]
                if LastIsp < IspEquil:
                    IspEquil = LastIsp
            Isp.append(IspEquil)
            Index+=1

            if P == 0.1 or P == 1.09 or P == 10:
                print("AT PRESSURE P = "+str(P))
                print("Alpha = "+str(Alpha))
                print("Beta =  "+str(Beta))
                print("=========")
        return Isp


        