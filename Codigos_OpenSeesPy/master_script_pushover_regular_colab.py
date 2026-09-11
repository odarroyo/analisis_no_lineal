#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CURSO DE ANÁLISIS NO LINEAL DE ESTRUCTURAS
Script: Pushover No Lineal - Pórtico Completamente Regular (Colab & Local)
Profesor: Orlando Arroyo
================================================================================

Este script modela un pórtico 2D de concreto reforzado COMPLETAMENTE REGULAR:
- Geometría: 3 vanos de 6.0 m y 7 pisos de 3.0 m (H = 21.0 m, L = 18.0 m).
- Secciones: Mismas dimensiones y refuerzo para todas las columnas (55x55 cm)
  y vigas (45x50 cm) en todos los niveles.
- Diafragmas rígidos horizontales activos en el 100% de los pisos.
- Cargas gravitacionales y masas nodales homogéneas.
- Normalización Método N2 (Fajfar, 2000): Curva MDOF y Curva SDOF equivalente.
- Compatible con Google Colab y ejecución local protegida para Mac ARM.
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
import opseestools.utilidades as ut
import opsvis as opsv
import numpy as np
import pandas as pd

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('default')

# %% [2] Inicialización del Modelo
# Unidades consistentes:
# - Longitud: metros [m]
# - Fuerza: kilonewtons [kN]
# - Esfuerzo: megapascales [MPa] -> kPa en OpenSees
# - Masa: toneladas métricas [ton] = [kN * s^2 / m]
# - Aceleración: m/s^2 (g = 9.81 m/s^2)

wipe()
model('basic', '-ndm', 2, '-ndf', 3)
print("🏗️ Modelo 2D regular inicializado (Ux, Uy, Rz).")

# %% [3] Geometría Completamente Regular
coordx = [0.0, 6.0, 12.0, 18.0]        # 3 vanos iguales de 6.0 m
coordy = [3.0 * i for i in range(8)]    # 7 pisos iguales de 3.0 m

ut.creategrid(coordx, coordy)
fixY(0.0, 1, 1, 1)

n_bays = len(coordx) - 1
n_stories = len(coordy) - 1
print(f"📐 Geometría regular: {n_bays} vanos y {n_stories} pisos (H = {coordy[-1]} m).")

# %% [4] Definición de Materiales No Lineales
fc = 28   # Resistencia a compresión del concreto [MPa]
fy = 420  # Límite elástico del acero [MPa]

tag_noconf, tag_conf, tag_acero = ut.col_materials(fc, fy, detailing='DMO', nps=3)
print(f"🧱 Materiales creados: Concreto No Confinado ({tag_noconf}), Confinado ({tag_conf}), Acero ({tag_acero}).")

# %% [5] Secciones Regulares Únicas
Bcol, Hcol = 0.55, 0.55  # Columna única 55x55 cm
Bvig, Hvig = 0.45, 0.50  # Viga única 45x50 cm
c = 0.05                 # Recubrimiento [m]

As4 = 0.000127 # Barra #4
As6 = 0.000280 # Barra #6
As8 = 0.000508 # Barra #8

col_sec = 101
vig_sec = 201

# Columna 55x55 cm: 5 #8 arriba, 5 #8 abajo, 6 #8 en caras laterales
ut.create_rect_RC_section(col_sec, Hcol, Bcol, c, tag_conf, tag_noconf, tag_acero, 5, As8, 5, As8, 6, As8)
# Viga 45x50 cm: 9 #6 superior, 5 #4 inferior
ut.create_rect_RC_section(vig_sec, Hvig, Bvig, c, tag_conf, tag_noconf, tag_acero, 9, As6, 5, As4)
print("📏 Secciones regulares definidas: Columna 55x55 cm y Viga 45x50 cm.")

# %% [6] Elementos y Diafragmas Regulares
tagcols, tagbeams = ut.create_elements(coordx, coordy, col_sec, vig_sec, dia=1)
print(f"🏢 Estructura regular ensamblada: {len(tagcols)} columnas y {len(tagbeams)} vigas. Diafragmas en todos los pisos.")

# %% [7] Cargas Gravitacionales Regulares en Vigas
floor_load = -70.0  # kN/m en entrepisos
roof_load  = -50.0  # kN/m en cubierta
ut.load_beams(floor_load, roof_load, tagbeams)
print(f"⚖️ Cargas uniformes aplicadas: {floor_load} kN/m en entrepisos y {roof_load} kN/m en cubierta.")

# %% [8] Asignación de Masas Nodales
default_mass = 20.0  # ton en X e Y
nodes_tags = np.array(getNodeTags())
coordy_all = np.array([nodeCoord(int(i))[1] for i in nodes_tags])

for tag, y in zip(nodes_tags, coordy_all):
    if y > 0:
        mass(int(tag), default_mass, default_mass, 0.0)

print(f"🏋️ Masas nodales de {default_mass} ton asignadas a los {sum(coordy_all > 0)} nodos de superestructura.")

# %% [9] Análisis Modal y Método N2
w2 = eigen(n_stories)
modal_props = modalProperties('-print', '-unorm', '-return')

periods = modal_props.get('eigenPeriod', [2*np.pi/np.sqrt(v) for v in w2])
gamma_N2 = modal_props.get('partiFactorMX', [1.287])[0]

