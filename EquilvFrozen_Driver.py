"""
Driver.py
Import IspComputer class to calculate specific impulse
"""
import os
from matplotlib import colors
import numpy as np
import HIspComputer
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt 
import colorsys
import matplotlib.ticker as mtick
import matplotlib.font_manager

#pip install matplotlib-label-lines
from labellines import labelLine, labelLines

myPath = os.path.realpath(__file__) #Get the path of this script
os.chdir(os.path.dirname(myPath))  #set script to parent folder of this script

#Install the font, print(matplotlib.font_manager.findSystemFonts(fontpaths=font_dir, fontext='ttf'))
#find the file dir in which the font is located in the print, copy paste it into font_dir
font_dir = ["C:\\Users\\SinhA\\AppData\\Local\\Microsoft\\Windows\\Fonts"]
for font in matplotlib.font_manager.findSystemFonts(font_dir):
    matplotlib.font_manager.fontManager.addfont(font)
#print(matplotlib.font_manager.findSystemFonts(fontpaths=font_dir, fontext='ttf'))

# Set font family globally
matplotlib.rcParams['mathtext.fontset'] = 'custom' 
matplotlib.rcParams['mathtext.rm'] = 'XCharter' #Roman
matplotlib.rcParams['mathtext.it'] = 'XCharter:italic' #italic
matplotlib.rcParams['mathtext.bf'] = 'XCharter:bold' #bold
matplotlib.rcParams['font.family'] = 'XCharter'
matplotlib.rcParams['font.size'] = 12 

#matplotlib.rcParams['text.usetex'] = True 

#Set Const
R = 8.314 #kj/kmol-K
g0 = 9.81 #m/s^2

PList = [0.1,1,10]#[0.1,1,10]
TRange = np.linspace(5000,20000,10000)

#All CEA data
# CEA_Temp = {
#     0.1: [5000,6000,7000,8000,9000,10000,11000],
#     1: [5000,6000,7000,8000,9000,10000,11000,12000],
#     10: [5000,6000,7000,8000,9000,10000,11000,12000,13000]
# }
# CEA_Isp = {
#     0.1: [2556.87054, 2645.107034, 2732.405708, 2844.556575, 3012.028542, 3294.862579, 3756.360856],
#     1: [2519.724771,2639.571865,2725.056065,2812.721713,2920.050968,3065.973496,3278.491335,3583.62895],
#     10: [2277.135576,2580.9989,2708.695209,2799.194599,2889.734964,2988.73496,3106.503568,3258.685,3454.3934]
# }

# CEA_Frozen = {
#     0.1: [1426.585117, 1568.929664, 1700, 1832.16106, 1964.148828, 2118.399592, None],
#     1: [1425.67788,1568.297655,1699.011213,1827.533129,1944.291539,2072.018349,2208.124363,2369.663609],
#     10: [1416.116208,1572.150866,1704.281346,1824.70948,1942.609582,2055.188583,2172.721713,2295.942915,2422.344546]
# }
# #

Higs_Temp = [5000,10000,15000,20000]
Higs_Isp = {
    0.1: [1418, 2107,3408,4101],
    1: [1414, 2060, 3021, 4043],
    10: [1389,2045, 2705,3734]
}
#Color system
Pcolor = {
    0.1:{'r': 0,'b': 255,'g': 150},
    1: {'r': 0,'b': 255,'g': 50} ,
    10: {'r': 52,'b': 116, 'g': 52},
}
#

fig = plt.figure()
ax = plt.gca()
ax.minorticks_on()

# for p in PList:
#     plt.scatter(Higs_Temp, Higs_Isp[p], color = 'r')

