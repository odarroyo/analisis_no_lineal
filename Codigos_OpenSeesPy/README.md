# Curso de Análisis No Lineal - Códigos OpenSeesPy

Repositorio de desarrollo de material pedagógico, ejemplos prácticos y scripts computacionales para los estudiantes del curso de **Análisis No Lineal de Estructuras**.

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python `3.12` (detectado: `3.12.12` en macOS Apple Silicon / ARM64).
- **Motor de Simulación FEA:** [OpenSeesPy](https://openseespydoc.readthedocs.io/) (`openseespy-mac-arm` versión `3.7.1.4`).
- **Librerías Complementarias del Entorno:**
  - **Pre/Post-proceso y utilidades OpenSees:** `opseestools` (v1.20), `opstool` (v1.0.26).
  - **Visualización y Gráficas:** `opsvis` (v1.3.4), `matplotlib`, `plotly`, `pyvista`.
  - **Cálculo Numérico y Datos:** `numpy`, `scipy`, `pandas`.
  - **Análisis de Secciones:** `sectionproperties`.
  - **Entorno Interactivo:** `ipykernel`, `jupyter`.

---

## 🐍 Entorno Virtual (Virtual Environment)

El entorno virtual dedicado para este proyecto se encuentra configurado en:

```text
/Users/odarroyo/virtual_environments/venv_openseespy2
```

### Activación en Terminal

Para activar el entorno en la terminal (zsh/bash):

```bash
source /Users/odarroyo/virtual_environments/venv_openseespy2/bin/activate
```

O ejecutar scripts directamente con el intérprete del entorno:

```bash
/Users/odarroyo/virtual_environments/venv_openseespy2/bin/python <nombre_del_script>.py
```

### Configuración en el Editor (VS Code / Antigravity IDE)

Para asegurar que los scripts y notebooks utilicen este entorno:
1. Abrir la paleta de comandos (`Cmd + Shift + P`).
2. Escribir y seleccionar: **`Python: Select Interpreter`**.
3. Seleccionar o pegar la ruta del binario:
   ```text
   /Users/odarroyo/virtual_environments/venv_openseespy2/bin/python
   ```

---

## 📂 Contenido del Directorio

- **[master_script_pushover_with_masses_and_nodal_loads_N2.py](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/master_script_pushover_with_masses_and_nodal_loads_N2.py)**:
  Script original en Python del pórtico con retranqueos y variación de secciones.

- **Modelo Base (Pórtico con Retranqueos e Irregularidad en Altura):**
  - **[master_script_pushover_with_masses_and_nodal_loads_N2_colab.ipynb](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/master_script_pushover_with_masses_and_nodal_loads_N2_colab.ipynb)**: Cuaderno para Google Colab con el modelo que incluye retranqueos en piso 7, variación de secciones (60x60 y 55x55), diafragmas por nivel `[1, 1, 1, 1, 0, 1, 0]`, masas nodales y método N2.
  - **[master_script_pushover_with_masses_and_nodal_loads_N2_colab.py](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/master_script_pushover_with_masses_and_nodal_loads_N2_colab.py)**: Versión en script `.py` del modelo con retranqueos con protección local y auto-instalación en Colab.

- **Modelo Nuevo (Pórtico Completamente Regular):**
  - **[master_script_pushover_regular_colab.ipynb](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/master_script_pushover_regular_colab.ipynb)**: Cuaderno interactivo para Colab con el modelo **100% regular**: 3 vanos iguales de 6 m, 7 pisos de 3 m, secciones constantes de columnas (55x55 cm) y vigas (45x50 cm), diafragmas rígidos en todos los pisos, curva MDOF vs SDOF equivalente del Método N2 y perfiles de deriva.
  - **[master_script_pushover_regular_colab.py](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/master_script_pushover_regular_colab.py)**: Script Python ejecutable del modelo regular.

- **Modelo de Muros de Concreto Reforzado con Elementos MVLEM:**
  - **[MVLEM_generator_colab.ipynb](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/MVLEM_generator_colab.ipynb)**: Cuaderno interactivo para Google Colab basado en `MVLEM_generator2.py`. Modela un edificio de 16 pisos ($H = 41.6$ m) con 2 muros acoplados mediante elementos macro-fibra `MVLEM` (8 fibras axiales y resorte central de cortante), concreto `Concrete02` (confinado en bordes y no confinado en alma), acero `Hysteretic`, vigas de enlace `elasticBeamColumn`, diafragmas rígidos y análisis Pushover con curvas de capacidad $V_b/W$ vs. Roof Drift Ratio (%) y $V_b$ vs. $\Delta_{\text{techo}}$.
  - **[MVLEM_generator_colab.py](file:///Users/odarroyo/Library/CloudStorage/OneDrive-Personal/3.%20Docencia/0.%20Cursos/18.Analisis_no_lineal/Codigos_OpenSeesPy/MVLEM_generator_colab.py)**: Versión ejecutable en script Python del modelo MVLEM con auto-instalación para Colab y protección local.

---

## 🎯 Guía para el Desarrollo de Nuevo Material Docente

Al desarrollar nuevos módulos, scripts o notebooks para las clases:
1. **Claridad didáctica:** Explicar los pasos fundamentales del modelado (Definición geométrica $\to$ Materiales $\to$ Secciones $\to$ Elementos $\to$ Cargas gravitacionales $\to$ Análisis no lineal).
2. **Visualización gráfica:** Acompañar los modelos con diagramas de mallas (`opsvis`), curvas de capacidad ($V_b$ vs. $\Delta_{\text{techo}}$), diagramas de momento-curvatura ($M-\phi$) y respuestas en el tiempo cuando aplique.
3. **Modularidad:** Utilizar funciones reutilizables y parámetros claros para que los estudiantes puedan modificar secciones, derivas objetivo y patrones de carga fácilmente.
