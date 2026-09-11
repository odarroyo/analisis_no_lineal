#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CURSO DE ANÁLISIS NO LINEAL DE ESTRUCTURAS
Script: Pushover No Lineal con Masas, Cargas Nodales y Método N2
Modelo de Pórtico con Irregularidad en Altura y Retranqueos (Colab & Local)
Profesor: Orlando Arroyo
================================================================================

Este script realiza el análisis estático no lineal (Pushover) del modelo base:
- Geometría de pórtico 2D con vanos variables (5 m, 7 m, 6 m) y 7 niveles.
- Retranqueo en el piso 7 (sin columnas exteriores) y vano abierto en el piso 5.
- Secciones diferenciadas: Columnas 60x60 cm en pisos inferiores y 55x55 cm arriba;
  vigas de 45x60 cm y 45x50 cm.
- Diafragmas rígidos selectivos por piso [1, 1, 1, 1, 0, 1, 0].
- Cargas gravitacionales por viga y asignación activa de masas nodales.
- Normalización y obtención de factores para el Método N2.
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
import itertools

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('default')

# %% [2] Inicialización del Modelo
wipe()
model('basic', '-ndm', 2, '-ndf', 3)
print("🏗️ Modelo 2D inicializado (2D, 3 GDL/nodo).")

# %% [3] Nodos y Apoyos
coordx = [0.0, 5.0, 12.0, 18.0]
coordy = [3.0 * i for i in range(8)]
ut.creategrid(coordx, coordy)
fixY(0.0, 1, 1, 1)
print(f"📐 Malla nodal creada: Ejes X={coordx}, 7 pisos de 3 m (H = {coordy[-1]} m).")

# %% [4] Definición de Materiales No Lineales
fc = 28   # MPa
fy = 420  # MPa
tag_noconf, tag_conf, tag_acero = ut.col_materials(fc, fy, detailing='DMO', nps=3)
print(f"🧱 Materiales no lineales: Concreto No Confinado ({tag_noconf}), Confinado ({tag_conf}), Acero ({tag_acero}).")

# %% [5] Secciones de Concreto Reforzado
Bcol, Hcol = 0.55, 0.55
Bcol2, Hcol2 = 0.60, 0.60
Bvig, Hvig = 0.45, 0.50
Bvig2, Hvig2 = 0.45, 0.60
c = 0.05

As4 = 0.000127
As5 = 0.000200
As6 = 0.000280
As7 = 0.003870
As8 = 0.000508

col55x55 = 101
col60x60 = 102
vig45x50 = 201
vig45x60 = 202

ut.create_rect_RC_section(col55x55, Hcol, Bcol, c, tag_conf, tag_noconf, tag_acero, 5, As8, 5, As8, 6, As8)
ut.create_rect_RC_section(vig45x50, Hvig, Bvig, c, tag_conf, tag_noconf, tag_acero, 9, As6, 5, As4)
ut.create_rect_RC_section(col60x60, Hcol2, Bcol2, c, tag_conf, tag_noconf, tag_acero, 5, As8, 5, As8, 6, As8)
ut.create_rect_RC_section(vig45x60, Hvig2, Bvig2, c, tag_conf, tag_noconf, tag_acero, 9, As6, 5, As4)
print("📏 Secciones transversales de fibra definidas (col55, col60, vig50, vig60).")

# %% [6] Elementos, Retranqueos y Diafragmas
columns_floor1 = [col55x55, col60x60, col60x60, col55x55]
columns_floor2 = [col55x55, col60x60, col60x60, col55x55]
columns_floor3 = [col55x55, col60x60, col60x60, col55x55]
columns_floor4 = [col55x55, col55x55, col55x55, col55x55]
columns_floor5 = [col55x55, col55x55, col55x55, col55x55]
columns_floor6 = [col55x55, col55x55, col55x55, col55x55]
columns_floor7 = ['None', col55x55, col55x55, 'None'] # Retranqueo en piso 7

building_columns = [
    columns_floor1, columns_floor2, columns_floor3,
    columns_floor4, columns_floor5, columns_floor6, columns_floor7
]

beams_floor1 = [vig45x50, vig45x60, vig45x60]
beams_floor2 = [vig45x50, vig45x60, vig45x60]
beams_floor3 = [vig45x50, vig45x60, vig45x60]
beams_floor4 = [vig45x50, vig45x60, vig45x60]
beams_floor5 = [vig45x50, 'None', vig45x50]          # Sin viga en el vano central
beams_floor6 = [vig45x50, vig45x50, vig45x50]
beams_floor7 = ['None', vig45x50, 'None']             # Viga solo en el vano central

building_beams = [
    beams_floor1, beams_floor2, beams_floor3,
    beams_floor4, beams_floor5, beams_floor6, beams_floor7
]

tagcols, tagbeams, column_info, beam_info = ut.create_elements2(
    coordx, coordy, building_columns, building_beams, output=0
)
ut.remove_hanging_nodes(tagcols, tagbeams)

floor_diaphragms = [1, 1, 1, 1, 0, 1, 0]
ut.apply_diaphragms(floor_diaphragms, output=0)
print(f"🏢 Estructura ensamblada: {len(tagcols)} columnas y {len(tagbeams)} vigas. Diafragmas aplicados: {floor_diaphragms}.")