#ax.grid(b=None, which='minor', axis='both', color = 'k')
Index = 0
for P in PList:
    #Color System
    Red,Green,Blue = Pcolor[P]["r"],Pcolor[P]["g"],Pcolor[P]["b"]
    Hue,Sat,Val = colorsys.rgb_to_hsv(Red/255, Green/255, Blue/255)
    Inverted = colorsys.hsv_to_rgb(((Hue+0.5)%1), 1,1)
    TopColor = colorsys.hsv_to_rgb(Hue,1,1-0.5*P/10)
    DarkColor = colorsys.hsv_to_rgb(Hue,0.8,0.8)

    FinalColorEquil = colorsys.hsv_to_rgb(((-0.065+0.035*Index)%1), 0.8,1)
    FinalColorFrozen = colorsys.hsv_to_rgb(((0.7-0.038*Index)%1), 0.8,1)
    #
    #The H in H_Bar stands for "hydrogen". Hence, Hydrogen ISP Calculator 
    H_bar = HIspComputer.ImpulseCalculator(P)
    H_bar.LoadAlphaBeta()
    V_Ex, Temp = H_bar.computeIsp_Equilibrium(TRange)

    H_froz = HIspComputer.ImpulseCalculator(P)
    H_froz.LoadAlphaBeta()
    V_Froz, Temp = H_froz.computeIsp_Frozen(TRange)
    #H_bar.PrintOutputAt(6000)
    plt.plot(Temp, V_Ex/g0, label = str(P)+' bar', color = FinalColorEquil,linewidth = 2)
    plt.plot(Temp, V_Froz/g0, label = str(P)+' bar', linestyle = "--", color = FinalColorFrozen,linewidth = 2)
    #plt.fill(np.append(TRange, TRange[::-1]),np.append(V_Ex/g0, (V_Froz/g0)[::-1]), Color = TopColor, alpha = 0.4, zorder = P)

    #CEA Data
    #CEATemp = CEA_Temp[P] ; CEAIsp = CEA_Isp[P]; CEAFroz = CEA_Frozen[P]
    #plt.plot(CEATemp, CEAIsp, color = TopColor,linestyle = None, marker = "o", markersize = 5, linewidth = 2)
    #plt.plot(CEATemp, CEAFroz, color = DarkColor,linestyle = None, marker = "o", markersize = 5, linewidth = 2)
    # print("PRESSURE: {}".format(P))
    # for T in [5000,10000,15000,20000]:
    #     Isp = H_froz.GetIspAt(T)
    #     print("------------------------------------------")
    #     print("PRESSURE: {}".format(P))
    #     print("TEMP: {} \t | \t ISP: {}".format(T,Isp/9.81))
    #     H_froz.PrintOutputAt(T)

    #print("----------------------")
    #print("PRESSURE ",P)
    #H_froz.PrintOutputAt(5000)
    #H_froz.PrintOutputAt(10000)
    #H_froz.PrintOutputAt(15000)
    #H_froz.PrintOutputAt(20000)
    Index+=1



#plt.axvline(x=13000, linestyle = '--', color = 'r')

#legend specific lines
lines = plt.gca().get_lines()
plt.legend(lines[:2],["Equilibrium","Frozen"], frameon = False)


#Add comas at thousands (ONLY GREATER THAN 10 000!)
xticks = np.arange(0, 20000+1, 2500)
xlist = []
for x in xticks:
    mystr = str(x)
    if x >= 10000:
        mystr = "{:,}".format(x)
    xlist.append(mystr)
ax.set_xticklabels(xlist)

# ax.get_xaxis().set_major_formatter(
#     mtick.FuncFormatter(lambda x, p: format(int(x), ',')))

# ax.get_yaxis().set_major_formatter(
#     mtick.FuncFormatter(lambda x, p: format(int(x), ',')))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#ax.spines['bottom'].set_visible(False)
#ax.spines['left'].set_visible(False)

plt.xticks(np.arange(0, 20000+1, 2500))
plt.yticks(np.arange(0, 7000+1, 1000))

plt.xlim(left = 5000, right = 20000)
plt.ylim(top = 7000, bottom = 1000)
plt.xlabel("Temperature [K]")#$\mathit{K}$")
plt.ylabel("Specific Impulse [s]")#$\mathit{s}$")

labelpos = {
    0: 12500,
    1: 13700,
    2: 14900,
    3: 15700,
    4: 17300,
    5: 17750,
}

for i in [0,1,2,3,4,5]:
    lines = plt.gca().get_lines()
    l1 = lines[(i)]
    labelLine(l1,labelpos[i], align=True, zorder = 3000)

plt.savefig("Figs\ISP_EqvFrz.eps")
plt.show()

