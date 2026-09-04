# Primera clase: Introducción al análisis no lineal de estructuras de concreto

## Idea central de la clase

> **La estructura tiene memoria.**

El objetivo de esta primera clase no es desarrollar todavía en detalle los algoritmos o modelos constitutivos del análisis no lineal. La intención es producir un **cambio de paradigma** respecto a la forma en que los estudiantes han aprendido tradicionalmente el análisis estructural.

La idea que debe quedar instalada al final de la sesión es que, en un problema no lineal, la respuesta futura de la estructura no depende únicamente de la carga actual, sino también del **estado interno alcanzado y de la trayectoria seguida para llegar hasta él**.

En análisis lineal solemos pensar en estados independientes. En análisis no lineal debemos seguir la **evolución de un sistema**.

---

# 1. Apertura: *Jurassic Park* y la idea de trayectoria

La clase puede comenzar con la escena de *Jurassic Park* en la que Ian Malcolm explica la teoría del caos utilizando dos gotas de agua sobre la mano de Ellie.

Después de proyectar la escena, plantear la pregunta:

> **¿Por qué la segunda gota no sigue exactamente el mismo camino que la primera?**

Permitir que los estudiantes propongan explicaciones:

- pequeñas diferencias en las condiciones iniciales;
- irregularidades;
- sensibilidad del sistema;
- influencia del estado previo;
- trayectoria.

A continuación, introducir la frase central:

> **Una estructura no lineal tiene memoria.**

Es importante aclarar inmediatamente:

> No se está afirmando que un sistema estructural no lineal sea necesariamente caótico. Lo relevante de la escena es la idea de que, para anticipar lo que ocurrirá después, necesitamos conocer el estado en el que se encuentra actualmente el sistema.

Esta escena sirve como puerta de entrada a varios conceptos que aparecerán a lo largo del curso:

- estado;
- historia;
- trayectoria;
- incrementalidad;
- iteración;
- evolución de la rigidez;
- daño y deformación residual.

---

# 2. El mundo cómodo del análisis lineal

Escribir en el tablero:

\[
\mathbf{K}\mathbf{u}=\mathbf{P}
\]

y preguntar:

> **¿Qué estamos suponiendo cuando escribimos esta ecuación?**

La discusión debería conducir a reconocer, entre otras, las siguientes hipótesis:

- la matriz de rigidez \(\mathbf{K}\) es conocida;
- \(\mathbf{K}\) no cambia con el desplazamiento;
- la respuesta es proporcional a la carga;
- si se duplica \(\mathbf{P}\), se duplica \(\mathbf{u}\);
- puede aplicarse el principio de superposición;
- el camino seguido para llegar al estado actual no importa;
- descargar conduce nuevamente al origen;
- el equilibrio puede formularse esencialmente sobre la configuración inicial.

Debe evitarse presentar estas hipótesis como “incorrectas”.

Una transición posible es:

> El análisis lineal no está mal. Es una de las aproximaciones más poderosas de la ingeniería estructural. El problema aparece cuando utilizamos sus hipótesis fuera del dominio en el que son razonables.

---

# 3. Experimento mental central: dos estructuras aparentemente iguales

Dibujar dos elementos de concreto reforzado aparentemente idénticos.

## Elemento A

Nunca ha sido sometido a cargas significativas.

## Elemento B

Fue previamente cargado hasta:

- fisurar el concreto;
- producir fluencia del acero;
- o desarrollar deformaciones inelásticas;

y posteriormente fue descargado.

Plantear:

> **Si ambos elementos se encuentran ahora bajo la misma carga y aplicamos exactamente el mismo incremento de carga, ¿responderán igual?**

La respuesta esperada es que no necesariamente.

Preguntar:

> **¿Por qué?**

Las respuestas pueden incluir:

- fisuración previa;
- reducción de rigidez;
- deformación residual;
- fluencia;
- daño;
- apertura y cierre de fisuras;
- cambios en variables internas del material.

Introducir entonces:

\[
\boxed{\text{Estado actual} \neq \text{solo carga actual}}
\]

y posteriormente:

\[
\boxed{
\text{Respuesta futura}
=
f(\text{estado actual},\text{historia},\text{incremento})
}
\]

Esta es una de las relaciones conceptuales más importantes de toda la clase.

---

# 4. De una solución a una trayectoria

## Análisis lineal

Representar una relación fuerza-desplazamiento lineal:

\[
F=Ku
\]

Se puede seleccionar cualquier punto de la recta y obtener directamente su respuesta.

La idea a enfatizar es:

> **No necesito saber cómo llegué hasta ese punto.**

## Análisis no lineal

Dibujar una curva fuerza-desplazamiento que incluya, por ejemplo:

- respuesta aproximadamente elástica;
- fisuración;
- cambio de rigidez;
- fluencia;
- postfluencia.

