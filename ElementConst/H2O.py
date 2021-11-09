class Species:
    def __init__(self):
        #Set all thermodynamic constants
        self.M = 18.0152800 #molar mass, kg/kmol
        
        self.hf = -241826.000 #enthalpy of formation, Kj/kmol
        self.gf = 0 #gibbs func of formation, kj/kmol
        self.s_abs = 0 #absolute entropy

        self.a1 = 0; self.a2 = 0; self.a3 = 0; self.a4 = 0; self.a5 = 0; self.a6 = 0; self.a7= 0
        self.b1 = 0; self.b2 = 0
        
    def getConstantList(self):
        return [self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.b1,self.b2]
    
    def updateConstants(self,T):
        if T < 1000:
            self.a1 = -3.9476083*10**4
            self.a2 = 5.75573102*10**2
            self.a3 = 9.31782653*10**(-1)
            self.a4 = 7.222712860*10**(-3)
            self.a5 = -7.342557370*10**(-6)
            self.a6 = 4.955043490*10**(-9)
            self.a7 = -1.336933246*10**(-12)
            self.b1 = -3.303974310*10**4
            self.b2 = 1.724205775*10**1
        elif T >= 1000 and T < 6000:
            self.a1 = 1.034972096*10**6
            self.a2 = -2.412698562*10**3
            self.a3 = 4.646110780*10**0
            self.a4 = 2.291998307*10**(-3)
            self.a5 = -6.836830480*10**(-7)
            self.a6 = 9.426468930*10**(-11)
            self.a7 = -4.822380530*10**(-15)
            self.b1 = -1.384286509*10**4
            self.b2 = -7.978148510*10**0
        elif T >= 6000:
            self.a1 = 1.034972096*10**6
            self.a2 = -2.412698562*10**3
            self.a3 = 4.646110780*10**0
            self.a4 = 2.291998307*10**(-3)
            self.a5 = -6.836830480*10**(-7)
            self.a6 = 9.426468930*10**(-11)
            self.a7 = -4.822380530*10**(-15)
            self.b1 = -1.384286509*10**4
            self.b2 = -7.978148510*10**0

        

    


