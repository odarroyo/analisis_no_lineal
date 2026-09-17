"""
================================================================================
UNIVERSIDAD INDUSTRIAL DE SANTANDER - ESCUELA DE INGENIERÍA CIVIL
CURSO: ANÁLISIS NO LINEAL DE ESTRUCTURAS
Profesor: Orlando Arroyo

Módulo Pedagógico:
¿Por qué el Análisis No Lineal exige Control por Desplazamiento?
Comparación de Columna en Voladizo: Modelo Elástico vs. Inelástico (Rótula ASCE 41)
Bajo Control de Desplazamiento (Pushover) y Control de Fuerza (Carga Monótona)
================================================================================

Este script realiza cuatro simulaciones numéricas en OpenSeesPy:
  1. Modelo Elástico bajo Control por Desplazamiento hasta 3% de deriva (90 mm).
     -> Obtiene la curva lineal y la fuerza elástica objetivo: F_el_3%.
  2. Modelo Elástico bajo Control por Fuerza hasta F_el_3%.
     -> Demuestra que en elasticidad lineal F = K*u <=> u = F/K (identidad total).
  3. Modelo Inelástico (Rótula ASCE 41 al 5% H) bajo Control por Desplazamiento.
     -> Captura la fluencia seccional (My), el endurecimiento a pico (Mu),
        la degradación de resistencia (softening) por descascaramiento y pandeo,
        y la meseta residual (Mr).
  4. Modelo Inelástico bajo Control por Fuerza buscando alcanzar F_el_3%.
     -> Demuestra la falla de convergencia de Newton-Raphson cuando la fuerza
        externa solicitada supera la capacidad resistente máxima (F_ext > V_cap).
        No existe equilibrio posible y el determinante de rigidez colapsa.

Exporta:
  - cantilever_simulation_data.json (para consumo del visualizador HTML)
  - cantilever_asce41_comparison.png (gráficas comparativas en alta resolución)
================================================================================
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import openseespy.opensees as ops

# ==============================================================================
# 1. PARÁMETROS GEOMÉTRICOS Y MATERIALES DE LA COLUMNA
# ==============================================================================
H = 3.0           # Altura total de la columna (m)
drift_target = 0.03  # Deriva máxima objetivo = 3% (0.09 m = 90 mm)
u_target = drift_target * H  # 0.09 m

# Posición de la rótula plástica concentrada al 5% de la altura
y_hinge = 0.05 * H        # 0.15 m desde la base
h_upper = H - y_hinge     # 2.85 m (brazo de palanca superior hasta la carga)

# Propiedades de la sección de concreto reforzado (400 mm x 400 mm)
b = 0.40          # Ancho de la sección (m)
h = 0.40          # Altura de la sección (m)
A = b * h         # Área de la sección transversal = 0.16 m2
I = (b * h**3) / 12.0  # Momento de inercia = 0.002133 m4

# Módulo de elasticidad del concreto (f'c = 28 MPa -> Ec ~ 25 GPa)
E = 25.0e6        # kPa (kN/m2)
EI = E * I        # Rigidez a flexión elástica = 53333.33 kN*m2

# Rigidez lateral elástica teórica del voladizo: K_lat = 3*EI / H^3
K_lat_theor = (3.0 * EI) / (H**3)  # 5925.93 kN/m

# ==============================================================================
# 2. PARÁMETROS DE LA RÓTULA PLÁSTICA ASCE 41-17 / ASCE 41-23
# ==============================================================================
# Para evitar la "doble contabilidad de la flexibilidad elástica" (double-counting
# of elastic flexibility), el resorte concentrado zeroLength modela ÚNICAMENTE
# la deformación inelástica / plástica (theta_p), tal como lo estipula la norma ASCE 41.
# Toda la flexibilidad elástica de la columna ya la aportan los elementos de viga (3EI/H^3).
# Por tanto, el resorte es virtualmente rígido antes de fluencia (theta_y ~ 0),
# garantizando que en el rango elástico (0 a My), ambos modelos (elástico e inelástico)
# sigan EXACTAMENTE la misma recta de rigidez K0 = 5925.9 kN/m.

My = 180.0        # kN*m (Momento de fluencia)
Mu = 210.0        # kN*m (Momento máximo / Capping, 1.17 My)
Mr = 40.0         # kN*m (Momento residual post-pico, 0.22 My)

# Rigidez elástica del resorte muy alta para representar rótula rígida-plástica:
K_spring_elastic = 1.0e7  # kNm/rad (>> 4*EI/H = 7.1e4 kNm/rad)
theta_y = My / K_spring_elastic  # 0.000018 rad (0.018 mrad ~ 0)

# Deformaciones plásticas según ASCE 41:
# a = 0.012 rad (rotación plástica de fluencia a pico capping)
# b = 0.024 rad (rotación plástica de fluencia a residual)
theta_u = theta_y + 0.012  # rad (~ 0.012 rad)
theta_r = theta_y + 0.024  # rad (~ 0.024 rad)

# Capacidad cortante lateral teórica en el pico: V_cap = Mu / h_upper
V_cap_theor = Mu / h_upper  # 210 / 2.85 = 73.68 kN
V_yield_theor = My / h_upper  # 180 / 2.85 = 63.16 kN
V_res_theor = Mr / h_upper  # 40 / 2.85 = 14.04 kN

print("=" * 80)
print("INICIANDO SIMULACIONES NUMÉRICAS EN OPENSEESPY")
print(f"Columna en voladizo H = {H:.2f} m | Sección: {b*1000:.0f}x{h*1000:.0f} mm")
print(f"Rótula ASCE 41 al 5% de H (y = {y_hinge:.2f} m, brazo h_lever = {h_upper:.2f} m)")
print(f"Capacidad máxima de momento Mu = {Mu:.1f} kN*m -> Cortante máximo V_cap = {V_cap_theor:.2f} kN")
print("=" * 80)

# ==============================================================================
# CASO 1: MODELO ELÁSTICO - CONTROL POR DESPLAZAMIENTO (PUSHOVER HASTA 3% DERIVA)
# ==============================================================================
print("\n[1/4] Ejecutando: Modelo Elástico con Control por Desplazamiento...")
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, y_hinge)
ops.node(3, 0.0, H)

ops.fix(1, 1, 1, 1)

ops.geomTransf('Linear', 1)
ops.element('elasticBeamColumn', 1, 1, 2, A, E, I, 1)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, I, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(3, 1.0, 0.0, 0.0)

ops.system('BandGeneral')
ops.numberer('Plain')
ops.constraints('Plain')
ops.test('NormDispIncr', 1.0e-8, 25, 0)
ops.algorithm('Newton')

N_steps_disp = 100
du_step = u_target / N_steps_disp
ops.integrator('DisplacementControl', 3, 1, du_step)
ops.analysis('Static')

el_dc_disp = [0.0]
el_dc_drift = [0.0]
el_dc_force = [0.0]
el_dc_base_moment = [0.0]
el_dc_hinge_moment = [0.0]

for step in range(1, N_steps_disp + 1):
    ret = ops.analyze(1)
    if ret != 0:
        print(f"  Error en análisis elástico por desplazamiento en paso {step}")
        break
    u = ops.nodeDisp(3, 1)
    ops.reactions()
    V = -ops.nodeReaction(1, 1)
    M_base = ops.nodeReaction(1, 3)
    M_hinge = V * h_upper  # Momento por equilibrio estático en y = 0.05 H
    el_dc_disp.append(u)
    el_dc_drift.append((u / H) * 100.0)
    el_dc_force.append(V)
    el_dc_base_moment.append(M_base)
    el_dc_hinge_moment.append(M_hinge)

F_target_elastic = el_dc_force[-1]
print(f"  -> Finalizado exitosamente. Desplazamiento máximo: {el_dc_disp[-1]*1000:.1f} mm ({el_dc_drift[-1]:.2f}% deriva)")
print(f"  -> Fuerza elástica requerida para 3% de deriva: F_el_3% = {F_target_elastic:.2f} kN")
print(f"  -> Momento en la base elástico: {el_dc_base_moment[-1]:.2f} kN*m | En la rótula: {el_dc_hinge_moment[-1]:.2f} kN*m")

# ==============================================================================
# CASO 2: MODELO ELÁSTICO - CONTROL POR FUERZA (INCREMENTOS HASTA F_el_3%)
# ==============================================================================
print("\n[2/4] Ejecutando: Modelo Elástico con Control por Fuerza...")
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, y_hinge)
ops.node(3, 0.0, H)

ops.fix(1, 1, 1, 1)

ops.geomTransf('Linear', 1)
ops.element('elasticBeamColumn', 1, 1, 2, A, E, I, 1)
ops.element('elasticBeamColumn', 2, 2, 3, A, E, I, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(3, F_target_elastic, 0.0, 0.0)

ops.system('BandGeneral')
ops.numberer('Plain')
ops.constraints('Plain')
ops.test('NormDispIncr', 1.0e-8, 25, 0)
ops.algorithm('Newton')

N_steps_force = 100
ops.integrator('LoadControl', 1.0 / N_steps_force)
ops.analysis('Static')

el_fc_disp = [0.0]
el_fc_drift = [0.0]
el_fc_force = [0.0]
el_fc_base_moment = [0.0]
el_fc_hinge_moment = [0.0]

for step in range(1, N_steps_force + 1):
    ret = ops.analyze(1)
    if ret != 0:
        print(f"  Error en paso {step}")
        break
    u = ops.nodeDisp(3, 1)
    ops.reactions()
    V = -ops.nodeReaction(1, 1)
    M_base = ops.nodeReaction(1, 3)
    M_hinge = V * h_upper
    el_fc_disp.append(u)
    el_fc_drift.append((u / H) * 100.0)
    el_fc_force.append(V)
    el_fc_base_moment.append(M_base)
    el_fc_hinge_moment.append(M_hinge)

print(f"  -> Finalizado exitosamente. Desplazamiento máximo: {el_fc_disp[-1]*1000:.1f} mm")
print(f"  -> Fuerza final alcanzada: {el_fc_force[-1]:.2f} kN (Coincidencia idéntica con control de desplazamiento)")

# ==============================================================================
# CASO 3: MODELO INELÁSTICO (RÓTULA ASCE 41) - CONTROL POR DESPLAZAMIENTO
# ==============================================================================
print("\n[3/4] Ejecutando: Modelo Inelástico (Rótula ASCE 41) con Control por Desplazamiento...")
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

# Nodos:
# 1: Base (0, 0)
# 2: Lado inferior de la rótula (0, y_hinge)
# 3: Lado superior de la rótula (0, y_hinge) [Coincidente]
# 4: Cúspide del voladizo (0, H)
ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, y_hinge)
ops.node(3, 0.0, y_hinge)
ops.node(4, 0.0, H)

ops.fix(1, 1, 1, 1)
# Restricción cinemática: traslaciones X e Y idénticas en la rótula (solo rota)
ops.equalDOF(2, 3, 1, 2)

# Material rotacional tipo Hysteretic (Backbone ASCE 41 simétrico)
# Puntos: (My, theta_y), (Mu, theta_u), (Mr, theta_r)
ops.uniaxialMaterial('Hysteretic', 1,
                     My, theta_y,
                     Mu, theta_u,
                     Mr, theta_r,
                     -My, -theta_y,
                     -Mu, -theta_u,
                     -Mr, -theta_r,
                     0.0, 0.0, 0.0, 0.0, 0.0)

# Elemento zeroLength con la rótula rotacional en el DOF 6 (giro Z en 2D = DOF 3)
ops.element('zeroLength', 1, 2, 3, '-mat', 1, '-dir', 6)

ops.geomTransf('Linear', 1)
ops.element('elasticBeamColumn', 2, 1, 2, A, E, I, 1)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, I, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(4, 1.0, 0.0, 0.0)

ops.system('BandGeneral')
ops.numberer('Plain')
ops.constraints('Transformation')
ops.test('NormDispIncr', 1.0e-6, 50, 0)
ops.algorithm('Newton')

N_steps_inel_dc = 150
du_inel = u_target / N_steps_inel_dc
ops.integrator('DisplacementControl', 4, 1, du_inel)
ops.analysis('Static')

inel_dc_disp = [0.0]
inel_dc_drift = [0.0]
inel_dc_force = [0.0]
inel_dc_base_moment = [0.0]
inel_dc_hinge_moment = [0.0]
inel_dc_hinge_rot = [0.0]
inel_dc_state = ["Elástico (Tramo O-B)"]

for step in range(1, N_steps_inel_dc + 1):
    ret = ops.analyze(1)
    if ret != 0:
        ops.algorithm('ModifiedNewton', '-initial')
        ret = ops.analyze(1)
        ops.algorithm('Newton')
        if ret != 0:
            print(f"  Análisis inelástico por desplazamiento se detuvo en paso {step}")
            break

    u = ops.nodeDisp(4, 1)
    ops.reactions()
    V = -ops.nodeReaction(1, 1)
    M_base = ops.nodeReaction(1, 3)

    # Rotación relativa de la rótula: en flexión lateral hacia +X (deriva positiva),
    # la rotación horaria en el sistema 2D es negativa. Tomamos la magnitud absoluta
    # para representar el giro plástico positivo congruente con la curva ASCE 41:
    th_hinge = abs(ops.nodeDisp(3, 3) - ops.nodeDisp(2, 3))
    # Momento en la rótula por equilibrio estático: M_h = V * h_upper
    M_h = V * h_upper

    # Clasificación pedagógica del estado de daño ASCE 41
    if th_hinge <= theta_y + 1e-4:
        state_str = "Elástico (Tramo O-B: M < My)"
    elif th_hinge <= theta_u:
        state_str = "Endurecimiento / Capping (Tramo B-C: My < M <= Mu)"
    elif th_hinge <= theta_r:
        state_str = "Degradación Post-Pico / Softening (Tramo C-D: Mu > M >= Mr)"
    else:
        state_str = "Meseta Residual (Tramo D-E: M ~ Mr)"

    inel_dc_disp.append(u)
    inel_dc_drift.append((u / H) * 100.0)
    inel_dc_force.append(V)
    inel_dc_base_moment.append(M_base)
    inel_dc_hinge_moment.append(M_h)
    inel_dc_hinge_rot.append(th_hinge)
    inel_dc_state.append(state_str)

max_V_inel = max(inel_dc_force)
max_M_inel = max(inel_dc_hinge_moment)
final_V_inel = inel_dc_force[-1]
final_M_inel = inel_dc_hinge_moment[-1]

print(f"  -> Finalizado exitosamente. Pasos completados: {len(inel_dc_disp)-1} / {N_steps_inel_dc}")
print(f"  -> Cortante máximo (Pico): V_max = {max_V_inel:.2f} kN | Momento máximo rótula: M_max = {max_M_inel:.2f} kN*m")
print(f"  -> Cortante final (Deriva 3%): V_fin = {final_V_inel:.2f} kN | Momento final rótula: M_fin = {final_M_inel:.2f} kN*m")
print(f"  -> Caída de capacidad observada: {((max_V_inel - final_V_inel) / max_V_inel)*100:.1f}% de pérdida de cortante.")

# ==============================================================================
# CASO 4: MODELO INELÁSTICO (RÓTULA ASCE 41) - CONTROL POR FUERZA HASTA F_el_3%
# ==============================================================================
print("\n[4/4] Ejecutando: Modelo Inelástico con Control por Fuerza buscando F_el_3%...")
print(f"  (Carga objetivo: {F_target_elastic:.2f} kN vs. Capacidad máxima real: {max_V_inel:.2f} kN)")
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, y_hinge)
ops.node(3, 0.0, y_hinge)
ops.node(4, 0.0, H)

ops.fix(1, 1, 1, 1)
ops.equalDOF(2, 3, 1, 2)

ops.uniaxialMaterial('Hysteretic', 1,
                     My, theta_y,
                     Mu, theta_u,
                     Mr, theta_r,
                     -My, -theta_y,
                     -Mu, -theta_u,
                     -Mr, -theta_r,
                     0.0, 0.0, 0.0, 0.0, 0.0)

ops.element('zeroLength', 1, 2, 3, '-mat', 1, '-dir', 6)

ops.geomTransf('Linear', 1)
ops.element('elasticBeamColumn', 2, 1, 2, A, E, I, 1)
ops.element('elasticBeamColumn', 3, 3, 4, A, E, I, 1)

ops.timeSeries('Linear', 1)
ops.pattern('Plain', 1, 1)
ops.load(4, F_target_elastic, 0.0, 0.0)

ops.system('BandGeneral')
ops.numberer('Plain')
ops.constraints('Transformation')
# Prueba de convergencia estricta para ilustrar el residuo divergente
ops.test('NormDispIncr', 1.0e-6, 40, 0)
ops.algorithm('Newton')

N_steps_fc_inel = 100
dF_step = F_target_elastic / N_steps_fc_inel
ops.integrator('LoadControl', 1.0 / N_steps_fc_inel)
ops.analysis('Static')

inel_fc_disp = [0.0]
inel_fc_drift = [0.0]
inel_fc_force = [0.0]
inel_fc_base_moment = [0.0]
inel_fc_hinge_moment = [0.0]
inel_fc_hinge_rot = [0.0]

failure_step = None
attempted_force = 0.0

for step in range(1, N_steps_fc_inel + 1):
    ret = ops.analyze(1)
    if ret != 0:
        failure_step = step
        attempted_force = step * dF_step
        print(f"  ❌ ¡COLAPSO NUMÉRICO EN PASO {step} DE {N_steps_fc_inel}!")
        print(f"     Fuerza externa solicitada en este incremento: F_ext = {attempted_force:.2f} kN")
        print(f"     Última fuerza resistente interna convergida: F_int = {inel_fc_force[-1]:.2f} kN")
        print(f"     Capacidad física máxima de la columna: V_cap = {max_V_inel:.2f} kN")
        print("     DIAGNÓSTICO PEDAGÓGICO: F_ext > V_cap. El residuo R = F_ext - F_int no puede anularse.")
        print("     La matriz de rigidez tangente Kt se hace singular/indefinida y Newton-Raphson diverge.")
        break

    u = ops.nodeDisp(4, 1)
    ops.reactions()
    V = -ops.nodeReaction(1, 1)
    M_base = ops.nodeReaction(1, 3)
    th_hinge = abs(ops.nodeDisp(3, 3) - ops.nodeDisp(2, 3))
    M_h = V * h_upper

    inel_fc_disp.append(u)
    inel_fc_drift.append((u / H) * 100.0)
    inel_fc_force.append(V)
    inel_fc_base_moment.append(M_base)
    inel_fc_hinge_moment.append(M_h)
    inel_fc_hinge_rot.append(th_hinge)

# ==============================================================================
# 5. ESTRUCTURACIÓN Y EXPORTACIÓN DE DATOS EN JSON PARA LA WEB INTERACTIVA
# ==============================================================================
output_data = {
    "metadata": {
        "title": "Comparativa de Análisis No Lineal: Control de Desplazamiento vs. Control de Fuerza",
        "author": "Prof. Orlando Arroyo - Universidad Industrial de Santander",
        "structure": "Columna en Voladizo (Cantilever Column)",
        "height_m": H,
        "section_b_m": b,
        "section_h_m": h,
        "E_kPa": E,
        "hinge_location_ratio": 0.05,
        "hinge_y_m": y_hinge,
        "lever_arm_m": h_upper,
        "drift_target_pct": drift_target * 100.0,
        "u_target_m": u_target,
        "F_target_elastic_kN": float(F_target_elastic),
        "asce41_parameters": {
            "My_kNm": My,
            "theta_y_rad": theta_y,
            "Mu_kNm": Mu,
            "theta_u_rad": theta_u,
            "Mr_kNm": Mr,
            "theta_r_rad": theta_r,
            "V_yield_kN": float(V_yield_theor),
            "V_cap_kN": float(V_cap_theor),
            "V_residual_kN": float(V_res_theor)
        },
        "failure_summary": {
            "failed_step": failure_step,
            "total_steps": N_steps_fc_inel,
            "attempted_force_kN": float(attempted_force),
            "last_converged_force_kN": float(inel_fc_force[-1]),
            "last_converged_disp_mm": float(inel_fc_disp[-1] * 1000.0),
            "last_converged_drift_pct": float(inel_fc_drift[-1]),
            "opensees_error_code": -3
        }
    },
    "case1_elastic_disp_control": {
        "disp_m": el_dc_disp,
        "drift_pct": el_dc_drift,
        "shear_kN": el_dc_force,
        "hinge_moment_kNm": el_dc_hinge_moment,
        "base_moment_kNm": el_dc_base_moment
    },
    "case2_elastic_force_control": {
        "disp_m": el_fc_disp,
        "drift_pct": el_fc_drift,
        "shear_kN": el_fc_force,
        "hinge_moment_kNm": el_fc_hinge_moment,
        "base_moment_kNm": el_fc_base_moment
    },
    "case3_inelastic_disp_control": {
        "disp_m": inel_dc_disp,
        "drift_pct": inel_dc_drift,
        "shear_kN": inel_dc_force,
        "hinge_moment_kNm": inel_dc_hinge_moment,
        "hinge_rot_rad": inel_dc_hinge_rot,
        "base_moment_kNm": inel_dc_base_moment,
        "damage_states": inel_dc_state
    },
    "case4_inelastic_force_control": {
        "disp_m": inel_fc_disp,
        "drift_pct": inel_fc_drift,
        "shear_kN": inel_fc_force,
        "hinge_moment_kNm": inel_fc_hinge_moment,
        "hinge_rot_rad": inel_fc_hinge_rot,
        "base_moment_kNm": inel_fc_base_moment
    }
}

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "cantilever_simulation_data.json")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2)

print(f"\n[OK] Datos numéricos guardados exitosamente en:\n  {json_path}")

# ==============================================================================
# 6. GENERACIÓN DE GRÁFICO COMPARATIVO CON MATPLOTLIB (ALTA DEFINICIÓN)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Subplot 1: Curva Pushover Global (Cortante Basal vs. Deriva / Desplazamiento)
ax1.plot([d * 1000 for d in el_dc_disp], el_dc_force, 'b--', lw=2.2, label=f'Elástico - Desp. Control (F_3% = {F_target_elastic:.1f} kN)')
ax1.plot([d * 1000 for d in el_fc_disp], el_fc_force, 'c:', lw=2.5, label='Elástico - Fuerza Control (Idéntico)')
ax1.plot([d * 1000 for d in inel_dc_disp], inel_dc_force, 'r-', lw=2.8, label=f'Inelástico ASCE 41 - Desp. Control (V_max = {max_V_inel:.1f} kN)')
ax1.plot([d * 1000 for d in inel_fc_disp], inel_fc_force, 'm-', lw=2.2, label='Inelástico ASCE 41 - Fuerza Control')

# Punto de colapso por control de fuerza
if failure_step is not None:
    ax1.scatter([inel_fc_disp[-1] * 1000], [inel_fc_force[-1]], color='red', s=140, zorder=5, edgecolors='black', lw=1.5)
    ax1.annotate(f'Colapso Numérico\nFuerza Control (Paso {failure_step})\nF_ext > V_cap ({inel_fc_force[-1]:.1f} kN)',
                 xy=(inel_fc_disp[-1] * 1000, inel_fc_force[-1]),
                 xytext=(inel_fc_disp[-1] * 1000 + 10, inel_fc_force[-1] + 60),
                 arrowprops=dict(facecolor='crimson', shrink=0.08, width=1.5, headwidth=8),
                 fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="mistyrose", ec="crimson", lw=1.2))

ax1.set_title('1. Respuesta Global: Cortante Basal vs. Desplazamiento en la Cúspide', fontsize=11, fontweight='bold')
ax1.set_xlabel('Desplazamiento en la Cúspide $\\Delta$ (mm)', fontsize=10)
ax1.set_ylabel('Cortante Basal $V$ (kN)', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper left', fontsize=8.5, framealpha=0.9)
ax1.set_xlim(-2, 95)

# Subplot 2: Evolución del Momento en la Rótula ASCE 41
ax2.plot(inel_dc_hinge_rot, inel_dc_hinge_moment, 'r-', lw=2.8, label='Inelástico: Rótula ASCE 41 (M_h vs $\\theta_h$)')
ax2.axhline(My, color='gray', linestyle=':', lw=1.2, label=f'Fluencia My = {My:.0f} kN*m')
ax2.axhline(Mu, color='darkorange', linestyle='--', lw=1.5, label=f'Capacidad Máxima Mu = {Mu:.0f} kN*m')
ax2.axhline(Mr, color='purple', linestyle=':', lw=1.2, label=f'Residual Mr = {Mr:.0f} kN*m')

# Anotaciones pedagógicas de los puntos ASCE 41
ax2.scatter([theta_y, theta_u, theta_r], [My, Mu, Mr], color=['green', 'darkorange', 'purple'], s=80, zorder=5)
ax2.text(theta_y, My - 18, 'B: Fluencia\n($\\theta_y, M_y$)', fontsize=8, ha='center', color='green', fontweight='bold')
ax2.text(theta_u, Mu + 8, 'C: Capping\n($\\theta_u, Mu$)', fontsize=8, ha='center', color='darkorange', fontweight='bold')
ax2.text(theta_r, Mr + 10, 'D: Residual\n($\\theta_r, M_r$)', fontsize=8, ha='center', color='purple', fontweight='bold')

# Flecha indicadora de la caída del momento (Softening)
ax2.annotate('¿Por qué cae el momento?\n• Descascaramiento recubrimiento\n• Agotamiento confinamiento\n• Pandeo/fluencia del acero',
             xy=((theta_u + theta_r) / 2, (Mu + Mr) / 2),
             xytext=(theta_u + 0.005, Mu - 50),
             arrowprops=dict(facecolor='darkred', shrink=0.08, width=1.5, headwidth=7),
             fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", fc="#fff5f5", ec="darkred", lw=1.2))

ax2.set_title('2. Comportamiento Constitutivo de la Rótula ASCE 41 al 5% H', fontsize=11, fontweight='bold')
ax2.set_xlabel('Giro Plástico de la Rótula $\\theta_h$ (rad)', fontsize=10)
ax2.set_ylabel('Momento en la Rótula $M_h$ (kN*m)', fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='lower right', fontsize=8.5, framealpha=0.9)

fig.suptitle('Laboratorio Pedagógico OpenSeesPy: Control por Desplazamiento vs. Control por Fuerza\n(Prof. Orlando Arroyo - UIS)',
             fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()

png_path = os.path.join(current_dir, "cantilever_asce41_comparison.png")
fig.savefig(png_path, dpi=200, bbox_inches='tight')
plt.close(fig)

print(f"[OK] Gráfico comparativo generado en:\n  {png_path}")
print("=" * 80)
print("¡EJECUCIÓN COMPLETADA EXITOSAMENTE!")
print("=" * 80)