Seleccionar un punto sobre la curva y plantear:

> **Aquí ya no puedo preguntar únicamente cuál es el desplazamiento correspondiente a una determinada fuerza. Necesito saber cómo llegué hasta aquí.**

Introducir la frase:

> **El análisis no lineal no consiste en encontrar un punto. Consiste en construir una trayectoria.**

---

# 5. Primer contacto con la incrementalidad

Introducir una secuencia de estados:

\[
\mathbf{P}_1
\rightarrow
\mathbf{P}_2
\rightarrow
\mathbf{P}_3
\rightarrow
\cdots
\]

o, en un análisis controlado por desplazamiento:

\[
u_1
\rightarrow
u_2
\rightarrow
u_3
\rightarrow
\cdots
\]

La idea es explicar que no se intenta saltar directamente desde el estado inicial hasta la respuesta final.

Se hace avanzar el sistema mediante incrementos.

\[
\boxed{
\text{Estado}_n
\longrightarrow
\text{Estado}_{n+1}
}
\]

El estado convergido en el paso \(n\) se convierte en el punto de partida del paso \(n+1\).

Mensaje clave:

> **En análisis no lineal, cada solución depende de la solución anterior.**

---

# 6. Incrementar no es suficiente: aparece el problema del equilibrio

Suponer que se parte de un estado conocido y se aplica un incremento:

\[
\Delta P
\]

Con una rigidez tangente puede obtenerse una primera estimación:

\[
\Delta u
\approx
K_t^{-1}\Delta P
\]

Mostrar gráficamente que una extrapolación empleando la tangente puede llevar a un punto que no pertenece a la curva real de respuesta.

Plantear entonces:

> **¿Qué hacemos si nuestra primera estimación no satisface el equilibrio?**

Respuesta:

> **Corregir.**

Introducir el residuo:

\[
R=P-F_{\text{int}}
\]

o, de forma más general:

\[
\mathbf{r}
=
\mathbf{P}
-
\mathbf{R}(\mathbf{u})
\]

No es necesario desarrollar todavía formalmente el método de Newton-Raphson. Basta con introducir su lógica:

1. proponer una solución;
2. evaluar el desequilibrio;
3. corregir;
4. volver a evaluar;
5. repetir hasta converger.

Frase sugerida:

> **Un análisis no lineal no obtiene la respuesta de una vez. La persigue.**

---

# 7. Tres fuentes de no linealidad

En esta primera clase solo se presenta el mapa conceptual. Cada tema puede desarrollarse posteriormente.

## 7.1 No linealidad del material

En concreto reforzado pueden aparecer:

### Concreto

- fisuración;
- pérdida de rigidez;
- aplastamiento;
- confinamiento;
- degradación;
- apertura y cierre de fisuras.

### Acero

- fluencia;
- endurecimiento;
- respuesta cíclica;
- efecto Bauschinger;
- histéresis.

Representación conceptual:

\[
\sigma
=
f(\varepsilon,\text{historia})
\]

---

## 7.2 No linealidad geométrica

Mostrar una columna sometida a carga axial \(P\) y desplazamiento lateral \(\Delta\).

El momento adicional asociado a la geometría deformada puede expresarse conceptualmente como:

\[
M=P\Delta
\]

Idea clave:

> **Incluso con un material perfectamente elástico puede existir una respuesta estructural no lineal si los cambios de geometría son suficientemente importantes.**

Este tema puede desarrollarse posteriormente utilizando una escena como la ciudad plegándose en *Inception* para introducir los efectos \(P-\Delta\).

---

## 7.3 No linealidad asociada a interacción o condiciones de frontera

Mencionar de manera breve ejemplos como:

- apertura y cierre;
- contacto;
- deslizamiento;
- elementos gap;
- apoyos unilaterales.

El objetivo no es profundizar todavía, sino mostrar que el término “no linealidad” incluye fenómenos distintos.

---

# 8. El primer modelo del curso: un sistema de un grado de libertad

Después de mostrar la complejidad del problema general, reducir deliberadamente el sistema.

Representar un oscilador de un grado de libertad:

- masa;
- resorte;
- amortiguador.

La diferencia respecto al modelo lineal tradicional es que ahora:

\[
F_s
=
f(u,\text{historia})
\]

El resorte puede tener inicialmente una constitutiva bilineal sencilla.

Mensaje pedagógico:

> **No necesitamos comenzar con un edificio completo. Si comprendemos completamente qué significa analizar un sistema no lineal de un grado de libertad, tendremos la base conceptual para entender posteriormente lo que hará un programa como OpenSees con una estructura de múltiples grados de libertad.**

Este modelo servirá posteriormente para introducir:

- pushover;
- historia de carga;
- histéresis;
- análisis incremental;
- iteraciones;
- criterios de convergencia;
- análisis dinámico no lineal.