# %% [7] Cargas Gravitacionales Distribuidas
beams_loads_floor1 = [-70, -70, -70]
beams_loads_floor2 = [-70, -70, -70]
beams_loads_floor3 = [-70, -70, -70]
beams_loads_floor4 = [-70, -70, -70]
beams_loads_floor5 = [-70, -70]
beams_loads_floor6 = [-70, -70, -70]
beams_loads_floor7 = [-50]

beam_loads = [
    beams_loads_floor1, beams_loads_floor2, beams_loads_floor3,
    beams_loads_floor4, beams_loads_floor5, beams_loads_floor6, beams_loads_floor7
]
ut.load_beams2(beam_loads, tagbeams, output=0)
print("⚖️ Cargas gravitacionales por viga asignadas.")

# %% [8] Asignación de Masas Nodales
# Masa en toneladas métricas [ton] = [kN * s^2 / m]
nodes_tags_updated = np.array(getNodeTags())
coordx_updated = np.array([nodeCoord(int(i))[0] for i in nodes_tags_updated])
coordy_updated = np.array([nodeCoord(int(i))[1] for i in nodes_tags_updated])

default_nodal_mass = 20.0 # ton

for tag, y in zip(nodes_tags_updated, coordy_updated):
    if y > 0:
        mass(int(tag), default_nodal_mass, default_nodal_mass, 0.0)

print(f"🏋️ Masas nodales de {default_nodal_mass} ton asignadas a los {sum(coordy_updated > 0)} nodos elevados.")

# %% [9] Análisis Modal y Parámetros del Método N2
num_modes = len(coordy) - 1
w2 = eigen(num_modes)
modal_props = modalProperties('-print', '-unorm', '-return')

periods = modal_props.get('eigenPeriod', [2*np.pi/np.sqrt(v) for v in w2])
gamma_N2 = modal_props.get('partiFactorMX', [1.3])[0]

print("\n" + "="*50)
print("🎯 RESULTADOS DEL ANÁLISIS MODAL")
print("="*50)
for i in range(min(4, len(periods))):
    print(f"  Modo {i+1}: Periodo T = {periods[i]:.4f} s | Frecuencia f = {1.0/periods[i]:.3f} Hz")
print(f"  Factor de Participación Modal N2 (Modo 1): Gamma = {gamma_N2:.4f}")
print("="*50 + "\n")

# %% [10] Análisis de Gravedad y Visualización del Modelo
an.gravedad()
loadConst('-time', 0.0)
print("✅ Análisis de cargas gravitacionales completado.")

try:
    plt.figure(figsize=(7.5, 6.5))
    opsvis.plot_model(node_labels=1, element_labels=1, gauss_points=False)
    plt.title("Modelo Estructural 2D - Nodos y Elementos", fontsize=12, fontweight='bold')
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

print(f"🚀 Iniciando Pushover (Control en nodo {ctrl_node}, Dmax = {Dmax:.3f} m)...")
dtecho, Vbasal, drifts, rotations = an.pushover2DRot(
    Dmax, Dincr, ctrl_node, 1, nodes_control, elements
)

dtecho = np.array(dtecho)
Vbasal = np.array(Vbasal)
story_drifts = drifts[:len(dtecho), :]
column_rotations = rotations[:len(tagcols), :len(dtecho), [1, 2]]
beam_rotations = rotations[len(tagcols):, :len(dtecho), [1, 2]]

d_ult = dtecho[-1] if len(dtecho) > 0 else 0.0
v_max = max(Vbasal) if len(Vbasal) > 0 else 0.0
print(f"🏁 Pushover finalizado. Desplazamiento máximo: {d_ult:.4f} m | Cortante basal máximo: {v_max:.2f} kN")

# SDOF equivalente
d_star = dtecho / gamma_N2
F_star = Vbasal / gamma_N2

# %% [12] Gráficas Didácticas de Resultados
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Subplot A: Curva MDOF
ax1.plot(dtecho, Vbasal, color='#1f77b4', linewidth=2.5, label='Curva de Capacidad MDOF')
ax1.scatter([dtecho[np.argmax(Vbasal)]], [v_max], color='red', s=70, zorder=5, label=f'$V_{{b,máx}} = {v_max:.1f}$ kN')
ax1.set_title('Curva de Capacidad MDOF', fontsize=12, fontweight='bold')
ax1.set_xlabel(r'Desplazamiento Techo $\Delta_{techo}$ [m]', fontsize=11)
ax1.set_ylabel(r'Cortante Basal $V_b$ [kN]', fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(frameon=True, facecolor='white', fontsize=10)

# Subplot B: SDOF Equivalente N2
ax2.plot(d_star, F_star, color='#2ca02c', linewidth=2.5, label='Curva SDOF ($F^* - d^*$')
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

    plt.title('Perfil de Derivas de Entrepiso (%)', fontsize=13, fontweight='bold')
    plt.xlabel('Deriva de Entrepiso [%]', fontsize=11)
    plt.ylabel('Nivel de Piso', fontsize=11)
    plt.yticks(floors)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', fontsize=10)
    plt.tight_layout()
    plt.show()

print("\n🎉 Ejecución completada con éxito.")
