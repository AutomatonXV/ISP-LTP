class Species:
    def __init__(self):
        #Set all thermodynamic constants
        self.M = 2.016 #kg/kmol
        self.hf = 0 # enthalpy of formation, Kj/kmol
        self.gf = 0 #gibbs func of formation, kj/kmol
        self.s_abs = 130.68 #absolute entropy

        self.a1 = 0; self.a2 = 0; self.a3 = 0; self.a4 = 0; self.a5 = 0; self.a6 = 0; self.a7= 0
        self.b1 = 0; self.b2 = 0
        
    def getConstantList(self):
        return [self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.b1,self.b2]
    
    def updateConstants(self,T):
        if T < 1000:
            self.a1 = 4.078322810*10**4 
            self.a2 = -8.009185450*10**2
            self.a3 = 8.214701670 
            self.a4 = -1.269714360*10**(-2) 
            self.a5 = 1.753604930*10**(-5)
            self.a6 = -1.202860160*10**(-8)
            self.a7 = 3.368093160*10**(-12)
            self.b1 = 2.682484380*10**3 
            self.b2 = -3.043788660*10**1
        elif T >= 1000 and T < 6000:
            self.a1 = 5.608123380*10**5 
            self.a2 = -8.371491340*10**2
            self.a3 = 2.975363040
            self.a4 = 1.252249930*10**(-3) 
            self.a5 = -3.740718420*10**(-7) 
            self.a6 = 5.936628250*10**(-11)
            self.a7 = -3.606995730*10**(-15)
            self.b1 = 5.339815850*10**3
            self.b2 = -2.202764050
        elif T >= 6000:
            self.a1 = 4.966716130*10**8
            self.a2 = -3.147448120*10**5
            self.a3 = 7.983887500*10**1 
            self.a4 = -8.414504190*10**(-3)
            self.a5 = 4.753060440*10**(-7)
            self.a6 = -1.371809730*10**(-11)
            self.a7 = 1.605374600*10**(-16)
            self.b1 = 2.488354660*10**6
            self.b2 = -6.695524190*10**2