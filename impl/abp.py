"""
@author Farzaneh.Tlb
5/13/19 10:52 AM
Implementation of Hodgkin & Huxley (Fill this line)
"""

import scipy as sp
import pylab as plt
from scipy.integrate import odeint
import numpy as np

# Constants
C_m = 1.0  # membrane capacitance, in uF/cm^2
g_Na = 120.0  # maximum conducances, in mS/cm^2
g_K = 36.0
g_L = 0.3
E_Na = 55.0  # Nernst reversal potentials, in mV
E_K = -72.0
E_L = -54.387
# E_L = 10.6


# Channel gating kinetics
# Functions of membrane voltage
def alpha_m(V): return 0.1 * (V + 40.0) / (1.0 - sp.exp(-(V + 40.0) / 10.0))


def beta_m(V):  return 4.0 * sp.exp(-(V + 65.0) / 18.0)


def alpha_h(V): return 0.07 * sp.exp(-(V + 65.0) / 20.0)


def beta_h(V):  return 1.0 / (1.0 + sp.exp(-(V + 35.0) / 10.0))


def alpha_n(V): return 0.01 * (V + 55.0) / (1.0 - sp.exp(-(V + 55.0) / 10.0))


def beta_n(V):  return 0.125 * sp.exp(-(V + 65) / 80.0)


# Membrane currents (in uA/cm^2)
#  Sodium (Na = element name)
def I_Na(V, m, h): return g_Na * m ** 3 * h * (V - E_Na)


#  Potassium (K = element name)
def I_K(V, n):  return g_K * n ** 4 * (V - E_K)


#  Leak
def I_L(V):     return g_L * (V - E_L)


# External current
def I_inj(x, t):  # step up 10 uA/cm^2 every 100ms for 400ms
     y= x * (t > 25.0) - x * (t > 25.2)
     return y


# The time to integrate over
t = sp.arange(0.0,100, .01)


# Integrate!
def dALLdt(X, t , i):
    V, m, h, n = X

    # calculate membrane potential & activation variables
    dVdt = (I_inj(i , t) - I_Na(V, m, h) - I_K(V, n) - I_L(V)) / C_m
    dmdt = alpha_m(V) * (1.0 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1.0 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1.0 - n) - beta_n(V) * n
    return dVdt, dmdt, dhdt, dndt

def get_g_k(n):
    return g_K*n**4

def get_g_Na(m , h):
    return g_Na*(m**3)*h

def parameter_fitting(x1,x2):
    for i in np.arange(x1,x2,1):
        X = odeint(dALLdt, [-60, 0.05, 0.6, 0.3], t, args=(i,))
        V = X[:, 0]
        if(len(np.where(V > 30)[0])>60):
            i1 = i
            for j in np.arange(i1-1,i1,0.01):
                X = odeint(dALLdt, [-60, 0.05, 0.6, 0.3], t, args=(j,))
                V = X[:, 0]
                if (len(np.where(V > 30)[0]) > 60):
                    return j


i = parameter_fitting(0,40)

print("Minimum Current" , i )

X = odeint(dALLdt, [-60, 0.05, 0.6, 0.3], t,(20,))
V = X[:, 0]
m = X[:, 1]
h = X[:, 2]
n = X[:, 3]
ina = I_Na(V, m, h)
ik = I_K(V, n)
il = I_L(V)

plt.figure()

plt.subplot(5, 1, 1)
plt.title('Hodgkin-Huxley Neuron')
plt.plot(t[2000:], V[2000:], 'k')
plt.ylabel('V (mV)')


plt.subplot(5, 1, 2)
plt.plot(t[2000:], get_g_k(n)[2000:], label='$g_{k}$')
plt.plot(t[2000:], get_g_Na(m , h)[2000:], label='$g_{Na}$')
plt.xlabel('t (ms)')
plt.ylabel('$Conductance$')
plt.ylim(-1, 40)
plt.legend()

plt.subplot(5, 1, 3)
plt.plot(t[2000:], m[2000:], 'r', label='m')
plt.plot(t[2000:], h[2000:], 'g', label='h')
plt.plot(t[2000:], n[2000:], 'b', label='n')
plt.ylabel('Gating Value')
plt.legend()

plt.subplot(5, 1, 4)
plt.plot(t[2000:], ina[2000:], 'c', label='$I_{Na}$')
plt.plot(t[2000:], ik[2000:], 'y', label='$I_{K}$')
plt.plot(t[2000:], il[2000:], 'm', label='$I_{L}$')
plt.ylabel('Current')
plt.legend()

plt.subplot(5, 1, 5)
plt.plot(t[2000:], I_inj(20 , t)[2000:], 'k')
plt.xlabel('t (ms)')
plt.ylabel('$I_{inj}$ ($\\mu{A}/cm^2$)')
plt.ylim(-1, 21)

plt.show()

