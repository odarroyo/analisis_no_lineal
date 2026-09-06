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
* **Objetivo:** Determinar la curva de capacidad resistente y la ductilidad global de una estructura sometida a un patrón de cargas laterales triangular proporcional a la altura mediante control por desplazamiento.
* **Características:**
  * Edificio cortante de 2 pisos (2-DOF) sometido a un vector de fuerzas laterales proporcionales $F_1 = \lambda/3$, $F_2 = 2\lambda/3$ donde el factor de carga $\lambda$ es una incógnita del equilibrio.
  * **Algoritmo de Control por Desplazamiento:** Incrementos secuenciales de desplazamiento objetivo en el techo $\Delta u_2$ y resolución iterativa de $\lambda$ y $u_1$ con Newton-Raphson bajo restricción cinemática.
  * **Curva de Capacidad Pushover en Tiempo Real:** Gráfica interactiva de cortante basal $V_b$ vs. desplazamiento de techo $u_2$ con puntos de estado marcados paso a paso.
  * **Inspector Matricial y Secuencia de Plastificación:** Desglose interactivo de las ecuaciones ampliadas, determinación del estado elasto-plástico por entrepiso y visualización física de la estructura deformada.

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
