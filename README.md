# Análisis No Lineal de Estructuras 🏢⚡

**Prof. Orlando Arroyo**  
*Universidad Industrial de Santander (UIS)*  
*Escuela de Ingeniería Civil — Posgrado en Ingeniería Estructural*

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen?style=flat-square&logo=github)](https://odarroyo.github.io/analisis_no_lineal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Plataforma educativa y conjunto de laboratorios computacionales interactivos diseñados para la docencia universitaria del curso de **Análisis No Lineal de Estructuras**.

🔗 **Acceso en vivo a la plataforma web:**  
👉 **[https://odarroyo.github.io/analisis_no_lineal/](https://odarroyo.github.io/analisis_no_lineal/)**

---

## 📚 Contenido de los Módulos

### 1. [Clase 01 — La Trayectoria Importa: Memoria Estructural e Histéresis](https://odarroyo.github.io/analisis_no_lineal/01_la_trayectoria_importa.html)
* **Objetivo:** Demostrar que los desplazamientos máximos o el estado de deformación final no determinan el estado resistente interno de una estructura no lineal.
* **Características:**
  * Simulación en tiempo real de un oscilador bilineal de 1 grado de libertad (1-DOF).
  * Control de rigidez elástica inicial $K_0$, fuerza de fluencia $F_y$ y pendiente post-fluencia $\alpha$.
  * Editor interactivo de historias de desplazamiento arbitrarias (ciclos, pulsos, reversiones de carga).
  * Visualización de histéresis elastoplástica con endurecimiento cinemático y seguimiento de memoria estructural.
  * Comparador de trayectorias (monotónica vs cíclica) con idéntico punto final pero respuestas internas radicalmente distintas.

### 2. [Clase 02 — El Equilibrio Iterativo y Newton-Raphson](https://odarroyo.github.io/analisis_no_lineal/02_equilibrio_newton_raphson.html)
* **Objetivo:** Comprender la resolución iterativa del equilibrio no lineal $\mathbf{P} - \mathbf{F}_{\text{int}}(\mathbf{u}) = \mathbf{0}$.
* **Características:**
  * Edificio cortante de 2 pisos (2-DOF) con resortes elastoplásticos independientes por entrepiso y animación cinemática.
  * Algoritmos de solución comparados: **Newton-Raphson Estándar** (actualización completa de $\mathbf{K}_t$) vs **Newton-Raphson Modificado** (rigidez constante elástica $\mathbf{K}_0$).
  * **Inspector Matricial y Desglose Operacional Paso a Paso:** Identificación física de cada elemento estructural en el ensamblaje de la matriz de rigidez tangente $\mathbf{K}_t$, cálculo de residuos nodales $\mathbf{r}$, determinante, y correcciones cinemáticas $\delta \mathbf{u}$.
  * **Mini-Simulador 1D Interactivo:** Intuición geométrica de las tangentes y residuos con autoescala dinámica (sin desbordamientos visuales) y control de pendiente post-fluencia.

### 3. [Clase 03 — Análisis Estático No Lineal: Pushover](https://odarroyo.github.io/analisis_no_lineal/03_analisis_pushover.html)
* **Objetivo:** Determinar la curva de capacidad resistente, ductilidad global y degradación post-pico de una edificación sometida a un patrón de cargas laterales triangular mediante control por desplazamiento, con leyes constitutivas trilineales completas.
* **Características:**
  * Edificio cortante de 2 pisos (2-DOF) sometido a un vector de fuerzas proporcionales $F_1 = \lambda/3$, $F_2 = 2\lambda/3$ donde el factor de carga $\lambda$ es una incógnita del equilibrio.
  * **Algoritmo de Control por Desplazamiento:** Incrementos secuenciales de desplazamiento de techo $\Delta u_2$ y resolución iterativa de $\lambda$ y $u_1$ con Newton-Raphson bajo restricción cinemática.
  * **Leyes Constitutivas Trilineales con Ablandamiento:** Rama 1 (Elástica), Rama 2 (Endurecimiento) hasta desplazamiento pico $\Delta_p$, y Rama 3 (Ablandamiento descendente $k_t < 0$) hasta resistencia residual $F_{\text{res}}$.
  * **Curva de Capacidad con Rama Descendente ($K_{\text{push}} < 0$):** Demostración interactiva de superación de puntos límite y descenso ordenado por la rama de degradación sin divergencia numérica.
  * **Mecanismos de Colapso (Piso Blando vs. Piso Alto):** Concentración severa de deformaciones en el entrepiso degradado mientras los pisos no críticos experimentan descarga elástica reversible.
  * **Inspector Matricial y Desglose Operacional:** Visualización en vivo del equilibrio exacto ($\mathbf{P} - \mathbf{F}_{\text{int}} = \mathbf{0}$) aun cuando la matriz tangente $[\mathbf{K}_t]$ es indefinida y $\det(\mathbf{K}_t) < 0$.
### 4. [Clase 04 — La Rótula Plástica: Modelo Concentrado ASCE 41 y Equilibrio en Voladizo](https://odarroyo.github.io/analisis_no_lineal/04_rotula_plastica_asce41.html)
* **Objetivo:** Demostrar cómo funciona una rótula plástica concentrada bajo la norma ASCE 41 en una columna en voladizo, analizando el acoplamiento cinemático en serie, el equilibrio estático de secciones y la descarga elástica (*springback*) durante el ablandamiento.
* **Características:**
  * Columna en voladizo con parámetros geométricos totalmente configurables: longitud $L$ (def. 3 m), ancho $b$ y peralte $d$.
  * Rótula plástica tipo ASCE 41 ubicada a $x_h = 0.05 L$ mediante un resorte rotacional no lineal en serie con el fuste elástico.
  * Curva troncal ASCE 41 completa (puntos A, B, C, D, E) con niveles de desempeño sísmico: **IO** (Immediate Occupancy), **LS** (Life Safety) y **CP** (Collapse Prevention).
  * **Visualización en 4 Lienzos HiDPI Simultáneos:** Deformada física de la columna con rótula coloreada según su estado, DCL con corte en la rótula y diagrama de momentos $M(x)$, curva pushover global $V-\Delta$ y curva constitutiva $M_h-\theta_h$.
  * **Demostración de Descarga Elástica (*Springback*):** En la rama descendente C–D, al degradarse la rótula, la fuerza lateral $V$ cae y el fuste elástico se endereza ($\Delta_{\text{el}}$ disminuye), mientras la rotación plástica $\theta_h$ crece aceleradamente para acomodar el desplazamiento global $\Delta$.
  * Inspector numérico de equilibrio en vivo con residuo exacto $|V \cdot 0.95L - M_h| = 0.00\text{ kN}\cdot\text{m}$ y módulo socrático interactivo con retroalimentación conceptual inmediata.

---

## 🎨 Características de Diseño
* **Modo Claro por Defecto:** Optimizado para proyección en aulas universitarias con alto contraste y fondos sólidos en lienzos Canvas 2D.
* **Modo Oscuro:** Alternable en cualquier momento con un clic y persistente en el navegador.
* **Autónomo e Independiente:** Todo el código funciona directamente en el navegador sin requerir servidores de backend, Node.js ni compiladores.

---

## 💻 Ejecución Local
Para abrir localmente los laboratorios sin conexión a internet:
1. Clona el repositorio:
   ```bash
   git clone https://github.com/odarroyo/analisis_no_lineal.git
   cd analisis_no_lineal
   ```
2. Abre `index.html` en cualquier navegador web moderno (Chrome, Firefox, Safari, Edge):
   ```bash
   open index.html
   ```

---

## 👨‍🏫 Autor y Contacto
* **Prof. Orlando Arroyo**  
* Universidad Industrial de Santander (UIS)  
* Escuela de Ingeniería Civil  
