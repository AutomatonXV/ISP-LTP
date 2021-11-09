import numpy as np
import numpy.polynomial.polynomial as poly

import matplotlib as mpl
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick

import math
#Constants
g0 = 9.81 #m/s2

#Datapoints, at 10000K
T_ch_CEA = 10002.44 #K
Isp_AlphaBeta =3066.44 #s

Pc_Pe = np.array([10e7,10e8,10e9,10e10,10e11,10e12,10e13,10e14])
V_ex = np.array([28337.5, 
                 28860.0,
                 29305.2,
                 29517.3,
                 29890.6,
                 29997.3,
                 30051.4,
                 30077.2,
                 ])
Isp_CEA = V_ex/g0
Rel_Err = 100*(abs((Isp_CEA-Isp_AlphaBeta))/(Isp_CEA))


fig = plt.figure()
ax = plt.gca()
ax.grid(b=None, which='major', axis='both', color = 'k')

ax.scatter(Pc_Pe,Rel_Err)
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlabel("Pressure Ratio (Pc/Pe)")
ax.set_ylabel("Rel Error to CEA (%)")
plt.axvline(x=10e15, linestyle = '--', color = 'r')


ax.get_yaxis().set_major_formatter(mtick.FormatStrFormatter('%.3f')) #change f to e for scientific

plt.xlim(right = 10e16, left = 10e6)
plt.ylim(top = 10, bottom = 0.0001)
#plt.yticks([0.0001,0.1,1,10])  # Set label locations.
plt.show()