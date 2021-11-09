import math
import numpy as np 
import csv

R = 8.314 #kj/kmol-k

def EvaluateConstants(T, consts):
    #Unpack constants and ensure all values are float type to avoid type error shenanigans
    a1 = float(consts[0]) ; a2 = float(consts[1]) ; a3 = float(consts[2]) ; a4 = float(consts[3]) ; a5 = float(consts[4]) 
    a6 = float(consts[5]) ; a7 = float(consts[6]) ; b1 = float(consts[7]) ; b2 = float(consts[8]) ; T = float(T)
    #Cp(T)/R
    
    Cp_R = a1*T**(-2)    +   a2*T**(-1)   +   a3  +   a4*T    +   a5*T**2  +   a6*T**3  +   a7*T**4

    h_RT = -a1*T**(-2)   +   a2*math.log(T)*T**(-1)   +   a3  +   a4*T/2  +   (a5*(T**2))/3    +(a6*(T**3))/4   +   (a7*(T**4))/5    +   b1/T
   
    so_R = -a1*(T**(-2))/2   -   a2*(T**-1)   +   a3*math.log(T)  +   a4*T    +   a5*(T**2)/2  +   a6*(T**3)/3  +   a7*(T**4)/4  +   b2

    return Cp_R, h_RT, so_R

def getPropertyAtTemp(X,T):
    #X is the OOP element species object
    #T is the temperature in kelvin
    X.updateConstants(T)
    Cp_R, h_RT, so_R = EvaluateConstants(T,X.getConstantList())

    return Cp_R*R, h_RT*T*R, so_R*R

def getPropertyList(X, start = 298, end = 5000, resolution = 1000):
    #X is the OOP element species object
    TScale = np.linspace(start,end,resolution)
    Cp = []; h = []; so = []

    for T in TScale:
        X.updateConstants(T)
        myCp, myH, mySo = EvaluateConstants(T,X.getConstantList())
        list.append(Cp,myCp*R)
        list.append(h,myH*T*R)
        list.append(so,mySo*R)

    #Pack into dict
    ThermoProp = {}
    ThermoProp["Temperature"] = TScale
    ThermoProp["GasConstant"] = Cp
    ThermoProp["Enthalpy"] = h
    ThermoProp["Entropy"] = so

    return ThermoProp

def exportToCSV(ThermoProp,filename):
    TScale = ThermoProp["Temperature"]
    Cp = ThermoProp["GasConstant"]
    h = ThermoProp["Enthalpy"]
    so = ThermoProp["Entropy"]

    #Transform to CSV
    fields = ['T','Cp', 'h', 'so']
    fullList = []
    for i in range(len(TScale)):
        row = []
        list.append(row, TScale[i])
        list.append(row, Cp[i])
        list.append(row, h[i])
        list.append(row, so[i])
        list.append(fullList, row)

    with open(filename,'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(fullList)

def getGibbs(X,T):
    #X is the species OOP
    #T is the temp in K
    Cp, h, so = getPropertyAtTemp(X,T)
    return (h-T*so)#+ 8314*T*math.log(P))
    
def QuadraticSolve(a1=1,b1=0,c1=0):
   
    a = float(a1)
    b = float(b1)
    c = float(c1)

    if a == 0:
        ValueError("This is not 2nd order.")

    rt = b**2-4*a*c
    if rt < 0:
        ValueError("Inside root is negative")
    num1 = -b + math.sqrt(rt)
    num2 = -b - math.sqrt(rt)
    denom = 2*a

    sol1 = num1/denom
    sol2 = num2/denom
    return sol1, sol2


    