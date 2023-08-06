import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import shahienetal.FluidProperties
import shahienetal.BeegsAndBrell as BB2
import shahienetal.TraverseCurve as pt

def calcDeltaDepths(true_depths:list):
    delta_true_depths = []
    for i in range(len(true_depths) - 1):
        delta_true_depths.append(true_depths[i + 1] - true_depths[i])
    return delta_true_depths

def calcMeasuredDepths(measured_depths:list):
    delta_measured_depths = []
    for i in range(len(measured_depths) - 1):
        delta_measured_depths.append(measured_depths[i + 1] - measured_depths[i])
    return delta_measured_depths

def calcThetas(delta_true_depths:list,delta_measured_depths:list):
    thetas = []
    for i in range(len(delta_true_depths)):
        thetas.append(math.asin(delta_true_depths[i] / delta_measured_depths[i]) * 180 / math.pi)
    return thetas

def calcXs(delta_measured_depths:list,thetas:list):
    x = [0]
    for i in range(len(delta_measured_depths)):
        x.append(delta_measured_depths[i] * math.cos(thetas[i] * math.pi / 180) + x[i])
    return x

def pressure_traverse(liquid_rate,true_depths,measured_depths,tht=150,twf=150,
                      glr=0,wc=0,gas_grav =0.65,oil_grav = 35,wtr_grav = 1.07,diameter=1.922,
                      margin=30,thp=0,sample_size =100):
    delta_true_depths=calcDeltaDepths(true_depths)
    delta_measured_depths=calcMeasuredDepths(measured_depths)
    thetas=calcThetas(delta_true_depths,delta_measured_depths)
    x=calcXs(delta_measured_depths,thetas)

    p = [0]
    depths = [0]
    for i in range(len(thetas)):
        p_temp, depths_temp = pt.pressure_traverse(liquid_rate=liquid_rate, depth=delta_measured_depths[i], tht=tht,
                                                   twf=twf,
                                                   glr=glr, wc=wc, gas_grav=gas_grav, oil_grav=oil_grav,
                                                   wtr_grav=wtr_grav, diameter=diameter, angle=thetas[i], margin=margin,
                                                   thp=p[len(p) - 1])
        p.extend(p_temp)
        depths.extend(np.array(depths_temp) + measured_depths[i])
    return p,depths,x

def plot_traverse(liquid_rate,true_depths,measured_depths,
                  ax=None,tht=150,
                  twf=150,
                  glr=0,
                  wc=0,gas_grav =0.65,oil_grav = 35,wtr_grav = 1.07,
                  diameter=1.922,
                margin=30,thp= 0,sample_size =100):

    p,depths,x=pressure_traverse(liquid_rate=liquid_rate,true_depths=true_depths,measured_depths=measured_depths,
                        tht=tht,twf=twf,
                       glr=glr,wc=wc,gas_grav=gas_grav,oil_grav=oil_grav,
                       wtr_grav=wtr_grav,diameter=diameter,margin=margin,
                       thp=thp,sample_size=sample_size)
    plt.ion()

    plt.subplots(figsize=(18, 10))
    plt.plot(x, true_depths)
    plt.ylabel('Depth ft')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    # Show the minor grid lines with very faint and almost transparent grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.ylim(0, true_depths[len(true_depths) - 1])
    plt.ylim(0, true_depths[len(true_depths) - 1])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gca().invert_yaxis()

    figure, ax = plt.subplots(figsize=(18, 10))
    ax.plot(p, depths, label=f'D = {diameter} inch \n'
                             f'Liquid Rate = {liquid_rate} STB\day \n'
                             f'GLR =  {glr} scf\stb \n'
                             f'wc = {wc}\nGas gravity = {gas_grav} \n'
                             f'Oil gravity=  {oil_grav} API\n'
                             f'Water Gravity = {wtr_grav}\n\n')
    plt.xlabel('Pressure psi')
    plt.ylabel('Depth ft')
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    # Show the minor grid lines with very faint and almost transparent grey lines
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    plt.ylim(0, depths[-1])
    plt.gca().invert_yaxis()
    plt.title("Traverse Curve", size=20, pad=20)