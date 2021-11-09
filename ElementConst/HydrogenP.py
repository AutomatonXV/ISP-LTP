class Species:
    def __init__(self):
        #Set all thermodynamic constants
        self.M = 1.007394 #molar mass, kg/kmol
        
        self.hf = 1536245.928 #enthalpy of formation, Kj/kmol
        self.gf = 0 #gibbs func of formation, kj/kmol
        self.s_abs = 0 #absolute entropy

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
            self.b1 = 1.840214877*10**5
            self.b2 = -1.140646644*10**0
        elif T >= 1000 and T < 6000:
            self.a1 = 0
            self.a2 = 0
            self.a3 = 2.5
            self.a4 = 0
            self.a5 = 0
            self.a6 = 0
            self.a7 = 0
            self.b1 = 1.840214877*10**5
            self.b2 = -1.140646644*10**0
        elif T >= 6000:
            self.a1 = 0
            self.a2 = 0
            self.a3 = 2.5
            self.a4 = 0
            self.a5 = 0
            self.a6 = 0
            self.a7 = 0
            self.b1 = 1.840214877*10**5
            self.b2 = -1.140646644*10**0

        

    


