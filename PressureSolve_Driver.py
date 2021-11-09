#At locked temperatures, generate pressure vs Isp
from typing import Final
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


#Set Const
R = 8.314 #kj/kmol-K
g0 = 9.81 #m/s^2

#Control Var
PList = np.linspace(0.1,10,100) #must match matlab
TempLock = [5000,10000,15000,20000]
Pcolor = {
    20000:{'r': 0,'b': 255,'g': 150},
    15000: {'r': 0,'b': 255,'g': 50} ,
    10000: {'r': 92,'b': 116, 'g': 92},
    5000: {'r': 52,'b': 116, 'g': 52},
}

fig = plt.figure()
ax = plt.gca()

DefR, DefG, DefB = 0,0,0#255, 0, 200
ColorDict = {}
Index = 0
for T in TempLock:
    #Color mix
    Red,Green,Blue = Pcolor[T]["r"],Pcolor[T]["g"],Pcolor[T]["b"]
    Hue,Sat,Val = colorsys.rgb_to_hsv(Red/255, Green/255, Blue/255)
    #FinalColor = colorsys.hsv_to_rgb(Hue,1,1-0.5*(20000-T)/20000)
    FinalColorEquil = colorsys.hsv_to_rgb(((0.04-0.035*Index)%1), 0.8,1)
    FinalColorFrozen = colorsys.hsv_to_rgb(((0.586+0.038*Index)%1), 0.8,1)

    #ColorDict[T] = FinalColor
    #Call class ImpulseCalculator but for an unintended purpose
    H_bar = HIspComputer.ImpulseCalculator()
    H_Froz = HIspComputer.ImpulseCalculator()

    FrozList = H_Froz.computeIsp_TempLockFrozen(PList,T)
    IspList = H_bar.computeIsp_TempLock(PList, T)
    labeltxt = "{} K".format(T)
    if T >= 10000: labeltxt =  f"{T:,d}"+" K"
    plt.plot(PList, IspList,label = labeltxt, color = FinalColorEquil, LineWidth = 2)
    plt.plot(PList, FrozList,label = labeltxt, color = FinalColorFrozen, LineStyle = '--', LineWidth = 2)


    Index +=1 


# #xvals = [1,1,1,1]
# lines = plt.gca().get_lines()
# truelines = lines[:3]
# l1=lines[-1]
# labelLines(truelines, zorder=2,align = True,fontsize=12)
# labelLine(l1, 1, ha='left', va = "bottom", align=True)
#Sanity Check:
#P = [0.1,1,10]
# T_5000  = [2557.032589,     2518.761399,    2275.646942]
# T_10000 = [3297.714837,     3066.442158,    2988.075577]
# T_15000 = [6271.53764,  	5092.312829,	4020.54261]
# T_20000 = [6977.077734, 	6828.444858,	6010.591356]
# plt.scatter(P,T_5000, color = ColorDict[5000])
# plt.scatter(P,T_10000,color = ColorDict[5000])
# plt.scatter(P,T_15000,color = ColorDict[5000])
# plt.scatter(P,T_20000,color = ColorDict[5000])

#plt.legend()
plt.xlabel("Pressure [Bar]")#$\mathit{Bar}$")
plt.ylabel("Specific Impulse [s]")#$\mathit{s}$")

ax.set_xscale('log')
ax.minorticks_on()
#ax.set_yscale('log')
# ax.get_yaxis().set_major_formatter(
#     mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
ax.get_xaxis().set_major_formatter(
    mtick.FormatStrFormatter('%.1f')) #change f to e for scientific


ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.yticks(np.arange(0, 7000+1, 1000))
plt.xticks([0.1,1,10])


plt.xlim(left = 0.1, right = 10)
plt.ylim(bottom = 1000, top = 7000)
#need to put contours
top = 'top'
bot = 'bottom'
ctr = 'center'
labelpos = {
    #equil
    0: [5,    ctr],
    2: [5,    ctr],
    4: [5,      ctr],
    6: [5,      ctr],
    #Frozen
    1: [0.2,   ctr],
    3: [0.2,    ctr],
    5: [0.2,    bot],
    7: [0.2,      ctr],
}
for i in [0,1,2,3,4,5,6,7]:
    lines = plt.gca().get_lines()
    l1 = lines[(i)]
    labelLine(l1, labelpos[i][0], va = labelpos[i][1], align=True)


plt.savefig("Figs\ISP_PressureGradient.eps")
plt.show()