---

# 9. Ejercicio conceptual: oscilador bilineal elastoplástico

Considerar:

\[
K_0 = 100\ \text{kN/mm}
\]

\[
F_y = 100\ \text{kN}
\]

y una rigidez postfluencia:

\[
\alpha=0
\]

es decir, un comportamiento perfectamente elastoplástico.

## Estado 1

Aplicar:

\[
F=50\ \text{kN}
\]

Entonces:

\[
u
=
\frac{F}{K_0}
=
0.5\ \text{mm}
\]

## Estado 2

Aplicar:

\[
F=100\ \text{kN}
\]

Entonces:

\[
u_y
=
1.0\ \text{mm}
\]

Hasta este punto, la respuesta todavía puede parecer similar a la intuición lineal.

## Estado 3

Imponer ahora:

\[
u=2\ \text{mm}
\]

Al haberse alcanzado la fluencia y ser \(\alpha=0\):

\[
F=100\ \text{kN}
\]

## Estado 4

Descargar hasta:

\[
F=0
\]

Plantear:

> **¿Regresa el desplazamiento a cero?**

La respuesta es no.

Aparece una deformación residual:

\[
u_r
\neq
0
\]

Mensaje clave:

> **Cero carga ya no significa cero deformación.**

Este ejercicio permite introducir de forma muy sencilla:

- plastificación;
- trayectoria;
- descarga;
- deformación residual;
- memoria del sistema.

---

# 10. Cierre de la primera clase

Retomar la frase inicial:

# La estructura tiene memoria

Presentar cuatro ideas fundamentales:

\[
\boxed{\text{Estado}}
\]

\[
\boxed{\text{Trayectoria}}
\]

\[
\boxed{\text{Incrementos}}
\]

\[
\boxed{\text{Equilibrio}}
\]

Cerrar con una idea como:

> Durante este curso aprenderemos a representar el estado de una estructura, hacerla avanzar a lo largo de una trayectoria, encontrar el equilibrio después de cada incremento y conservar la historia necesaria para determinar qué puede ocurrir después.

---

# 11. Del análisis estructural lineal al análisis no lineal

## Análisis lineal

\[
\mathbf{K}\mathbf{u}
=
\mathbf{P}
\]

## Análisis no lineal

\[
\mathbf{R}
\left(
\mathbf{u},
\text{estado interno}
\right)
=
\mathbf{P}
\]

La diferencia conceptual no consiste únicamente en reemplazar una recta por una curva.

El cambio fundamental es:

> **Pasamos de resolver estados independientes a seguir la evolución de un sistema.**

---

# 12. Material interactivo desarrollado: oscilador bilineal

Se desarrolló una primera herramienta interactiva para apoyar la explicación de la idea central de la clase:

> **La respuesta depende del camino recorrido.**

La aplicación representa un oscilador de un grado de libertad con una constitutiva bilineal y permite imponer una historia de deformaciones. La gráfica fuerza–deformación se actualiza con la trayectoria que sigue el sistema, no solamente con su envolvente monotónica.

## 12.1 Objetivo pedagógico

La herramienta busca que los estudiantes puedan comprobar visualmente que:

- conocer la deformación actual no siempre es suficiente para conocer la fuerza;
- la respuesta depende del estado interno producido por los pasos anteriores;
- después de la fluencia aparecen deformaciones plásticas;
- durante la descarga y la recarga, el sistema puede visitar una misma deformación con fuerzas diferentes;
- la envolvente constitutiva y la trayectoria efectivamente recorrida son conceptos distintos.

## 12.2 Modelo implementado

Se adoptó un modelo bilineal con endurecimiento cinemático. Sus parámetros editables son:

\[
K_0 = \text{rigidez inicial}
\]

\[
F_y = \text{fuerza de fluencia}
\]

\[
\alpha = \frac{K_p}{K_0}
\]

donde \(K_p\) es la pendiente post-fluencia. Por tanto:

\[
K_p = \alpha K_0
\]

y la deformación de fluencia es:

\[
u_y = \frac{F_y}{K_0}
\]

Cuando \(\alpha=0\), el comportamiento es elastoplástico perfecto. Para valores positivos de \(\alpha\), la fuerza continúa aumentando después de la fluencia con pendiente \(K_p\).

El endurecimiento cinemático permite representar descarga, inversión de la dirección de carga y ciclos histeréticos sencillos. Esta elección resulta útil para introducir la memoria del sistema antes de estudiar modelos constitutivos más complejos.

## 12.3 Interacciones disponibles

La aplicación permite:

