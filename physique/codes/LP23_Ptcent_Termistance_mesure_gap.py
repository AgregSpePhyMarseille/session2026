#!/usr/bin/env python
# coding: utf-8

# # Mesure du gap du silicium: details du protocol
#
# - On chauffe de l'eau dans un becher
# - On met l'eau dans un un becher avec la thermostance
# - On prent la temperature tout le 2 degree, une vingtaine de mesures
# - Pour le multimetre il suffit de brancher les deux files et appuyer sur le ohms (meme moi j'yarrive)
#
#              $$R_{semicond} = A exp (E_g / 2k_B T)$$
#
#
#

# In[27]:


import numpy as np
import matplotlib.pyplot as plt


# In[28]:


def convert_res_temp(r, r0=100, alpha=0.00385):
    # specifique Ptcent
    theta = (r/r0 -1)/alpha
    return theta


# In[29]:


def calcule_coeff_erreurs(x,y):
    N = len(x)

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    Sxx = np.sum((x - x_mean)**2)
    Sxy = np.sum((x - x_mean)*(y - y_mean))

    # paramètres
    a = Sxy / Sxx
    b = y_mean - a * x_mean

    # variance résiduelle
    residuals = y - (a*x + b)
    s2 = np.sum(residuals**2) / (N - 2)

    # erreurs
    sigma_a = np.sqrt(s2 / Sxx)
    sigma_b = np.sqrt(s2 * (1/N + x_mean**2 / Sxx))

    print(a, sigma_a)
    print(b, sigma_b)

    coef = [a,b]
    err = [sigma_a, sigma_b]
    return coef, err




temp2 = np.array([90, 89,88,86,84,82,80,78,75,73,70,67,64,60,57,52,49])
res_pt = np.array([0.13472,0.13429,0.13389,0.13331,0.13241,0.13155,0.13083,0.13016,0.1289,0.12822,0.1271,0.12580, 0.12475,0.12328,0.12211,0.12013,0.11909])*1000 # ohm
res_thermis = np.array([0.1197,0.1187,0.1202,0.1268,0.1336,0.1414,0.1484,0.1568,0.1730,0.1844,0.2017,0.2235,0.2450,0.2753,0.3066,0.3655,0.4019])*1000  # ohm


# In[32]:


x = temp2
res_pt
y1 = res_thermis
y2 = res_pt
fig, ax = plt.subplots()

ax.plot(x,y1,'x', label="Thermistance")
ax.plot(x,y2,'x', label="Ptcent")

ax.set_xlabel('Temperature (C)')
ax.set_ylabel('Resistance (Ohm)')
ax.legend()
plt.show()


# In[33]:


#res_thermis.size


# In[34]:


temp = convert_res_temp(res_pt) + 273.15
temp


# In[35]:


x = 1/temp[1:]
y = np.log(res_thermis)[1:]



# ax.plot(x,y2,'x', label="Ptcent")

coef, err = calcule_coeff_erreurs(x,y)
fig, ax = plt.subplots()

ax.plot(x,y,'x', label="Thermistance")

# ax.plot(add_point[1], add_point[0], 'rx')

x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )


ax.set_xlabel(r'1/Temperature ($K^{-1}$)')
ax.set_ylabel('Resistance (Ohm)')
ax.legend()
plt.show()


# In[36]:


# Constante de Boltzmann
kB = 8.61733 * 10**-5
Egap = 2* kB * coef[0]
print(f"L'energie du gap vaut: {round(Egap,3)} eV")


# In[26]:


2* kB * coef[0]


# In[ ]:
