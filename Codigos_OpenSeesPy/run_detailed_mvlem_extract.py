#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de simulación detallada OpenSeesPy para el modelo de Muros MVLEM de 16 pisos.
Extrae la respuesta paso a paso con:
- Curva de capacidad Pushover
- Perfil de desplazamientos piso a piso y derivas de entrepiso
- Deformaciones y esfuerzos en las macrofibras de la base
- Mecanismo de acople: descomposición del momento de volcamiento total M_OTM
"""
import sys
import os
import json
import numpy as np

sys.path.insert(0, '/Users/mac/Library/CloudStorage/OneDrive-Personal/3. Docencia/0. Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy')
from openseespy.opensees import *
import opseestools.analisis as an

wipe()
model('basic', '-ndm', 2, '-ndf', 3)

# Geometría
xloc = [0.0, 9.15]
yloc = [0.0, 2.6, 5.2, 7.8, 10.4, 13.0, 15.6, 18.2, 
        20.8, 23.4, 26.0, 28.6, 31.2, 33.8, 36.4, 39.0, 41.6]
ny = len(yloc) # 17 niveles
nx = len(xloc) # 2 muros
ht = yloc[-1]

# Nodos
for i in range(nx):
    for j in range(ny):
        nnode = 1000 * (i + 1) + j
        node(nnode, xloc[i], yloc[j])

fixY(0.0, 1, 1, 1)

# Diafragmas rígidos
for j in range(1, ny):
    for i in range(1, nx):
        masternode = 1000 + j
        slavenode  = 1000 * (i + 1) + j
        equalDOF(masternode, slavenode, 1)

# Materiales
fc = 35000.0 # kPa
E  = 1000.0 * 4300.0 * (fc / 1000.0)**0.5
ec = 2.0 * fc / E
fcu = 0.1 * fc
ecu = 0.006

k = 1.3
fcc = fc * k
ecc = 2.0 * fcc / E
fucc = 0.2 * fcc
eucc = 0.02

Fy = 420000.0
Es = 210000000.0
ey = Fy / Es
fu = 630000.0
eult = 0.10

uniaxialMaterial('Concrete02', 1, -fcc, -ecc, -fucc, -eucc)
uniaxialMaterial('Concrete02', 2, -fc,  -ec,  -fcu,  -ecu)
uniaxialMaterial('Hysteretic', 3, Fy, ey, fu, eult, 0.05*Fy, 0.11,
                                  -Fy, -ey, -fu, -eult, -0.05*Fy, -0.11,
                                  1.0, 1.0, 0.0, 0.0)

tagshear = 1000
G = E * 0.4
uniaxialMaterial('Elastic', tagshear, G)

# Elementos MVLEM
width = [0.30, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 0.30]
nfib  = len(width)
cMVLEM = 0.4
t1 = [7.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
t2 = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 7.5]

rhoborde = 0.012
rhoalma  = 0.012
rho = [rhoborde] + [rhoalma] * (nfib - 2) + [rhoborde]

concTags  = [1] + [2] * (nfib - 2) + [1]
steelTags = [3] * nfib
shearTags = [tagshear] * nfib

for i, thick in enumerate([t2, t1]):
    for j in range(ny - 1):
        nodeI = 1000 * (i + 1) + j
        nodeJ = 1000 * (i + 1) + (j + 1)
        eltag = 1000 * (i + 1) + j
        element('MVLEM', eltag, 0.0, nodeI, nodeJ, nfib, cMVLEM,
                '-thick', *thick, '-width', *width, '-rho', *rho,
                '-matConcrete', *concTags, '-matSteel', *steelTags, '-matShear', *shearTags)

# Vigas de enlace
bv = 0.30
hv = 0.50
Av = bv * hv
Iv = bv * hv**3 / 12.0
Ev = 24000000.0
geomTransf('Linear', 1)

tagvigas = []
for j in range(1, ny):
    nodeI = 1000 + j
    nodeJ = 2000 + j
    eltag = 100000 + j
    tagvigas.append(eltag)
    element('elasticBeamColumn', eltag, nodeI, nodeJ, Av, Ev, Iv, 1)

# Gravedad
P_gravity = -797.5 # kN
timeSeries('Linear', 1)
pattern('Plain', 1, 1)
for i in range(nx):
    for j in range(ny - 1):
        nodeJ = 1000 * (i + 1) + (j + 1)
        load(nodeJ, 0.0, P_gravity, 0.0)

W_total = nx * (ny - 1) * abs(P_gravity)

an.gravedad()
loadConst('-time', 0.0)

# Pushover
timeSeries('Linear', 2)
pattern('Plain', 2, 2)
q_lat = 1.0 / (ny - 1)
for j in range(ny - 1):
    load(1000 + j + 1, q_lat, 0.0, 0.0)

ctrl_node = 2016
Dmax = 0.015 * ht # 0.624 m
Dincr = 0.0005
Tol = 1e-6
maxNumIter = 10

wipeAnalysis()
constraints('Plain')
numberer('RCM')
system('BandGeneral')
test('EnergyIncr', Tol, maxNumIter)
algorithm('Newton')
integrator('DisplacementControl', ctrl_node, 1, Dincr)
analysis('Static')

algoritmo = {1:'KrylovNewton', 2: 'SecantNewton', 4: 'RaphsonNewton', 5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

Nsteps = int(Dmax / Dincr)
total_steps_to_sample = 50
sample_every = max(1, Nsteps // total_steps_to_sample)

# Coordenadas relativas de las 8 macrofibras (desde el centro del muro Lw = 7.65 m)
# Anchos: 0.30, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 0.30
Lw = sum(width)
fiber_x = []
current_edge = -Lw / 2.0
for w in width:
    fiber_x.append(current_edge + w / 2.0)
    current_edge += w

curve_u = []
curve_v = []
curve_drift = []
curve_vw = []

# Array para guardar estados completos muestreados
sampled_states = []

def record_current_state(step_num):
    u_roof = nodeDisp(ctrl_node, 1)
    v_base = getTime()
    drift_pct = (u_roof / ht) * 100.0
    vw = v_base / W_total
    
    # Perfil de desplazamientos en pisos (X de 0 a 16)
    floor_disps = [round(nodeDisp(1000 + j, 1), 5) for j in range(ny)]
    
    # Derivas de entrepiso (%)
    story_drifts = []
    for j in range(1, ny):
        dr = (floor_disps[j] - floor_disps[j-1]) / 2.6 * 100.0
        story_drifts.append(round(dr, 4))
        
    # Deformaciones y esfuerzos en la base del Muro 1 (nodo 1000 a 1001) y Muro 2 (nodo 2000 a 2001)
    # Altura del primer piso h = 2.6 m
    # En la base (nodo 1000 y 2000), los apoyos están fijos (v_i = 0, theta_i = 0)
    # Por tanto: eps_k = (v_j - x_k * theta_j) / h
    v1_j = nodeDisp(1001, 2)
    th1_j = nodeDisp(1001, 3)
    
    v2_j = nodeDisp(2001, 2)
    th2_j = nodeDisp(2001, 3)
    
    h_story = 2.6
    strains_w1 = [(v1_j - xk * th1_j) / h_story for xk in fiber_x]
    strains_w2 = [(v2_j - xk * th2_j) / h_story for xk in fiber_x]
    
    # Fuerzas globales en la base de Muro 1 y Muro 2
    f_w1 = eleResponse(1000, 'forces')
    f_w2 = eleResponse(2000, 'forces')
    
    # Fuerzas axiales en la base (reacciones)
    n_w1 = -f_w1[1] if len(f_w1) >= 2 else 0.0
    n_w2 = -f_w2[1] if len(f_w2) >= 2 else 0.0
    m_w1 = f_w1[2] if len(f_w1) >= 3 else 0.0
    m_w2 = f_w2[2] if len(f_w2) >= 3 else 0.0
    
    # Momento de volcamiento total en la base del edificio
    # M_OTM = M_w1 + M_w2 + T * L_arm  (L_arm = 9.15 m)
    # T = (N_w1 - N_w2) / 2  (fuerza axial neta inducida por el acople)
    t_axial = (n_w1 - n_w2) / 2.0
    m_couple = t_axial * 9.15
    m_walls = m_w1 + m_w2
    m_total = m_walls + m_couple
    
    couple_pct = (m_couple / m_total * 100.0) if m_total > 1e-3 else 0.0
    
    state = {
        "step": step_num,
        "roof_disp_m": round(u_roof, 5),
        "roof_drift_pct": round(drift_pct, 4),
        "base_shear_kN": round(v_base, 2),
        "coeff_vw": round(vw, 4),
        "floor_disps_m": floor_disps,
        "story_drifts_pct": story_drifts,
        "wall1_strains": [round(s, 6) for s in strains_w1],
        "wall2_strains": [round(s, 6) for s in strains_w2],
        "moments_kNm": {
            "m_wall1": round(m_w1, 1),
            "m_wall2": round(m_w2, 1),
            "m_couple": round(m_couple, 1),
            "m_total": round(m_total, 1),
            "couple_ratio_pct": round(couple_pct, 1)
        }
    }
    return state

# Guardar estado inicial (después de gravedad)
sampled_states.append(record_current_state(0))
curve_u.append(round(nodeDisp(ctrl_node, 1), 5))
curve_v.append(round(getTime(), 2))
curve_drift.append(round((nodeDisp(ctrl_node, 1) / ht) * 100.0, 4))
curve_vw.append(round(getTime() / W_total, 4))

print("Iniciando bucle de pushover paso a paso...")
for k in range(1, Nsteps + 1):
    ok = analyze(1)
    if ok != 0:
        for j in algoritmo:
            if j < 4:
                algorithm(algoritmo[j], '-initial')
            else:
                algorithm(algoritmo[j])
            test('EnergyIncr', Tol, maxNumIter * 50)
            ok = analyze(1)
            if ok == 0:
                test('EnergyIncr', Tol, maxNumIter)
                algorithm('Newton')
                break
    if ok != 0:
        print(f"Colapso numérico en paso {k} con u = {nodeDisp(ctrl_node, 1):.4f} m")
        break
        
    u_now = nodeDisp(ctrl_node, 1)
    v_now = getTime()
    curve_u.append(round(u_now, 5))
    curve_v.append(round(v_now, 2))
    curve_drift.append(round((u_now / ht) * 100.0, 4))
    curve_vw.append(round(v_now / W_total, 4))
    
    if k % sample_every == 0 or k == Nsteps:
        sampled_states.append(record_current_state(k))

print(f"Simulación finalizada exitosamente! {len(curve_u)} pasos calculados, {len(sampled_states)} estados completos guardados.")

full_dataset = {
    "metadata": {
        "title": "Simulación No Lineal de Edificio de Muros Acoplados con Macroelementos MVLEM",
        "author": "Prof. Orlando Arroyo - Universidad Industrial de Santander",
        "stories": 16,
        "story_height_m": 2.6,
        "total_height_m": ht,
        "wall_spacing_m": 9.15,
        "wall_length_m": Lw,
        "num_macrofibers": 8,
        "fiber_widths_m": width,
        "fiber_coords_x_m": [round(x, 3) for x in fiber_x],
        "thick_wall1_m": t2,
        "thick_wall2_m": t1,
        "rebar_ratio": rho,
        "fc_MPa": 35.0,
        "fy_MPa": 420.0,
        "seismic_weight_kN": W_total,
        "v_max_kN": max(curve_v),
        "vw_max": max(curve_vw),
        "d_max_m": max(curve_u),
        "drift_max_pct": max(curve_drift)
    },
    "story_elevations_m": yloc,
    "pushover_curve": {
        "disp_m": curve_u[::max(1, len(curve_u)//100)],
        "shear_kN": curve_v[::max(1, len(curve_v)//100)],
        "drift_pct": curve_drift[::max(1, len(curve_drift)//100)],
        "coeff_vw": curve_vw[::max(1, len(curve_vw)//100)]
    },
    "interactive_states": sampled_states
}

out_file = "/Users/mac/Library/CloudStorage/OneDrive-Personal/3. Docencia/0. Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/mvlem_detailed_simulation.json"
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(full_dataset, f, indent=2)

print(f"Dataset detallado guardado en: {out_file}")