- modificar \(K_0\), \(F_y\) y \(\alpha\);
- ingresar hasta 80 valores de deformación separados por comas, espacios o punto y coma;
- actualizar automáticamente la trayectoria fuerza–deformación;
- comparar la trayectoria recorrida con la envolvente bilineal;
- reproducir, pausar y reiniciar la historia;
- desplazarse manualmente entre los pasos mediante un control deslizante;
- consultar en cada paso la deformación, la fuerza y la deformación plástica;
- identificar si el incremento mostrado es elástico o plástico;
- cargar historias de ejemplo monótonas, cíclicas o diseñadas para mostrar memoria.

## 12.4 Historia inicial para demostrar memoria

La secuencia propuesta por defecto es:

\[
u = [0,\ 0.5,\ 1.0,\ 2.0,\ 1.0,\ 0,\ 0.5]\ \text{mm}
\]

con los parámetros iniciales:

\[
K_0=100\ \text{kN/mm},
\qquad
F_y=100\ \text{kN},
\qquad
\alpha=0.05
\]

La secuencia visita \(u=0.5\ \text{mm}\) antes y después de producir plastificación. Al comparar ambas visitas se observa que la fuerza no es la misma, a pesar de que la deformación total sí lo es.

Este resultado permite formular la pregunta central durante la clase:

> **Si la deformación actual es la misma, ¿qué información adicional necesitamos para determinar la fuerza?**

La respuesta conduce a las variables internas, la deformación plástica y la historia previa.

## 12.5 Estado actual de la aplicación

La herramienta se encuentra implementada y validada como una aplicación web adaptable a computadores, tabletas y teléfonos.

Versión publicada:

<https://oscilador-bilineal-no-lineal.iksak.chatgpt.site>

Carpeta local del proyecto:

```text
oscilador-bilineal/
```

Archivos principales:

```text
oscilador-bilineal/
├── app/
│   ├── page.tsx        # modelo, estado de la interfaz y gráfica
│   ├── globals.css     # diseño visual y adaptación responsive
│   └── layout.tsx      # metadatos generales
├── public/
│   └── og.png          # tarjeta de presentación del laboratorio
├── .openai/
│   └── hosting.json    # identificación del sitio publicado
├── package.json
└── package-lock.json
```

## 12.6 Traslado de la carpeta local

El proyecto es autocontenido y puede moverse completo a otra ubicación. Para conservar tanto la aplicación como su historial local, se debe trasladar la carpeta `oscilador-bilineal` completa, incluidos los directorios ocultos `.git` y `.openai`.

La carpeta `node_modules` puede trasladarse, pero no es indispensable. Si se omite, las dependencias pueden reconstruirse en la nueva ubicación ejecutando, dentro de la carpeta del proyecto:

```bash
npm install
```

Para abrir una versión local durante el desarrollo:

```bash
npm run dev
```

Para verificar que la aplicación puede compilarse para producción:

```bash
npm run build
```

Mover la carpeta local no cambia ni elimina la versión que ya se encuentra publicada.

---

# 13. Posible secuencia de las primeras clases

## Clase 1 — ¿Por qué necesitamos análisis no lineal?

Conceptos:

- estado;
- memoria;
- trayectoria;
- incrementalidad;
- equilibrio.

## Clase 2 — ¿Cómo representamos un material que tiene memoria?

Conceptos:

- envolvente;
- descarga;
- recarga;
- histéresis;
- oscilador no lineal de un grado de libertad.

## Clase 3 — ¿Cómo encontramos equilibrio cuando la rigidez cambia?

Conceptos:

- rigidez tangente;
- residuo;
- Newton-Raphson;
- iteraciones;
- criterios de convergencia.

## Clase 4 — ¿Cómo empujamos una estructura hasta el rango no lineal?

Conceptos:

- pushover;
- control de carga;
- control de desplazamiento;
- transición del sistema de un grado de libertad a sistemas de múltiples grados de libertad.

---

# Mensajes clave de la primera clase

1. **Una estructura no lineal tiene memoria.**
2. **El estado actual no puede describirse solamente por la carga actual.**
3. **El análisis no lineal construye una trayectoria, no únicamente una solución.**
4. **Cada incremento parte del estado convergido del incremento anterior.**
5. **El equilibrio debe verificarse y, normalmente, alcanzarse mediante iteraciones.**
6. **La no linealidad puede ser material, geométrica o asociada a interacción.**
7. **El oscilador de un grado de libertad será el laboratorio conceptual para introducir estos fenómenos antes de estudiar estructuras completas.**

---

# Frases que pueden servir como hilo narrativo

> **Una estructura no lineal tiene memoria.**

> **El análisis no lineal no consiste en encontrar un punto. Consiste en construir una trayectoria.**

> **En análisis no lineal, cada solución depende de la solución anterior.**

> **Un análisis no lineal no obtiene la respuesta de una vez. La persigue.**

> **Cero carga ya no significa cero deformación.**

> **Pasamos de resolver estados independientes a seguir la evolución de un sistema.**
