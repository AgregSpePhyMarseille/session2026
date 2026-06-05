#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


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



def calcule_z_score_moyennes(mu1, err1, mu2, err2):
    return (mu1 - mu2) / np.sqrt(err1**2 + err2**2)


# In[37]:


rho_glyc = 1260.4
eta_glyc = 1.49
acc_g = 9.81

h_max = 220* 10**-3
h_min = 40* 10**-3
d = h_max - h_min

m_bille = np.array([0.286,0.167,0.088,0.034]) * 10**-3
r_bille = np.array([6.0, 5.0, 4.0, 3.0])/2 * 10**-3
rho_bille = m_bille/(4/3*np.pi*r_bille**3)
rho_bille_mean = np.mean(rho_bille)



t_chutte = np.array([6.23,7.85,12.58, 21.21]) 
v_lim = d/t_chutte


# In[38]:


rho_bille


# In[39]:


x = r_bille**2
y = v_lim
# coef = np.polyfit(x,y,deg=1)
coef, err = calcule_coeff_erreurs(x,y)
fig, ax = plt.subplots()
ax.plot(x, y, 'x')

# ax.plot(add_point[1], add_point[0], 'rx')

x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )

ax.set_xlabel(r"$r_{bille}^2$", fontsize=15)
ax.set_ylabel(r"$v_{lim}$", fontsize=15)
ax.set_title(r"Régression linéaire : y =" + str(round(coef[0],3)) + "x  + " + str(round(coef[1],3)), fontsize=18)


# In[45]:


eta_exp = (2/9*acc_g*(rho_bille_mean-rho_glyc))/coef[0]


# In[46]:


eta_exp


# In[47]:


err[0]/coef[0]*eta_exp


# In[44]:


np.std(rho_bille)/np.mean(rho_bille)


# In[ ]:




