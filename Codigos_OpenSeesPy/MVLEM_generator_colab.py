#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CURSO DE ANÁLISIS NO LINEAL DE ESTRUCTURAS
Script: Análisis Pushover de Muros de Concreto Reforzado con Elementos MVLEM
Modelo: Edificio de 16 Pisos con Muros Acoplados (Versión Colab & Local)
Profesor: Orlando Arroyo
================================================================================

Este script implementa el modelado macroscópico de muros estructurales mediante el
elemento MVLEM (Multiple-Vertical-Line-Element-Model, Vulcano et al., 1988):
- Discretización del muro en 8 macrofibras verticales (flexo-compresión) y un resorte
  horizontal central para respuesta a cortante.
- Materiales no lineales: Concrete02 (confinado en bordes, no confinado en alma) y
  acero Hysteretic con endurecimiento y degradación cíclica.
- Edificio de 16 pisos (H = 41.6 m, entrepisos de 2.6 m) con 2 muros acoplados mediante
  vigas de enlace y diafragmas rígidos en cada nivel.
- Análisis estático no lineal (Pushover) bajo diferentes patrones de carga lateral.
- Gráficas didácticas: Curva de Capacidad (V/W vs Roof Drift %) y Cortante Basal vs Desplazamiento.
- Compatible con Google Colab y protegido para ejecución local en Mac ARM.
================================================================================
"""

# ==============================================================================
# 0. VERIFICACIÓN DE DEPENDENCIAS (PROTECCIÓN PARA ENTORNO LOCAL Y GOOGLE COLAB)
# ==============================================================================
import sys
import os
import platform
import subprocess
import importlib
import time

IN_COLAB = 'google.colab' in sys.modules
if not IN_COLAB:
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False

def check_and_install_dependencies():
    if IN_COLAB:
        colab_packages = ["openseespy", "opseestools", "opsvis", "matplotlib", "numpy", "scipy", "pandas"]
        missing = []
        for pkg in colab_packages:
            try:
                importlib.import_module(pkg)
            except ImportError:
                missing.append(pkg)
        
        if missing:
            print(f"🔧 [Google Colab] Instalando dependencias necesarias: {missing}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", *missing])
            print("✅ Dependencias de Google Colab instaladas con éxito.\n")
    else:
        required_modules = ["openseespy.opensees", "opseestools", "opsvis", "matplotlib", "numpy", "pandas"]
        missing = []
        for mod in required_modules:
            try:
                importlib.import_module(mod)
            except ImportError:
                missing.append(mod)
        
        if missing:
            print(f"⚠️ [Entorno Local] Faltan los siguientes módulos: {missing}")
            if sys.platform == "darwin" and platform.machine() == "arm64":
                print("💡 En macOS Apple Silicon (M1/M2/M3/M4), instala con:")
                print("   pip install openseespy-mac-arm opseestools opsvis matplotlib numpy pandas scipy")
            else:
                print(f"💡 Instala con: pip install {' '.join(missing)}")
            sys.exit(1)
        else:
            print("✅ Entorno local verificado: OpenSeesPy y librerías complementarias listas.")

check_and_install_dependencies()

# %% [1] Importación de Librerías y Configuración Gráfica
from openseespy.opensees import *
import matplotlib.pyplot as plt
import opseestools.analisis as an
import opsvis as opsv
import numpy as np

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('default')

# %% [2] Inicialización del Modelo
# Unidades de trabajo coherentes:
# - Longitud: metros [m]
# - Fuerza: kilonewtons [kN]
# - Esfuerzo / Presión: kilopascales [kPa] = kN/m^2 (ej. fc = 35 MPa = 35000 kPa)
# - Masa: toneladas métricas [ton] = [kN * s^2 / m]

wipe()
model('basic', '-ndm', 2, '-ndf', 3)
print("🏗️ Modelo 2D inicializado para elementos MVLEM (3 GDL/nodo: Ux, Uy, Rz).")

# %% [3] Parámetros Geométricos y Configuración del Edificio
# Coordenadas de los muros y niveles de entrepiso
xloc = [0.0, 9.15] # Ubicación en X de los 2 muros acoplados [m]
yloc = [0.0, 2.6, 5.2, 7.8, 10.4, 13.0, 15.6, 18.2, 
        20.8, 23.4, 26.0, 28.6, 31.2, 33.8, 36.4, 39.0, 41.6] # 16 pisos de 2.6 m

ny = len(yloc) # 17 niveles nodales (base + 16 pisos)
nx = len(xloc) # 2 ejes de muros

diafragma = 1 # 1 = Diafragma rígido activo en cada nivel
pushtype  = 2 # 1 = Triangular proporcional a altura, 2 = Uniforme, 3 = Modal

ht = yloc[-1] # Altura total del edificio (41.6 m)
print(f"📐 Geometría: {nx} muros acoplados, {ny-1} pisos de 2.6 m (Altura total H = {ht} m).")

# %% [4] Definición de Nodos y Restricciones de Base
for i in range(nx):
    for j in range(ny):
        nnode = 1000 * (i + 1) + j
        node(nnode, xloc[i], yloc[j])

# Empotramiento perfecto en la base (Y = 0)
fixY(0.0, 1, 1, 1)
print("📍 Nodos y apoyos empotrados en la base generados exitosamente.")

# %% [5] Asignación de Diafragmas Rígidos de Piso
if diafragma == 1:
    for j in range(1, ny):
        for i in range(1, nx):
            masternode = 1000 + j
            slavenode  = 1000 * (i + 1) + j
            equalDOF(masternode, slavenode, 1) # Restricción horizontal Ux
    print(f"🔗 Diafragmas rígidos asignados en los {ny-1} pisos.")

# %% [6] Materiales Constitutivos No Lineales
# Transformaciones geométricas
geomTransf('Linear', 1)
geomTransf('PDelta', 2)

# Parámetros del concreto [kPa] (fc = 35 MPa)
fc = 35000.0
E  = 1000.0 * 4300.0 * (fc / 1000.0)**0.5
ec = 2.0 * fc / E
fcu = 0.1 * fc
ecu = 0.006

# Concreto confinado (Mander k = 1.3)
k = 1.3
fcc = fc * k
ecc = 2.0 * fcc / E
fucc = 0.2 * fcc
eucc = 0.02

# Acero de refuerzo longitudinal [kPa] (Fy = 420 MPa)
Fy = 420000.0
Es = 210000000.0
ey = Fy / Es
fu = 630000.0 # Fu = 630 MPa
eult = 0.10

# UniaxialMaterial para MVLEM
# Tag 1: Concreto confinado (bordes)
# Tag 2: Concreto no confinado (alma)
# Tag 3: Acero Hysteretic con endurecimiento y degradación
# Tag 1000: Resorte elástico a cortante (G = 0.4 * E)
uniaxialMaterial('Concrete02', 1, -fcc, -ecc, -fucc, -eucc)
uniaxialMaterial('Concrete02', 2, -fc,  -ec,  -fcu,  -ecu)
uniaxialMaterial('Hysteretic', 3, Fy, ey, fu, eult, 0.05*Fy, 0.11,
                                  -Fy, -ey, -fu, -eult, -0.05*Fy, -0.11,
                                  1.0, 1.0, 0.0, 0.0)

tagshear = 1000
G = E * 0.4
uniaxialMaterial('Elastic', tagshear, G)
print("🧱 Materiales definidos: Concrete02 (confinado/no confinado), Hysteretic (acero) y resorte a cortante.")

# %% [7] Definición de Elementos MVLEM (Muros Estructurales)
# Ancho de las 8 macrofibras a lo largo de la longitud del muro [m]
width = [0.30, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 0.30]
nfib  = len(width) # 8 fibras
cMVLEM = 0.4 # Ubicación del centro de rotación respecto a la base del elemento

# Espesores por fibra [m] (Aletas/elementos de borde en los extremos)
t1 = [7.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3] # Muro 1 (borde izquierdo engrosado)
t2 = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 7.5] # Muro 2 (borde derecho engrosado)

# Cuantías de acero (1.2% en bordes y alma)
rhoborde = 0.012
rhoalma  = 0.012
rho = [rhoborde] + [rhoalma] * (nfib - 2) + [rhoborde]

# Tags de materiales para las fibras
concTags  = [1] + [2] * (nfib - 2) + [1] # Confinado en bordes, no confinado en alma
steelTags = [3] * nfib
shearTags = [tagshear] * nfib

# Creación de los elementos MVLEM piso a piso
for i, thick in enumerate([t2, t1]):
    for j in range(ny - 1):
        nodeI = 1000 * (i + 1) + j
        nodeJ = 1000 * (i + 1) + (j + 1)
        eltag = 1000 * (i + 1) + j
        element('MVLEM', eltag, 0.0, nodeI, nodeJ, nfib, cMVLEM,
                '-thick', *thick, '-width', *width, '-rho', *rho,
                '-matConcrete', *concTags, '-matSteel', *steelTags, '-matShear', *shearTags)

print(f"🏢 Muros generados: {nx * (ny - 1)} elementos MVLEM discretizados con {nfib} macrofibras.")

# %% [8] Vigas de Enlace / Acople entre Muros
bv = 0.30 # Base [m]
hv = 0.50 # Altura [m]
Av = bv * hv
Iv = bv * hv**3 / 12.0
Ev = 24000000.0 # Módulo elástico de las vigas [kPa] (24 GPa)

tagvigas = []
for j in range(1, ny):
    nodeI = 1000 + j
    nodeJ = 2000 + j
    eltag = 100000 + j
    tagvigas.append(eltag)
    element('elasticBeamColumn', eltag, nodeI, nodeJ, Av, Ev, Iv, 1)

print(f"🌉 Vigas de acople generadas: {len(tagvigas)} vigas conectando ambos muros.")

# %% [9] Cargas Gravitacionales
# Carga vertical puntual por muro por nivel [kN]
P_gravity = -797.5 # kN

timeSeries('Linear', 1)
pattern('Plain', 1, 1)
for i in range(nx):
    for j in range(ny - 1):
        nodeJ = 1000 * (i + 1) + (j + 1)
        load(nodeJ, 0.0, P_gravity, 0.0)

# Peso sísmico total estimado del edificio [kN]
W_total = nx * (ny - 1) * abs(P_gravity)
print(f"⚖️ Cargas gravitacionales aplicadas: {P_gravity} kN/nodo. Peso total W = {W_total:.1f} kN.")

# Análisis de gravedad
an.gravedad()
loadConst('-time', 0.0)
print("✅ Cargas de gravedad convergidas.")

# %% [10] Configuración del Patrón de Carga Lateral (Pushover)
timeSeries('Linear', 2)
pattern('Plain', 2, 2)

if pushtype == 1:
    # Patrón triangular proporcional a la altura
    ylocation = np.array(yloc)
    norm = np.sum(ylocation)
    forces = ylocation / norm
    for j in range(ny - 1):
        load(1000 + j + 1, forces[j + 1], 0.0, 0.0)
    print("🎯 Patrón de empuje lateral: Triangular proporcional a la altura.")
elif pushtype == 2:
    # Patrón uniforme
    q_lat = 1.0 / (ny - 1)
    for j in range(ny - 1):
        load(1000 + j + 1, q_lat, 0.0, 0.0)
    print("🎯 Patrón de empuje lateral: Uniforme en la altura.")

# %% [11] Ejecución del Análisis Pushover No Lineal
ctrl_node = max(getNodeTags())
Dmax = 0.015 * ht # Desplazamiento máximo: 1.5% de deriva global = 0.624 m
Dincr = 0.0001    # Paso fino de desplazamiento [m]

print(f"🚀 Iniciando Pushover MVLEM (Control nodo {ctrl_node} en H = {ht} m, Dmax = {Dmax:.3f} m)...")
stime = time.time()
dtecho, Vbasal = an.pushover2(Dmax, Dincr, ctrl_node, 1, [ht, W_total], Tol=1e-6)
etime = time.time()

dtecho = np.array(dtecho)
Vbasal = np.array(Vbasal)
roof_drift_pct = (dtecho / ht) * 100.0
coeff_V_W = Vbasal / W_total

d_ult = dtecho[-1] if len(dtecho) > 0 else 0.0
v_max = max(Vbasal) if len(Vbasal) > 0 else 0.0
cw_max = max(coeff_V_W) if len(coeff_V_W) > 0 else 0.0
print(f"🏁 Pushover completado en {etime - stime:.2f} s.")
print(f"   Desplazamiento máximo: {d_ult:.4f} m (Deriva techo: {roof_drift_pct[-1]:.2f}%)")
print(f"   Cortante basal máximo: {v_max:.2f} kN (V/W máximo: {cw_max:.3f})")

# %% [12] Gráficas Didácticas de Capacidad para Muros MVLEM
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Subplot 1: Deriva de Techo vs Coeficiente de Cortante Basal (V/W)
ax1.plot(roof_drift_pct, coeff_V_W, color='#d62728', linewidth=2.5, label='Curva de Capacidad MVLEM')
ax1.scatter([roof_drift_pct[np.argmax(coeff_V_W)]], [cw_max], color='black', s=70, zorder=5,
            label=f'$V/W_{{máx}} = {cw_max:.3f}$')
ax1.set_title('Curva Normalizada de Capacidad (Muros Acoplados)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Deriva en Cubierta - Roof Drift [%]', fontsize=11)
ax1.set_ylabel('Coeficiente Sísmico $V_b / W$', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(frameon=True, facecolor='white', fontsize=10)

# Subplot 2: Cortante Basal [kN] vs Desplazamiento de Techo [m]
ax2.plot(dtecho, Vbasal, color='#1f77b4', linewidth=2.5, label='Respuesta Cortante Basal')
ax2.scatter([dtecho[np.argmax(Vbasal)]], [v_max], color='red', s=70, zorder=5,
            label=f'$V_{{b,máx}} = {v_max:.1f}$ kN')
ax2.set_title('Curva Cortante Basal vs Desplazamiento', fontsize=12, fontweight='bold')
ax2.set_xlabel(r'Desplazamiento de Cubierta $\Delta_{techo}$ [m]', fontsize=11)
ax2.set_ylabel(r'Cortante Basal $V_b$ [kN]', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(frameon=True, facecolor='white', fontsize=10)

plt.tight_layout()
plt.show()

print("\n🎉 Análisis de muros MVLEM finalizado exitosamente.")