print("\n" + "="*55)
print("🎯 RESULTADOS DEL ANÁLISIS MODAL (PÓRTICO REGULAR)")
print("="*55)
for i in range(min(4, len(periods))):
    print(f"  Modo {i+1}: Periodo T = {periods[i]:.4f} s | Frecuencia f = {1.0/periods[i]:.3f} Hz")
print(f"  Factor de Participación Modal N2 (Modo 1): Gamma = {gamma_N2:.4f}")
print("="*55 + "\n")

# %% [10] Análisis de Gravedad y Visualización del Modelo
an.gravedad()
loadConst('-time', 0.0)
print("✅ Cargas de gravedad convergidas.")

try:
    plt.figure(figsize=(7.5, 6.5))
    opsvis.plot_model(node_labels=1, element_labels=1, gauss_points=False)
    plt.title("Pórtico 2D Regular - Nodos y Elementos", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"(Visualización opsvis omitida en modo consola: {e})")

# %% [11] Análisis Pushover No Lineal
leftmost_nodes = ut.find_leftmost_nodes(coordy)
ut.pushover_loads(coordy, nodes=leftmost_nodes)
elements = tagcols + tagbeams
nodes_control = [1000] + [int(i) for i in leftmost_nodes]

H_total = coordy[-1]
Dmax = 0.05 * H_total
Dincr = 0.001
ctrl_node = getNodeTags()[-1]

print(f"🚀 Iniciando Pushover regular (Control en nodo {ctrl_node}, Dmax = {Dmax:.3f} m)...")
dtecho, Vbasal, drifts, rotations = an.pushover2DRot(
    Dmax, Dincr, ctrl_node, 1, nodes_control, elements
)

dtecho = np.array(dtecho)
Vbasal = np.array(Vbasal)
story_drifts = drifts[:len(dtecho), :]

d_ult = dtecho[-1] if len(dtecho) > 0 else 0.0
v_max = max(Vbasal) if len(Vbasal) > 0 else 0.0
print(f"🏁 Pushover regular finalizado. Desplazamiento: {d_ult:.4f} m | Cortante basal máximo: {v_max:.2f} kN")

# Curva SDOF equivalente N2
d_star = dtecho / gamma_N2
F_star = Vbasal / gamma_N2

# %% [12] Gráficas de Resultados
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Subplot A: Curva MDOF
ax1.plot(dtecho, Vbasal, color='#1f77b4', linewidth=2.5, label='Curva de Capacidad MDOF')
ax1.scatter([dtecho[np.argmax(Vbasal)]], [v_max], color='red', s=70, zorder=5, label=f'$V_{{b,máx}} = {v_max:.1f}$ kN')
ax1.set_title('Curva de Capacidad MDOF (Pórtico Regular)', fontsize=12, fontweight='bold')
ax1.set_xlabel(r'Desplazamiento Techo $\Delta_{techo}$ [m]', fontsize=11)
ax1.set_ylabel(r'Cortante Basal $V_b$ [kN]', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(frameon=True, facecolor='white', fontsize=10)

# Subplot B: SDOF Equivalente N2
ax2.plot(d_star, F_star, color='#2ca02c', linewidth=2.5, label='Curva SDOF ($F^* - d^*$)')
ax2.scatter([d_star[np.argmax(F_star)]], [max(F_star)], color='darkgreen', s=70, zorder=5, label=f'$F^*_{{máx}} = {max(F_star):.1f}$ kN')
ax2.set_title(rf'Curva SDOF Equivalente N2 ($\Gamma = {gamma_N2:.3f}$)', fontsize=12, fontweight='bold')
ax2.set_xlabel(r'Desplazamiento SDOF $d^*$ [m]', fontsize=11)
ax2.set_ylabel(r'Fuerza SDOF $F^*$ [kN]', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(frameon=True, facecolor='white', fontsize=10)

plt.tight_layout()
plt.show()

# Perfil de derivas
if story_drifts.shape[1] > 0:
    plt.figure(figsize=(7, 6))
    num_floors = story_drifts.shape[1]
    floors = list(range(1, num_floors + 1))
    idx_50 = len(dtecho) // 2

    plt.plot(story_drifts[idx_50, :] * 100, floors, 'o--', color='#ff7f0e', linewidth=2,
             label=rf'50% Pushover ($\Delta = {dtecho[idx_50]:.3f}$ m)')
    plt.plot(story_drifts[-1, :] * 100, floors, 's-', color='#d62728', linewidth=2.2,
             label=rf'Estado Último ($\Delta = {dtecho[-1]:.3f}$ m)')
    plt.axvline(1.0, color='black', linestyle=':', linewidth=1.5, label='Límite Normativo Deriva (1.0%)')

    plt.title('Perfil Regular de Derivas de Entrepiso (%)', fontsize=13, fontweight='bold')
    plt.xlabel('Deriva de Entrepiso [%]', fontsize=11)
    plt.ylabel('Nivel de Piso', fontsize=11)
    plt.yticks(floors)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', fontsize=10)
    plt.tight_layout()
    plt.show()

print("\n🎉 Análisis del pórtico regular completado con éxito.")
