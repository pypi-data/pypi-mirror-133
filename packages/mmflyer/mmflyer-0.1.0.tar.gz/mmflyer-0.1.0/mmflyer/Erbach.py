# -*- coding: utf-8 -*-
#
#   Erbach.py
#   ~~~~~~~~~
#
#   Python implementation of Walter Erbach's C64 Basic program
#   from 1990 NFFS SYmposium (p79-85)
###############################################################
import numpy as np
import pint
import model as m
from model import test_model as t
u = pint.UnitRegistry()


class Erbach(object):

    def __init__(self, model):
        self.model = model

    def query(self, xq, x, y):
        # interpotate/extrapolate evenly spaced data
        n = len(x)
        x_l = x[n-1]
        dx = x[1] - x[0]

        if xq < x[0]:  # extrapolate left side
            print("extrapolate left")
            dydxl = (y[1] - y[0])/(x[1]-x[0])
            return y[0] - dydxl * (x[0] - xq)
        if xq > x[n-1]:
            print("extrapolate right")
            dydxr = (y[n-1] - y[n-2])/(x[n-1]-x[n-2])
            return y[n-1]+dydxr * (xq - x[n-1])
        # handle interpolation
        print("interpolate")
        # find interval for this query
        yq = -100
        for i in range(1,n):
            il = i - 1
            ir = i
            if xq >= x[il] and xq <= x[ir]:
                s = "*"
                yq = y[il] + (y[ir] - y[il])/(x[ir]-x[il])*(xq-x[il])
                break
        return  yq

    def power(self, WI, SA, CG, PCW):
        print(WI, SA, CG, PCW)
        rho = 0.00119
        alpha_w = (WI - SA)   # Wing angle of attack
        alpha_s = (SA)        # Stab angle of attack
        C_lw = self.query(alpha_w, m.alpha, m.C_l)
        C_ls = self.query(alpha_s, m.alpha, m.C_l)
        C_dw = self.query(alpha_w, m.alpha, m.C_d)
        C_ds = self.query(alpha_s, m.alpha, m.C_d)
        print(C_lw, C_ls, C_dw, C_ds)

        VE = (t["WT"]/(0.00119*t["SW"]*(C_lw + PCW*C_ls)))**0.5
        VE2_16 = VE*VE*16
        f1 = rho/2.0*t["SW"]*VE2_16
        AWL = C_ls * f1
        BWD = C_lw * f1
        CTL = C_dw * f1*PCW
        DTD = C_ds * f1*PCW

        PWR= VE*(BWD+DTD)*12
        DW = t["WC"] * (CG -0.25)
        R = SA
        EWLA = t["WH"]*np.sin(R)+DW*np.cos(R)
        FWDA = t["WH"]*np.cos(R)-DW*np.sin(R)
        GTLA = (t["TA"]-DW)*np.cos(R)
        HTDA = (t["TA"]-DW)*np.sin(R)
        JMWL = AWL*EWLA
        KMWD = BWD*FWDA
        LMTL = -CTL*GTLA
        MMTD = DTD*HTDA
        CM = JMWL + KMWD + LMTL + MMTD
        CO = CG*100
        print("VE",VE,"PWR", PWR,"CM", CM,"CO", CO)


if __name__ == '__main__':
    print(t)
    for key in m.test_model:
        print(key,m.test_model[key])
    e = Erbach(m.test_model)
    e.power(4,-2,0.4,0.4)
