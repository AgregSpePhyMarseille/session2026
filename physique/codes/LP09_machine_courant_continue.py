#!/usr/bin/env python
# coding: utf-8

# In[39]:


import numpy as np
import matplotlib.pyplot as plt


# In[40]:


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


# # 1.2.2. Protocole: on varie la charge (que la premiere partie du protocole)

# In[41]:


# on regle la vitesse a 100 tours par second a l'oscillloscope
add_point = [12.7,2.77,0.030]
u_m = np.array([12.2,12.6,12.9, 13.5, 14.1] + [add_point[0]]) # tension d'alimentation du moteur
i_m = np.array([1.92,2.53,3.27,4.06,4.89] + [add_point[1]]) # courant avec difefrents valeur de resistance
gamma_em = np.array([0.018, 0.027, 0.039,0.051,0.064] + [add_point[2]]) # couple em sur le deuxieme
# u_m = np.array([11.9,12.1, 12.5, 12.9]) # tension d'alimentation du moteur
# i_m = np.array([1.89,2.38,2.77, 3.45]) # courant avec difefrents valeur de resistance
# gamma_em = np.array([0.016, 0.024, 0.030, 0.040]) # couple em sur le deuxieme


# ### Coubre U_m = f(I_m) pour determiner la resistance et la constante K' du moteur

# In[42]:


x = i_m
y = u_m
# coef = np.polyfit(x,y,deg=1)
coef, err = calcule_coeff_erreurs(x,y)


# ## On estime la resistance du moteur

# In[43]:


r_m = round(coef[0],3)
r_m_err = round(err[0],3)
print('La resistance du moteur vaut ' + str(r_m) + ' ohm')
print('Et son erreur  vaut ' + str(r_m_err) + ' ohm')


# In[44]:


fig, ax = plt.subplots()
ax.plot(x, y, 'x')

ax.plot(add_point[1], add_point[0], 'rx')

x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )

ax.set_xlabel(r"Courant moteur $I_R$ (A)", fontsize=15)
ax.set_ylabel(r"Tension moteur U (V)", fontsize=15)
ax.set_title(r"Régression linéaire : y =" + str(round(coef[0],3)) + "x  + " + str(round(coef[1],3)), fontsize=18)

plt.show()


# ## On estime K' 

# In[45]:


n_tours = 100
k_prime_1 = round(coef[1],5) / (np.pi*n_tours)
k_prime_err_1 = round(err[1],5) / (np.pi*n_tours)
print('La constante K du moteur vaut ' + str(k_prime_1) )
print('Et son erreur  vaut ' + str(k_prime_err_1))


# In[ ]:





# # 1.3.2. Protocole : on varie la tension sans charge et on mesure la vitesse de rotation

# In[46]:


# u_m = np.array([0,2.0, 4.0, 6.0, 8.0, 10, 12, 14]) # tension d'alimentation du moteur
# i_m = np.array([0,0.65, 0.75, 0.83, 0.88, 0.94, 0.95, 0.97]) # courant avec difefrents valeur de resistance, considerer un offset 0.22 amperes
# n_tours = np.array([0,13.7, 31.3, 48.8, 67, 87, 105, 125]) # tours pas second 

# offset_im = 0.22
# i_m [1:] -= offset_im
u_m = np.array([4.8,6.3,9.8,13.3]) # tension d'alimentation du moteur
i_m = np.array([0.82,0.9,0.97,1.0]) # courant avec difefrents valeur de resistance, considerer un offset 0.22 amperes
n_tours = np.array([30,45,75,106]) # tours pas second 

r_m = 0.8

omega = np.pi * n_tours # en rad s-1
e = u_m - r_m * i_m 


# In[47]:


x = omega
const = 1
y = const*e
# coef = np.polyfit(x,y,deg=1)
coef, err = calcule_coeff_erreurs(x,y)

k_prime_2 = round(coef[0],5)
k_prime_err_2 = round(err[0],5)
print('La constante de couplage du moteur, avec la deuxieme mesure, vaut ' + str(k_prime_2) )
print('Et son erreur  vaut ' + str(k_prime_err_2))


# In[48]:


fig, ax = plt.subplots()
ax.plot(x, y, 'x')
# ax.plot(add_point[1], add_point[2], 'rx')
x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )
ax.set_xlabel(r"Vitesse de rotation $\Omega$ (rad s$^{-1}$)", fontsize=15)
ax.set_ylabel(r" Tension U (V)", fontsize=15)
ax.set_title(r"Régression linéaire : y =" + str(round(coef[0],3)) + "x  " + str(round(coef[1],3)), fontsize=15)

