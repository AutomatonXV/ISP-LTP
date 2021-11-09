class Species:
    def __init__(self):
        #Set all thermodynamic constants
        self.M = 1.00794 #molar mass, kg/kmol
        
        self.hf = 217999.828 #enthalpy of formation, Kj/kmol
        self.gf = 203290 #gibbs func of formation, kj/kmol
        self.s_abs = 114.72 #absolute entropy

        self.a1 = 0; self.a2 = 0; self.a3 = 0; self.a4 = 0; self.a5 = 0; self.a6 = 0; self.a7= 0
        self.b1 = 0; self.b2 = 0
        
    def getConstantList(self):
        return [self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.b1,self.b2]
    
    def updateConstants(self,T):
        if T < 1000:
            self.a1 = 0
            self.a2 = 0
            self.a3 = 2.5
            self.a4 = 0
            self.a5 = 0
            self.a6 = 0
            self.a7 = 0
            self.b1 = 2.547370801*10**4 
            self.b2 = -4.466828530*10**-1
        elif T >= 1000 and T < 6000:
            self.a1 = 6.07877425*10**1 
            self.a2 = -1.819354417*10**-1
            self.a3 = 2.500211817
            self.a4 = -1.226512864*10**-7 
            self.a5 = 3.732876330*10**-11 
            self.a6 = -5.687744560*10**-15
            self.a7 = 3.410210197*10**-19
            self.b1 = 2.547486398*10**4
            self.b2 = -4.481917770*10**-1
        elif T >= 6000:
            self.a1 = 2.173757694*10**8
            self.a2 = -1.312035403*10**5
            self.a3 = 3.399174200*10**1 
            self.a4 = -3.813999680*10**-3
            self.a5 = 2.432854837*10**-7
            self.a6 = -7.694275540*10**-12
            self.a7 = 9.644105630*10**-17
            self.b1 = 1.067638086*10**6
            self.b2 = -2.742301051*10**2

        

    