plt.show()


# ## Calcule du z-score

# In[49]:


# mu1 = k_prime
mu1 = k_prime_1
mu2 = k_prime_2
err1 = k_prime_err_1
err2 = k_prime_err_2

zscore = calcule_z_score_moyennes(mu1, err1, mu2, err2)
print('Le zscore entre les deux mesure de la constante de couplage du moteur vaut ' + str(zscore) )


# # Protocole 1.2.2 (deuxieme partie du protocole)
# ### Coubre $T{EM}$ = f(I_M) pour determiner la constante de couplage K' du moteur
# 
# C'est la deuxieme partie du protocole 1.2.2, mais ca marche mal.

# In[50]:


add_point = [12.7,2.77,0.030]
u_m = np.array([12.2,12.6,12.9, 13.5, 14.1] + [add_point[0]]) # tension d'alimentation du moteur
i_m = np.array([1.92,2.53,3.27,4.06,4.89] + [add_point[1]]) # courant avec difefrents valeur de resistance
gamma_em = np.array([0.018, 0.027, 0.039,0.051,0.064] + [add_point[2]]) # couple em sur le deuxieme


# In[51]:


x = i_m
y = gamma_em
coef, err = calcule_coeff_erreurs(x,y)

k_prime_3 = round(coef[0],5)
k_prime_err_3 = round(err[0],5)
print('La constante de couplage du moteur vaut ' + str(k_prime_3) )
print('Et son erreur  vaut ' + str(k_prime_err_3))


# In[52]:


fig, ax = plt.subplots()
ax.plot(x, y, 'x')

ax.plot(add_point[1], add_point[2], 'rx')

x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )

ax.set_xlabel(r"Courant moteur $I_M$ (A)", fontsize=15)
ax.set_ylabel(r"Couple moteur $T_{EM}$ (Nm)", fontsize=15)
ax.set_title(r"Régression linéaire : y =" + str(round(coef[0],3)) + "x  " + str(round(coef[1],3)), fontsize=15)

plt.show()


# In[ ]:





# # 1.4. Variante pour la détermination de la résistance de l'induit (on bloque le moteur)
# 
# Pour ce faire il faut brancher la generatice a l'inverse par rapport au moteur

# In[53]:


u0 = np.array([0.1,0.6, 0.7,0.9,1])
i0 = np.array([0.08,0.44,0.5,0.58, 0.62])


# In[54]:


x = i0
y = u0
# coef = np.polyfit(x,y,deg=1)
coef, err = calcule_coeff_erreurs(x,y)


r_m = round(coef[0],3)
r_m_err = round(err[0],3)
print('La resistance du moteur vaut ' + str(r_m) + ' ohm')
print('Et son erreur  vaut ' + str(r_m_err) + ' ohm')


# In[ ]:


fig, ax = plt.subplots()
ax.plot(x, y, 'x')

# ax.plot(add_point[1], add_point[0], 'rx')

x_estim = np.linspace(np.min(x), np.max(x), 5)
y_estim = coef[0] * x_estim + coef[1]
ax.plot(x_estim, y_estim, '--g' )

ax.set_xlabel(r"Courant moteur $I_R$ (A)", fontsize=15)
ax.set_ylabel(r"Tension moteur U (V)", fontsize=15)
ax.set_title(r"Régression linéaire : y =" + str(round(coef[0],3)) + "x  + " + str(round(coef[1],3)), fontsize=18)

plt.show()


# #  2.3. Protocole: Calcul du rendement
# 
# C'est fait que pour le rendement total (celui appelle $\eta_{TOT}$ dans la notice du moteur Pierron. 
# 
# On peut le faire mieux si on considere le rendement que du moteur,  mais il faut estimer le $T_p(\Omega)$ et c'est long (Il faut regarder la partie 1.3) 
# 
# 

# In[35]:


n = 80 # nombre de tours/s
#omega = 80*2*np.pi 
Tp = 0.01484 # d'apres la notice, valeur pour n=80
Pa =  33.43 # une valeur de puissance absorbe d'apres la notice
Pc = 2*np.pi*n*Tp
Pj = 0.7*2.67**2 # rm = 0.7, im = 2.67*
Ptr = Pa - Pc - Pj

pu = np.array([2.99, 4.7, 7.7])
um = np.array([8.1, 8.2,8.7])
im = np.array([1.4, 1.8,2.5]) 

pu/(um*im)
print(pu)


# In[ ]:




