#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constructor limpio y seguro de 08_modelado_muros_mvlem.html
Lee el dataset numérico de mvlem_detailed_simulation.json y ensambla el
archivo HTML asegurando:
1. Ninguna corrupción de secuencias de escape de LaTeX (uso de r'''...''' y .replace()).
2. Diagrama SVG cinemático completo y detallado del macroelemento MVLEM en sección 2.
3. 4 lienzos interactivos con setupCanvas seguro contra dimensiones cero y DPIRatio.
4. Inicialización segura de variables JS (window.MVLEM_DATA, isInitialized flag).
5. Carga e inicialización robusta de KaTeX con observador/intervalo continuo.
"""
import os
import json

base_dir = "/Users/mac/Library/CloudStorage/OneDrive-Personal/3. Docencia/0. Cursos/18.Analisis_no_lineal"
json_path = os.path.join(base_dir, "Codigos_OpenSeesPy/mvlem_detailed_simulation.json")
html_path = os.path.join(base_dir, "08_modelado_muros_mvlem.html")

with open(json_path, 'r', encoding='utf-8') as f:
    sim_data = json.load(f)

json_str = json.dumps(sim_data)

# Plantilla puramente RAW para evitar escapes
template_raw = r'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Clase 08: Modelado No Lineal de Muros con Elementos MVLEM | Análisis No Lineal</title>
  <meta name="description" content="Laboratorio interactivo de análisis no lineal en OpenSeesPy: Modelado de muros de concreto reforzado mediante macroelementos MVLEM en un edificio de 16 pisos con muros acoplados.">

  <!-- KaTeX para renderizado de ecuaciones matemáticas (sin defer para disponibilidad inmediata) -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>

  <!-- Google Fonts: Inter y JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

  <style>
    /* ==========================================================================
       VARIABLES Y PALETA DE COLORES (MODO CLARO POR DEFECTO / OSCURO)
       TEMA CLASE 08: TEAL PROFUNDO (#0d6f73), CIAN SÍSMICO (#0284c7) Y ÁMBAR (#d97706)
       ========================================================================== */
    :root {
      --bg-base: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #f1f5f9;
      --bg-card-hover: #e2e8f0;
      --border-subtle: #cbd5e1;
      --border-accent: #0d6f73;
      --text-main: #0f172a;
      --text-muted: #334155;
      --text-faint: #64748b;

      --header-bg: rgba(255, 255, 255, 0.94);
      --hero-bg: linear-gradient(135deg, #ffffff 0%, #ecfdf5 40%, #f0fdfa 100%);
      --hero-title-gradient: linear-gradient(120deg, #0f172a 20%, #0d6f73 65%, #0284c7 100%);

      --teal-600: #0d6f73;
      --teal-500: #0f766e;
      --teal-400: #14b8a6;
      --teal-300: #2dd4bf;
      --cyan-500: #0284c7;
      --blue-500: #2563eb;
      --emerald-500: #059669;
      --amber-500: #d97706;
      --rose-500: #e11d48;
      --purple-500: #7c3aed;

      --canvas-bg: #ffffff;
      --canvas-grid: #e2e8f0;
      --canvas-axis: #64748b;
      --canvas-text: #1e293b;

      --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
      --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
      --shadow-glow: 0 0 20px rgba(13, 111, 115, 0.2);
    }

    body.dark-theme {
      --bg-base: #060b13;
      --bg-surface: #0b1320;
      --bg-card: #111d30;
      --bg-card-hover: #192a45;
      --border-subtle: #24354f;
      --border-accent: #2dd4bf;
      --text-main: #f1f5f9;
      --text-muted: #cbd5e1;
      --text-faint: #94a3b8;

      --header-bg: rgba(11, 19, 32, 0.94);
      --hero-bg: linear-gradient(135deg, #0b1320 0%, #082125 50%, #0c1c2e 100%);
      --hero-title-gradient: linear-gradient(120deg, #ffffff 20%, #2dd4bf 65%, #38bdf8 100%);

      --teal-600: #2dd4bf;
      --teal-500: #14b8a6;
      --teal-400: #2dd4bf;
      --teal-300: #5eead4;
      --cyan-500: #38bdf8;
      --blue-500: #60a5fa;
      --emerald-500: #34d399;
      --amber-500: #fbbf24;
      --rose-500: #fb7185;
      --purple-500: #a78bfa;

      --canvas-bg: #0d131f;
      --canvas-grid: #1e293b;
      --canvas-axis: #475569;
      --canvas-text: #94a3b8;

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.5);
      --shadow-glow: 0 0 25px rgba(45, 212, 191, 0.25);
    }

    /* ==========================================================================
       RESET Y ESTILOS BASE
       ========================================================================== */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.3s ease, color 0.3s ease;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* ==========================================================================
       HEADER Y NAVEGACIÓN SUPERIOR
       ========================================================================== */
    .top-header {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--header-bg);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    .header-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 0.75rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .btn-back {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      text-decoration: none;
      transition: all 0.2s ease;
    }

    .btn-back:hover {
      background: var(--bg-card-hover);
      color: var(--teal-600);
      border-color: var(--teal-600);
      transform: translateX(-2px);
    }

    .course-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      background: rgba(13, 111, 115, 0.12);
      color: var(--teal-600);
      border: 1px solid rgba(13, 111, 115, 0.25);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .theme-toggle {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.45rem 0.85rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s ease;
    }

    .theme-toggle:hover {
      background: var(--bg-card-hover);
      border-color: var(--teal-600);
    }

    /* ==========================================================================
       HERO PRINCIPAL
       ========================================================================== */
    .hero-section {
      background: var(--hero-bg);
      border-bottom: 1px solid var(--border-subtle);
      padding: 3rem 1.5rem 2.5rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }

    .hero-section::before {
      content: '';
      position: absolute;
      top: -50%;
      left: 50%;
      transform: translateX(-50%);
      width: 1000px;
      height: 600px;
      background: radial-gradient(circle, rgba(13, 111, 115, 0.12) 0%, rgba(2, 132, 199, 0.05) 50%, transparent 70%);
      pointer-events: none;
    }

    .hero-container {
      max-width: 1050px;
      margin: 0 auto;
      position: relative;
      z-index: 1;
    }

    .hero-tag {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.82rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 0.35rem 0.9rem;
      border-radius: 9999px;
      background: rgba(13, 111, 115, 0.12);
      color: var(--teal-600);
      border: 1px solid rgba(13, 111, 115, 0.28);
      margin-bottom: 1.25rem;
    }

    .hero-title {
      font-size: clamp(2rem, 4.2vw, 3.1rem);
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.18;
      background: var(--hero-title-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 1.25rem;
    }

    .hero-desc {
      font-size: clamp(1rem, 1.8vw, 1.18rem);
      color: var(--text-muted);
      max-width: 860px;
      margin: 0 auto 1.75rem;
      line-height: 1.65;
    }

    .hero-metadata-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      max-width: 900px;
      margin: 0 auto;
      text-align: left;
    }

    .meta-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 0.85rem 1.1rem;
      box-shadow: var(--shadow-sm);
    }

    .meta-label {
      font-size: 0.72rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.06em;
      color: var(--text-faint);
      margin-bottom: 0.25rem;
    }

    .meta-value {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
    }

    /* ==========================================================================
       CONTENEDOR PRINCIPAL
       ========================================================================== */
    .main-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
      width: 100%;
      flex: 1;
    }

    /* ==========================================================================
       PANEL DE CONTROL PRINCIPAL Y ESTADOS DE PUSHOVER
       ========================================================================== */
    .control-panel {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 1.5rem;
      margin-bottom: 2rem;
      box-shadow: var(--shadow-md);
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .panel-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .controls-row {
      display: flex;
      align-items: center;
      gap: 1.25rem;
      flex-wrap: wrap;
      margin-bottom: 1.25rem;
    }

    .btn-group {
      display: inline-flex;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 0.25rem;
      gap: 0.25rem;
    }

    .btn-ctrl {
      background: transparent;
      border: none;
      color: var(--text-main);
      padding: 0.45rem 0.85rem;
      border-radius: 7px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
    }

    .btn-ctrl:hover {
      background: var(--bg-card-hover);
      color: var(--teal-600);
    }

    .btn-ctrl.active {
      background: var(--teal-600);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(13, 111, 115, 0.35);
    }

    .btn-primary {
      background: var(--teal-600);
      color: #ffffff;
    }

    .btn-primary:hover {
      background: var(--teal-500);
      color: #ffffff;
    }

    .slider-container {
      flex: 1;
      min-width: 280px;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }

    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
    }

    .range-slider {
      -webkit-appearance: none;
      appearance: none;
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: var(--border-subtle);
      outline: none;
      transition: background 0.2s;
      cursor: pointer;
    }

    .range-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: var(--teal-600);
      cursor: pointer;
      border: 3px solid #ffffff;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
      transition: transform 0.15s ease, background 0.2s;
    }

    .range-slider::-webkit-slider-thumb:hover {
      transform: scale(1.15);
      background: var(--teal-500);
    }

    /* Puntos clave / Presets de análisis */
    .presets-row {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-top: 0.75rem;
      padding-top: 0.75rem;
      border-top: 1px dashed var(--border-subtle);
    }

    .preset-label {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-faint);
      margin-right: 0.25rem;
    }

    .btn-preset {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .btn-preset:hover {
      border-color: var(--teal-600);
      color: var(--teal-600);
      background: var(--bg-card-hover);
    }

    .btn-preset.active {
      background: rgba(13, 111, 115, 0.15);
      border-color: var(--teal-600);
      color: var(--teal-600);
      font-weight: 700;
    }

    /* ==========================================================================
       MÉTRICAS KPI EN TIEMPO REAL
       ========================================================================== */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1rem 1.15rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }

    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--teal-600);
      opacity: 0.8;
    }

    .kpi-card.kpi-cyan::before { background: var(--cyan-500); }
    .kpi-card.kpi-amber::before { background: var(--amber-500); }
    .kpi-card.kpi-purple::before { background: var(--purple-500); }
    .kpi-card.kpi-emerald::before { background: var(--emerald-500); }

    .kpi-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-faint);
      margin-bottom: 0.35rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .kpi-value {
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--text-main);
      font-family: var(--font-mono);
      line-height: 1.1;
      margin-bottom: 0.3rem;
    }

    .kpi-sub {
      font-size: 0.76rem;
      color: var(--text-muted);
    }

    /* ==========================================================================
       CANVAS Y VISUALIZADORES 2D
       ========================================================================== */
    .canvas-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    @media (max-width: 1024px) {
      .canvas-grid {
        grid-template-columns: 1fr;
      }
    }

    .canvas-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 1.25rem;
      box-shadow: var(--shadow-md);
      display: flex;
      flex-direction: column;
    }

    .canvas-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.85rem;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .canvas-title {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .canvas-toolbar {
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .btn-tab {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 0.25rem 0.55rem;
      border-radius: 6px;
      font-size: 0.74rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .btn-tab.active, .btn-tab:hover {
      background: rgba(13, 111, 115, 0.12);
      border-color: var(--teal-600);
      color: var(--teal-600);
    }

    .canvas-wrapper {
      position: relative;
      width: 100%;
      height: 380px;
      background: var(--canvas-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
    }

    canvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .canvas-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-top: 0.75rem;
      font-size: 0.75rem;
      color: var(--text-muted);
      justify-content: center;
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }

    .legend-swatch {
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }

    /* ==========================================================================
       DIAGRAMA CONCEPTUAL SVG DEL ELEMENTO MVLEM
       ========================================================================== */
    .element-diagram-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 1.5rem;
      margin: 1.5rem 0 2rem;
      box-shadow: var(--shadow-sm);
    }

    /* ==========================================================================
       SECCIÓN DE TEORÍA Y ECUACIONES MATEMÁTICAS
       ========================================================================== */
    .theory-section {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 2rem;
      margin-bottom: 2rem;
      box-shadow: var(--shadow-md);
    }

    .theory-title {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 1.25rem;
      padding-bottom: 0.75rem;
      border-bottom: 2px solid var(--teal-600);
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .theory-subtitle {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin: 1.5rem 0 0.75rem;
    }

    .theory-p {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.7;
      margin-bottom: 1rem;
    }

    .math-box {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--teal-600);
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin: 1.25rem 0;
      overflow-x: auto;
      font-size: 1.05rem;
    }

    .compare-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.25rem 0;
      font-size: 0.88rem;
    }

    .compare-table th, .compare-table td {
      padding: 0.75rem 1rem;
      border: 1px solid var(--border-subtle);
      text-align: left;
    }

    .compare-table th {
      background: var(--bg-card);
      color: var(--text-main);
      font-weight: 700;
    }

    /* ==========================================================================
       PANEL DE CÓDIGO OPENSEESPY
       ========================================================================== */
    .code-panel {
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 12px;
      overflow: hidden;
      margin: 1.5rem 0;
    }

    .code-header {
      background: #161b22;
      padding: 0.6rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #30363d;
    }

    .code-tabs {
      display: flex;
      gap: 0.5rem;
    }

    .code-tab {
      background: transparent;
      border: 1px solid transparent;
      color: #8b949e;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.15s ease;
    }

    .code-tab.active, .code-tab:hover {
      background: #21262d;
      color: #58a6ff;
      border-color: #30363d;
    }

    .code-content {
      padding: 1.25rem;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.6;
      color: #c9d1d9;
      overflow-x: auto;
      max-height: 480px;
    }

    /* ==========================================================================
       QUIZ SOCRÁTICO
       ========================================================================== */
    .quiz-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1.25rem;
    }

    .quiz-question {
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 0.85rem;
      font-size: 0.95rem;
    }

    .quiz-options {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .quiz-option {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 0.65rem 1rem;
      color: var(--text-main);
      font-size: 0.88rem;
      text-align: left;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .quiz-option:hover {
      background: var(--bg-card-hover);
      border-color: var(--teal-600);
    }

    .quiz-option.correct {
      background: rgba(5, 150, 105, 0.15);
      border-color: #059669;
      color: #059669;
      font-weight: 700;
    }

    .quiz-option.incorrect {
      background: rgba(225, 29, 72, 0.15);
      border-color: #e11d48;
      color: #e11d48;
      font-weight: 700;
    }

    .quiz-feedback {
      margin-top: 0.75rem;
      padding: 0.65rem 0.9rem;
      border-radius: 6px;
      font-size: 0.84rem;
      line-height: 1.5;
      display: none;
    }
  </style>
</head>
<body>

  <!-- HEADER NAVEGACIÓN -->
  <header class="top-header">
    <div class="header-container">
      <div class="header-left">
        <a href="index.html#muros-section" class="btn-back">
          <span>&larr;</span>
          <span>Volver al Portal del Curso</span>
        </a>
        <span class="course-badge">Clase 08 • Macroelementos MVLEM</span>
      </div>

      <div class="header-right">
        <button class="theme-toggle" id="theme-toggle-btn" title="Alternar Modo Claro / Oscuro">
          <span id="theme-icon">🌙</span>
          <span id="theme-label">Tema</span>
        </button>
      </div>
    </div>
  </header>

  <!-- HERO PRINCIPAL -->
  <section class="hero-section">
    <div class="hero-container">
      <div class="hero-tag">Laboratorio Numérico Interactivo • OpenSeesPy</div>
      <h1 class="hero-title">Modelado No Lineal de Muros Estructurales con Elementos MVLEM</h1>
      <p class="hero-desc">
        Formulación cinemática de sección plana de Vulcano, Bertero & Colotti (1988) y Orakcal & Wallace (2006). Simulación de la respuesta acoplada flexión-corte en el <strong>edificio arquetipo de 16 pisos de Ramos & Hube (2021, <em>Engineering Structures</em>)</strong> mediante macrofibras de concreto y acero y resorte central de cortante.
      </p>

      <div class="hero-metadata-grid">
        <div class="meta-card">
          <div class="meta-label">Arquetipo Estructural</div>
          <div class="meta-value">Edificio 16 Pisos (Ramos & Hube, 2021)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">Altura Total / Entrepiso</div>
          <div class="meta-value">41.6 m (h = 2.6 m)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">Configuración Resistente</div>
          <div class="meta-value">2 Muros Acoplados (Lw = 7.65 m)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">Discretización Seccional</div>
          <div class="meta-value">8 Macrofibras + Resorte Cortante c=0.4</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTENEDOR PRINCIPAL INTERACTIVO -->
  <main class="main-container">

    <!-- PANEL DE CONTROL PUSHOVER -->
    <section class="control-panel">
      <div class="panel-header">
        <div class="panel-title">
          <span>🕹️</span>
          <span>Control de Carga Lateral y Estado Deformado</span>
        </div>
        <div class="btn-group">
          <button class="btn-ctrl" id="btn-play">▶️ Reproducir</button>
          <button class="btn-ctrl" id="btn-prev">&larr; Anterior</button>
          <button class="btn-ctrl" id="btn-next">Siguiente &rarr;</button>
          <button class="btn-ctrl" id="btn-reset">⏮️ Reiniciar</button>
        </div>
      </div>

      <div class="controls-row">
        <div class="slider-container">
          <div class="slider-header">
            <span>Paso de Desplazamiento de Techo (\(\Delta_{\text{roof}}\)):</span>
            <span id="step-display" style="font-family: var(--font-mono); font-weight: 700; color: var(--teal-600);">0 / 52</span>
          </div>
          <input type="range" min="0" max="52" value="0" step="1" class="range-slider" id="pushover-slider">
          <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-faint); margin-top: 0.25rem;">
            <span>0.00 m (0.0% Drift)</span>
            <span id="disp-display" style="font-weight: 700; color: var(--teal-600);">0.0000 m</span>
            <span id="drift-display" style="font-weight: 700; color: var(--cyan-500);">0.000 % Drift</span>
            <span>0.624 m (1.5% Drift)</span>
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);">Velocidad:</span>
          <select id="speed-select" style="background: var(--bg-card); color: var(--text-main); border: 1px solid var(--border-subtle); padding: 0.35rem 0.6rem; border-radius: 6px; font-size: 0.82rem; font-weight: 600; outline: none;">
            <option value="0.5">0.5x</option>
            <option value="1" selected>1.0x (Normal)</option>
            <option value="2">2.0x (Rápido)</option>
            <option value="4">4.0x (Máximo)</option>
          </select>
        </div>
      </div>

      <!-- Presets / Hitos Físicos de Daño -->
      <div class="presets-row">
        <span class="preset-label">Saltar a Hito Crítico:</span>
        <button class="btn-preset active" data-step="0">0. Estado Elástico (0.0% Drift)</button>
        <button class="btn-preset" data-step="6">1. Primera Fluencia Acero Tracción (~0.17% Drift)</button>
        <button class="btn-preset" data-step="15">2. Resistencia Máxima Vb,max (~0.43% Drift)</button>
        <button class="btn-preset" data-step="24">3. Inicio de Aplastamiento Concreto (~0.72% Drift)</button>
        <button class="btn-preset" data-step="35">4. Límite de Diseño NSR-10 (1.0% Drift)</button>
        <button class="btn-preset" data-step="52">5. Demanda Extrema Inelástica (1.5% Drift)</button>
      </div>
    </section>

    <!-- KPIS EN TIEMPO REAL -->
    <section class="kpi-grid">
      <div class="kpi-card kpi-cyan">
        <div class="kpi-title">
          <span>Deriva de Techo (\(\theta_{\text{roof}}\))</span>
          <span>📐</span>
        </div>
        <div class="kpi-value" id="kpi-drift">0.000 %</div>
        <div class="kpi-sub" id="kpi-disp">Desplazamiento: 0.000 m</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Cortante Basal Total (\(V_{\text{base}}\))</span>
          <span>⚡</span>
        </div>
        <div class="kpi-value" id="kpi-shear">0.0 kN</div>
        <div class="kpi-sub">Suma muros M1 + M2</div>
      </div>

      <div class="kpi-card kpi-emerald">
        <div class="kpi-title">
          <span>Coeficiente Sísmico (\(V/W\))</span>
          <span>🏢</span>
        </div>
        <div class="kpi-value" id="kpi-vw">0.000</div>
        <div class="kpi-sub">Peso Sísmico W = 25,520 kN</div>
      </div>

      <div class="kpi-card kpi-purple">
        <div class="kpi-title">
          <span>Aporte del Acople (\(T \cdot L\))</span>
          <span>⚖️</span>
        </div>
        <div class="kpi-value" id="kpi-couple">0.0 %</div>
        <div class="kpi-sub">Fracción del Volcamiento Total</div>
      </div>

      <div class="kpi-card kpi-amber">
        <div class="kpi-title">
          <span>Mecanismo Inelástico</span>
          <span>🔍</span>
        </div>
        <div class="kpi-value" id="kpi-state" style="font-size: 1.15rem; font-family: var(--font-sans);">Elástico Lineal</div>
        <div class="kpi-sub" id="kpi-state-desc">Sin daño ni plastificación</div>
      </div>
    </section>

    <!-- GRID DE VISUALIZADORES CANVASES 2D -->
    <div class="canvas-grid">

      <!-- LIENZO A: ELEVACIÓN DEL EDIFICIO DE 16 PISOS -->
      <div class="canvas-card">
        <div class="canvas-header">
          <div class="canvas-title">
            <span>🏢</span>
            <span>Elevación del Edificio y Deformada Lateral</span>
          </div>
          <div class="canvas-toolbar">
            <button class="btn-tab" id="btn-scale-toggle">Escala: 15x</button>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="canvas-building"></canvas>
        </div>
        <div class="canvas-legend">
          <div class="legend-item"><span class="legend-swatch" style="background: #0284c7;"></span> Muro 1 (Barlovento / Tracción)</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #0d6f73;"></span> Muro 2 (Sotavento / Compresión)</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #10b981;"></span> Vigas de Acople</div>
        </div>
      </div>

      <!-- LIENZO B: CURVA DE CAPACIDAD PUSHOVER -->
      <div class="canvas-card">
        <div class="canvas-header">
          <div class="canvas-title">
            <span>📈</span>
            <span>Curva de Capacidad Pushover Global</span>
          </div>
          <div class="canvas-toolbar">
            <button class="btn-tab active" id="btn-curve-vw">V/W vs % Drift</button>
            <button class="btn-tab" id="btn-curve-dim">V (kN) vs D (m)</button>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="canvas-pushover"></canvas>
        </div>
        <div class="canvas-legend">
          <div class="legend-item"><span class="legend-swatch" style="background: #0d6f73;"></span> Curva Pushover MVLEM</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #e11d48;"></span> Estado Actual</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #f59e0b;"></span> Puntos Críticos de Fluencia y Máximo</div>
        </div>
      </div>

      <!-- LIENZO C: PERFIL SECCIONAL DE DEFORMACIONES DE LAS 8 MACROFIBRAS -->
      <div class="canvas-card">
        <div class="canvas-header">
          <div class="canvas-title">
            <span>🔬</span>
            <span>Perfil Seccional \(\epsilon_k(x)\) en Macrofibras (Base Piso 1)</span>
          </div>
          <div class="canvas-toolbar">
            <button class="btn-tab active" id="btn-wall-select">Muro 1 (Tracción Neta)</button>
            <button class="btn-tab" id="btn-wall-select2">Muro 2 (Compresión Neta)</button>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="canvas-fibers"></canvas>
        </div>
        <div class="canvas-legend">
          <div class="legend-item"><span class="legend-swatch" style="background: #0284c7;"></span> Compresión (\(\epsilon < 0\))</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #f59e0b;"></span> Tracción Elástica (\(0 < \epsilon \le \epsilon_y\))</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #e11d48;"></span> Fluencia Acero (\(\epsilon > \epsilon_y\))</div>
        </div>
      </div>

      <!-- LIENZO D: DERIVAS DE ENTREPISO Y DESCOMPOSICIÓN DE MOMENTOS -->
      <div class="canvas-card">
        <div class="canvas-header">
          <div class="canvas-title">
            <span id="title-canvas-d">📊 Perfil de Deriva de Entrepiso en la Altura</span>
          </div>
          <div class="canvas-toolbar">
            <button class="btn-tab active" id="btn-view-drift">Derivas de Entrepiso</button>
            <button class="btn-tab" id="btn-view-moments">Volcamiento (M_OTM)</button>
          </div>
        </div>
        <div class="canvas-wrapper">
          <canvas id="canvas-drift"></canvas>
        </div>
        <div class="canvas-legend" id="legend-canvas-d">
          <div class="legend-item"><span class="legend-swatch" style="background: #0d6f73;"></span> Deriva Entrepiso \(\Delta_i / h_i\) (%)</div>
          <div class="legend-item"><span class="legend-swatch" style="background: #e11d48;"></span> Límite NSR-10 (1.0%)</div>
        </div>
      </div>

    </div>

    <!-- SECCIÓN DE TEORÍA Y FORMULACIÓN MATEMÁTICA -->
    <section class="theory-section">
      <h2 class="theory-title">📐 Fundamentación Teórica del Macroelemento MVLEM</h2>

      <p class="theory-p">
        El <strong>Multiple-Vertical-Line-Element Model (MVLEM)</strong>, formulado originalmente por <strong>Vulcano, Bertero & Colotti (1988)</strong> y perfeccionado por <strong>Orakcal, Massone & Wallace (2004, 2006)</strong>, es el macroelemento estándar para capturar la respuesta inelástica de muros de concreto armado gobernados por flexión o con interacción flexión-corte moderada.
      </p>

      <!-- DIAGRAMA CONCEPTUAL SVG DEL MACROELEMENTO MVLEM -->
      <div class="element-diagram-card">
        <div style="font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span>📐</span>
            <span>Esquema Cinemático y Grados de Libertad del Macroelemento MVLEM (2 Nodos, \(m\) Fibras, Resorte Cortante)</span>
          </div>
          <span style="font-size: 0.76rem; color: var(--teal-600); font-weight: 600;">Orakcal & Wallace (2006)</span>
        </div>

        <svg viewBox="0 0 760 400" width="100%" height="auto" style="max-height: 400px; display: block; margin: 0 auto; background: var(--canvas-bg); border-radius: 8px; border: 1px solid var(--border-subtle);" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
            </marker>
            <marker id="arrow-teal" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#0d6f73" />
            </marker>
            <marker id="arrow-amber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706" />
            </marker>
            <linearGradient id="beamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#0284c7" stop-opacity="0.3"/>
              <stop offset="50%" stop-color="#0d6f73" stop-opacity="0.5"/>
              <stop offset="100%" stop-color="#0284c7" stop-opacity="0.3"/>
            </linearGradient>
            <pattern id="hatchRebar" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
              <line x1="0" y1="0" x2="0" y2="8" stroke="#e11d48" stroke-width="1.5" />
            </pattern>
          </defs>

          <!-- Viga rígida superior (Piso j) -->
          <rect x="120" y="45" width="520" height="24" rx="4" fill="url(#beamGrad)" stroke="#0d6f73" stroke-width="2"/>
          <text x="380" y="38" text-anchor="middle" fill="var(--text-muted)" font-size="12" font-weight="700">Viga Rígida Superior (Restricción de Diafragma - Nivel j)</text>

          <!-- Viga rígida inferior (Piso i) -->
          <rect x="120" y="335" width="520" height="24" rx="4" fill="url(#beamGrad)" stroke="#0d6f73" stroke-width="2"/>
          <text x="380" y="375" text-anchor="middle" fill="var(--text-muted)" font-size="12" font-weight="700">Viga Rígida Inferior (Nivel i)</text>

          <!-- Nodos Externos i y j -->
          <circle cx="380" cy="57" r="7" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
          <text x="395" y="62" fill="#0284c7" font-size="13" font-weight="800">Nodo j</text>

          <circle cx="380" cy="347" r="7" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
          <text x="395" y="352" fill="#0284c7" font-size="13" font-weight="800">Nodo i</text>

          <!-- Grados de libertad en Nodo j: [uj, vj, thetaj] -->
          <line x1="380" y1="57" x2="430" y2="57" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
          <text x="435" y="54" fill="#0284c7" font-size="11" font-weight="700">u_j</text>

          <line x1="380" y1="57" x2="380" y2="15" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
          <text x="386" y="20" fill="#0284c7" font-size="11" font-weight="700">v_j</text>

          <path d="M 360 45 A 25 25 0 0 1 398 35" fill="none" stroke="#0284c7" stroke-width="2" marker-end="url(#arrow-blue)"/>
          <text x="345" y="38" fill="#0284c7" font-size="11" font-weight="700">\theta_j</text>

          <!-- Grados de libertad en Nodo i: [ui, vi, thetai] -->
          <line x1="380" y1="347" x2="430" y2="347" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
          <text x="435" y="344" fill="#0284c7" font-size="11" font-weight="700">u_i</text>

          <line x1="380" y1="347" x2="380" y2="305" stroke="#0284c7" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
          <text x="386" y="315" fill="#0284c7" font-size="11" font-weight="700">v_i</text>

          <!-- Macrofibras (8 macroelementos uniaxiales) -->
          <!-- Bulbo Izquierdo (Fibra 1: Confinado) -->
          <rect x="135" y="69" width="30" height="266" fill="url(#hatchRebar)" opacity="0.3" stroke="#e11d48" stroke-dasharray="3,3"/>
          <line x1="150" y1="69" x2="150" y2="180" stroke="#e11d48" stroke-width="2"/>
          <!-- Resorte axial Fibra 1 -->
          <path d="M 150 180 L 144 186 L 156 194 L 144 202 L 156 210 L 150 216 L 150 335" fill="none" stroke="#e11d48" stroke-width="2"/>
          <text x="150" y="235" text-anchor="middle" fill="#e11d48" font-size="10" font-weight="700">Fibra 1</text>
          <text x="150" y="247" text-anchor="middle" fill="var(--text-faint)" font-size="8">Borde Confinado</text>

          <!-- Fibras del alma (2 a 7) -->
          <!-- Fibra 2 -->
          <line x1="210" y1="69" x2="210" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 210 185 L 206 190 L 214 196 L 206 202 L 214 208 L 210 213 L 210 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="210" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=2</text>

          <!-- Fibra 3 -->
          <line x1="265" y1="69" x2="265" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 265 185 L 261 190 L 269 196 L 261 202 L 269 208 L 265 213 L 265 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="265" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=3</text>

          <!-- Fibra 4 -->
          <line x1="320" y1="69" x2="320" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 320 185 L 316 190 L 324 196 L 316 202 L 324 208 L 320 213 L 320 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="320" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=4</text>

          <!-- Eje Centroidal del Muro (x=0) -->
          <line x1="380" y1="69" x2="380" y2="335" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4,4"/>

          <!-- Fibra 5 -->
          <line x1="440" y1="69" x2="440" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 440 185 L 436 190 L 444 196 L 436 202 L 444 208 L 440 213 L 440 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="440" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=5</text>

          <!-- Fibra 6 -->
          <line x1="495" y1="69" x2="495" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 495 185 L 491 190 L 499 196 L 491 202 L 499 208 L 495 213 L 495 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="495" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=6</text>

          <!-- Fibra 7 -->
          <line x1="550" y1="69" x2="550" y2="185" stroke="#0d6f73" stroke-width="1.5"/>
          <path d="M 550 185 L 546 190 L 554 196 L 546 202 L 554 208 L 550 213 L 550 335" fill="none" stroke="#0d6f73" stroke-width="1.5"/>
          <text x="550" y="235" text-anchor="middle" fill="var(--text-muted)" font-size="9">k=7</text>

          <!-- Bulbo Derecho (Fibra 8: Confinado) -->
          <rect x="595" y="69" width="30" height="266" fill="url(#hatchRebar)" opacity="0.3" stroke="#e11d48" stroke-dasharray="3,3"/>
          <line x1="610" y1="69" x2="610" y2="180" stroke="#e11d48" stroke-width="2"/>
          <path d="M 610 180 L 604 186 L 616 194 L 604 202 L 616 210 L 610 216 L 610 335" fill="none" stroke="#e11d48" stroke-width="2"/>
          <text x="610" y="235" text-anchor="middle" fill="#e11d48" font-size="10" font-weight="700">Fibra 8</text>
          <text x="610" y="247" text-anchor="middle" fill="var(--text-faint)" font-size="8">Borde Confinado</text>

          <!-- Resorte Central de Cortante a altura c*h (c = 0.40 -> y = 335 - 0.4*266 = 228.6) -->
          <circle cx="380" cy="228" r="5" fill="#d97706"/>
          <!-- Enlace rígido desde el nodo inferior al resorte de corte -->
          <line x1="380" y1="335" x2="380" y2="228" stroke="#d97706" stroke-width="2.5"/>
          <!-- Resorte horizontal de corte -->
          <path d="M 330 228 L 340 222 L 350 234 L 360 222 L 370 234 L 380 228 L 390 222 L 400 234 L 410 222 L 420 234 L 430 228" fill="none" stroke="#d97706" stroke-width="2.5"/>
          <line x1="430" y1="228" x2="455" y2="228" stroke="#d97706" stroke-width="2" marker-end="url(#arrow-amber)"/>
          <text x="460" y="232" fill="#d97706" font-size="11" font-weight="800">Resorte Cortante K_h</text>
          <text x="460" y="246" fill="var(--text-faint)" font-size="9">a altura c·h (c = 0.40)</text>

          <!-- Cotas de Altura (h) y c·h -->
          <line x1="70" y1="69" x2="70" y2="335" stroke="var(--text-faint)" stroke-width="1.5"/>
          <line x1="62" y1="69" x2="78" y2="69" stroke="var(--text-faint)" stroke-width="1.5"/>
          <line x1="62" y1="335" x2="78" y2="335" stroke="var(--text-faint)" stroke-width="1.5"/>
          <text x="52" y="205" text-anchor="middle" fill="var(--text-main)" font-size="12" font-weight="700">h = 2.6 m</text>

          <line x1="95" y1="228" x2="95" y2="335" stroke="#d97706" stroke-width="1.5"/>
          <line x1="88" y1="228" x2="102" y2="228" stroke="#d97706" stroke-width="1.5"/>
          <line x1="88" y1="335" x2="102" y2="335" stroke="#d97706" stroke-width="1.5"/>
          <text x="108" y="285" fill="#d97706" font-size="10" font-weight="700">c·h</text>

          <!-- Cotas de Ancho (Lw) y Coordenada x_k -->
          <line x1="135" y1="385" x2="625" y2="385" stroke="var(--text-faint)" stroke-width="1.5"/>
          <line x1="135" y1="380" x2="135" y2="390" stroke="var(--text-faint)" stroke-width="1.5"/>
          <line x1="625" y1="380" x2="625" y2="390" stroke="var(--text-faint)" stroke-width="1.5"/>
          <text x="380" y="398" text-anchor="middle" fill="var(--text-main)" font-size="11" font-weight="700">Longitud del Muro L_w = 7.65 m</text>
        </svg>
      </div>

      <!-- CAJA DE REFERENCIA BIBLIOGRÁFICA DEL EDIFICIO ARQUETIPO -->
      <div style="background: rgba(2, 132, 199, 0.08); border: 1px solid rgba(2, 132, 199, 0.25); border-left: 4px solid var(--cyan-500); border-radius: 10px; padding: 1.1rem 1.35rem; margin: 1.5rem 0 1.75rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 700; color: var(--cyan-500); font-size: 0.95rem; margin-bottom: 0.45rem;">
          <span>📚</span>
          <span>Edificio Arquetipo y Referencia Bibliográfica del Modelo</span>
        </div>
        <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 0.6rem;">
          La geometría, propiedades seccionales y distribución de masas de este laboratorio interactivo corresponden al edificio arquetipo de 16 pisos con muros de concreto armado acoplados mediante losas/vigas no lineales investigado por <strong>Ramos y Hube (2021)</strong> en <em>Engineering Structures</em>:
        </p>
        <blockquote style="font-size: 0.85rem; font-family: var(--font-mono); background: var(--bg-surface); padding: 0.75rem 1rem; border-radius: 6px; border: 1px solid var(--border-subtle); color: var(--text-main); line-height: 1.5;">
          <strong>Ramos, L., & Hube, M. A. (2021).</strong> <em>Seismic response of reinforced concrete wall buildings with nonlinear coupling slabs.</em> <strong>Engineering Structures</strong>, 234, 111888. <a href="https://doi.org/10.1016/j.engstruct.2021.111888" target="_blank" rel="noopener" style="color: var(--cyan-500); text-decoration: underline; word-break: break-all;">https://doi.org/10.1016/j.engstruct.2021.111888</a>
        </blockquote>
        <p style="font-size: 0.83rem; color: var(--text-faint); margin-top: 0.55rem; line-height: 1.5;">
          <strong>Parámetros del Arquetipo:</strong> 16 pisos (\(H = 41.6\text{ m}\), \(h = 2.6\text{ m}\)), peso sísmico reactivo \(W = 25\,520\text{ kN}\), dos muros con bulbos de borde (\(L_w = 7.65\text{ m}\), espesor de alma \(t_w = 0.30\text{ m}\), bulbos de \(7.50\text{ m}\)) separados centro a centro a \(L_{\text{arm}} = 9.15\text{ m}\) y acoplados mediante elementos de losa/viga de enlace de luz libre \(L_n = 1.50\text{ m}\).
        </p>
      </div>

      <h3 class="theory-subtitle">1. Comparación con Otros Modelos Numéricos de Muros</h3>
      <table class="compare-table">
        <thead>
          <tr>
            <th>Formulación</th>
            <th>Ventajas</th>
            <th>Limitaciones Críticas en Muros</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Elemento Viga de Fibras (Beam-Column)</strong></td>
            <td>Rápido, un solo eje centroidal, fácil conectividad.</td>
            <td>Asume que las secciones planas permanecen planas en todo el elemento; subestima el pandeo de borde, no captura la migración biaxial del eje neutro en muros anchos y desacopla arbitrariamente el cortante mediante un resorte elástico simple.</td>
          </tr>
          <tr>
            <td><strong>Láminas Multicapa (Multilayer Shell MITC4 / DKGQ)</strong></td>
            <td>Captura esfuerzos biaxiales microscópicos en concreto y acero mediante la teoría de campo de compresión modificada (MCFT).</td>
            <td>Demanda computacional enorme (cientos de miles de GDL), problemas severos de convergencia en análisis dinámico paso a paso y complejidad extrema de calibración.</td>
          </tr>
          <tr>
            <td><strong>Macroelemento MVLEM (Orakcal & Wallace)</strong></td>
            <td><strong>Equilibrio óptimo:</strong> Discretiza el muro en macrofibras axiales y un resorte de corte central a \(c \cdot h\). Captura fluencia, agrietamiento, descascaramiento y migración del eje neutro sin sobrecosto numérico.</td>
            <td>En su versión básica, la respuesta a cortante se desacopla de la respuesta a flexión (resuelto posteriormente en la extensión SFI-MVLEM de Kolozvari et al., 2015).</td>
          </tr>
        </tbody>
      </table>

      <h3 class="theory-subtitle">2. Cinemática y Grados de Libertad del Elemento</h3>
      <p class="theory-p">
        El macroelemento MVLEM bidimensional se define entre dos nodos externos \(i\) (nodo inferior) y \(j\) (nodo superior), cada uno con 3 grados de libertad globales: \([u_i, v_i, \theta_i]\) y \([u_j, v_j, \theta_j]\). Los nodos se conectan a vigas infinitamente rígidas en las caras superior e inferior para modelar la restricción del diafragma de piso.
      </p>

      <div class="math-box">
        $$\mathbf{u}_e = [u_i, v_i, \theta_i, u_j, v_j, \theta_j]^T \in \mathbb{R}^6$$
        $$\Delta_{v,k} = (v_j - v_i) - x_k (\theta_j - \theta_i)$$
        $$\epsilon_k = \frac{\Delta_{v,k}}{h} = \frac{(v_j - v_i) - x_k (\theta_j - \theta_i)}{h}$$
      </div>

      <p class="theory-p">
        donde \(h\) es la altura del entrepiso (\(h = 2.6\text{ m}\) en nuestro edificio), \(x_k\) es la coordenada horizontal de la macrofibra \(k\) medida desde el centroide del muro, \(\Delta_{v,k}\) es el alargamiento axial de la macrofibra, y \(\epsilon_k\) es su deformación unitaria uniaxial.
      </p>

      <h3 class="theory-subtitle">3. Resorte Horizontal de Cortante</h3>
      <p class="theory-p">
        La respuesta a cortante se concentra en un resorte horizontal ubicado a una altura relativa \(c \cdot h\) medida desde el nodo inferior \(i\). Típicamente se adopta \(c = 0.40\), que coincide con la posición media del punto de inflexión en muros dominados por flexión. El desplazamiento relativo horizontal en el resorte es:
      </p>

      <div class="math-box">
        $$\Delta_h = (u_j - u_i) - h(1-c)\theta_i - hc\theta_j$$
        $$\gamma = \frac{\Delta_h}{h}$$
        $$V = K_h \cdot \Delta_h = \left( \frac{G \cdot A_v}{h} \right) \Delta_h$$
      </div>

      <h3 class="theory-subtitle">4. Determinación de Esfuerzos y Fuerzas de Sección</h3>
      <p class="theory-p">
        Para cada una de las \(m = 8\) macrofibras, el esfuerzo se obtiene evaluando las leyes constitutivas uniaxiales del concreto y del acero:
      </p>

      <div class="math-box">
        $$F_k = A_{c,k} \cdot \sigma_{c,k}(\epsilon_k) + A_{s,k} \cdot \sigma_{s,k}(\epsilon_k) = b_k t_k \left[ (1 - \rho_k)\sigma_{c,k}(\epsilon_k) + \rho_k \sigma_{s,k}(\epsilon_k) \right]$$
        $$N = \sum_{k=1}^{m} F_k, \qquad M = \sum_{k=1}^{m} (-x_k F_k) + V \cdot (c \cdot h)$$
      </div>

      <h3 class="theory-subtitle">5. La Mecánica del Acople: Descomposición del Momento de Volcamiento (\(M_{\text{OTM}}\))</h3>
      <p class="theory-p">
        En un sistema de dos muros acoplados mediante vigas o losas de enlace, el momento de volcamiento total en la base no es simplemente la suma de los momentos flectores basales de cada muro individual. Las losas y vigas de enlace desarrollan grandes fuerzas de cortante vertical \(V_{\text{viga}, j}\) que se acumulan en la altura:
      </p>

      <div class="math-box">
        $$T = \sum_{j=1}^{16} V_{\text{viga}, j}$$
        $$M_{\text{OTM}}(z=0) = M_{\text{muro}1} + M_{\text{muro}2} + T \cdot L_{\text{arm}}$$
      </div>

      <p class="theory-p">
        donde \(L_{\text{arm}} = 9.15\text{ m}\) es la distancia entre los ejes centroidales de los dos muros. Como demostraron <strong>Ramos y Hube (2021)</strong> y se comprueba interactivamente en el <strong>Lienzo D</strong> de este recurso, el par axial de acople \(T \cdot L_{\text{arm}}\) absorbe <strong>más del 60% del momento de volcamiento total</strong>, protegiendo las bases de los muros individuales contra sobrecargas flectoras extremas y dotando a la estructura de una enorme capacidad de disipación histerética de energía.
      </p>
    </section>

    <!-- VISOR DE CÓDIGO OPENSEESPY -->
    <div class="theory-section">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.75rem;">
        <h2 class="theory-title" style="margin-bottom: 0; border: none; padding: 0;">💻 Script OpenSeesPy del Modelo MVLEM</h2>
        <div style="display: flex; gap: 0.5rem;">
          <a href="https://github.com/odarroyo/analisis_no_lineal/blob/main/Codigos_OpenSeesPy/MVLEM_generator_colab.ipynb" target="_blank" rel="noopener" class="btn-ctrl btn-primary" style="text-decoration: none;">
            <span>📓 Abrir en GitHub / Colab</span>
          </a>
          <button class="btn-ctrl" id="btn-copy-code">📋 Copiar Código</button>
        </div>
      </div>

      <div class="code-panel">
        <div class="code-header">
          <div class="code-tabs">
            <button class="code-tab active" data-tab="0">1. Geometría y Nodos</button>
            <button class="code-tab" data-tab="1">2. Materiales</button>
            <button class="code-tab" data-tab="2">3. Elementos MVLEM</button>
            <button class="code-tab" data-tab="3">4. Vigas de Acople</button>
            <button class="code-tab" data-tab="4">5. Pushover</button>
          </div>
          <span style="font-size: 0.75rem; color: #8b949e; font-family: var(--font-mono);">Python 3 • OpenSeesPy</span>
        </div>
        <pre class="code-content"><code id="code-display"># Cargando código...</code></pre>
      </div>
    </div>

    <!-- EVALUACIÓN FORMATIVA (QUIZ SOCRÁTICO) -->
    <div class="theory-section">
      <h2 class="theory-title">🎯 Autoevaluación Formativa: Conceptos Clave de Muros MVLEM</h2>
      <p class="theory-p">Pon a prueba tu comprensión de la mecánica no lineal y la formulación computacional de muros:</p>

      <!-- Pregunta 1 -->
      <div class="quiz-card" id="q1">
        <div class="quiz-question">1. ¿Por qué el elemento MVLEM ubica su resorte horizontal de cortante a una altura \(c \cdot h\) con \(c \approx 0.40\)?</div>
        <div class="quiz-options">
          <button class="quiz-option" data-opt="0">A) Porque a esa altura el cortante es cero según la teoría elástica de vigas.</button>
          <button class="quiz-option" data-opt="1">B) Porque aproxima la ubicación media del punto de inflexión del muro, minimizando el error en el momento flector inducido por la deformación a corte.</button>
          <button class="quiz-option" data-opt="2">C) Para forzar que el muro falle exclusivamente por corte en lugar de flexión.</button>
          <button class="quiz-option" data-opt="3">D) Es un valor aleatorio de calibración que no influye en la matriz de rigidez.</button>
        </div>
        <div class="quiz-feedback" id="q1-fb"></div>
      </div>

      <!-- Pregunta 2 -->
      <div class="quiz-card" id="q2">
        <div class="quiz-question">2. En un edificio de muros acoplados, ¿qué efecto genera la acción de las vigas de acople sobre el volcamiento global?</div>
        <div class="quiz-options">
          <button class="quiz-option" data-opt="0">A) Las vigas solo transmiten cortante horizontal, por lo que los muros trabajan como si estuvieran completamente aislados.</button>
          <button class="quiz-option" data-opt="1">B) El cortante vertical acumulado de las vigas crea un par axial de tracción/compresión \(T \cdot L_{\text{arm}}\) que resiste la mayor parte del momento de volcamiento total.</button>
          <button class="quiz-option" data-opt="2">C) Aumenta el momento flector en la base de ambos muros de forma simultánea e idéntica.</button>
          <button class="quiz-option" data-opt="3">D) Elimina la deformación axial en los muros haciéndolos infinitamente rígidos verticalmente.</button>
        </div>
        <div class="quiz-feedback" id="q2-fb"></div>
      </div>

      <!-- Pregunta 3 -->
      <div class="quiz-card" id="q3">
        <div class="quiz-question">3. ¿Cuál es la principal ventaja de utilizar un modelo de concreto confinado (Concrete02 con \(k = 1.3\)) en los elementos de borde?</div>
        <div class="quiz-options">
          <button class="quiz-option" data-opt="0">A) Reducir el módulo de elasticidad inicial del muro para que sea más flexible.</button>
          <button class="quiz-option" data-opt="1">B) El aumento de resistencia a compresión (\(f'_{cc} = 45.5\text{ MPa}\)) y la gran capacidad de deformación inelástica (\(\epsilon_{cu} = 0.018\)) debida al confinamiento de los estribos en los extremos del muro.</button>
          <button class="quiz-option" data-opt="2">C) Duplicar la resistencia a tracción del concreto hasta alcanzar la fluencia del acero.</button>
          <button class="quiz-option" data-opt="3">D) Impedir cualquier tipo de agrietamiento durante toda la historia de desplazamiento.</button>
        </div>
        <div class="quiz-feedback" id="q3-fb"></div>
      </div>

      <!-- Pregunta 4 -->
      <div class="quiz-card" id="q4">
        <div class="quiz-question">4. Al observar el perfil de deformaciones unitarias \(\epsilon_k(x)\) en la base del Muro 1 (barlovento), ¿por qué casi todas las fibras entran en tracción plástica?</div>
        <div class="quiz-options">
          <button class="quiz-option" data-opt="0">A) Porque el programa tiene un error numérico de integración seccional.</button>
          <button class="quiz-option" data-opt="1">B) Debido a que la fuerza de tracción neta inducida por el acople \(T\) supera la carga axial gravitacional, reduciendo drásticamente la zona comprimida del muro.</button>
          <button class="quiz-option" data-opt="2">C) Porque el concreto no tiene resistencia a compresión en el modelo MVLEM.</button>
          <button class="quiz-option" data-opt="3">D) Porque las vigas de acople empujan hacia abajo el muro de barlovento.</button>
        </div>
        <div class="quiz-feedback" id="q4-fb"></div>
      </div>
    </section>

  </main>

  <!-- DATASET EMBEBIDO DIRECTAMENTE DE OPENSEESPY -->
  <script>
    window.MVLEM_DATA = /*MVLEM_JSON_DATA*/;
  </script>

  <!-- LÓGICA DE INTERACCIÓN, CANVAS 2D Y FÍSICA -->
  <script>
    /* ==========================================================================
       VARIABLES GLOBALES DE ESTADO Y DATOS DE SIMULACIÓN
       ========================================================================== */
    const MVLEM = window.MVLEM_DATA || {};
    const states = MVLEM.interactive_states || [];
    const totalStates = states.length;

    let isInitialized = false;
    let currentStepIdx = 0;
    let isPlaying = false;
    let playTimer = null;
    let playSpeed = 1;
    let scaleAmp = 15; // Factor de amplificación visual de la deformada
    let activeCurveMode = 'vw'; // 'vw' o 'dim'
    let activeWallIdx = 0; // 0: Muro 1 (Tracción), 1: Muro 2 (Compresión)
    let activeViewD = 'drift'; // 'drift' o 'moments'

    /* ==========================================================================
       GESTIÓN DEL TEMA CLARO / OSCURO CON PERSISTENCIA
       ========================================================================== */
    function applyTheme(isDark) {
      if (isDark) {
        document.body.classList.add('dark-theme');
        const icon = document.getElementById('theme-icon');
        if (icon) icon.textContent = '☀️';
      } else {
        document.body.classList.remove('dark-theme');
        const icon = document.getElementById('theme-icon');
        if (icon) icon.textContent = '🌙';
      }
      try {
        localStorage.setItem('nl_course_theme_mvlem', isDark ? 'dark' : 'light');
      } catch (e) {}

      // Solo redibujar si ya se completó la inicialización
      if (isInitialized) {
        renderAllCanvases();
      }
    }

    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', () => {
        const isDark = !document.body.classList.contains('dark-theme');
        applyTheme(isDark);
      });
    }

    // Cargar tema guardado
    let savedTheme = 'light';
    try {
      savedTheme = localStorage.getItem('nl_course_theme_mvlem') || localStorage.getItem('nl_course_theme') || 'light';
    } catch(e) {}
    applyTheme(savedTheme === 'dark');

    /* ==========================================================================
       ESTADOS FÍSICOS Y MECANISMO DE DAÑO
       ========================================================================== */
    function getPhysicalState(drift) {
      if (drift < 0.12) {
        return { name: "Elástico Lineal", desc: "Sin agrietamiento ni plastificación apreciable" };
      } else if (drift < 0.25) {
        return { name: "Agrietamiento y Fluencia", desc: "Primera fluencia en armadura de borde a tracción" };
      } else if (drift < 0.50) {
        return { name: "Capacidad Máxima (Pico)", desc: "Cortante basal máximo (Vb = 11,329 kN) y fluencia en vigas" };
      } else if (drift < 0.85) {
        return { name: "Degradación / Daño", desc: "Aplastamiento inicial de bulbo en compresión" };
      } else if (drift < 1.15) {
        return { name: "Plastificación Extensa", desc: "Límite de diseño NSR-10 (1.0% deriva) superado" };
      } else {
        return { name: "Demanda Extrema", desc: "Deformación inelástica severa en la rótula plástica basal" };
      }
    }

    /* ==========================================================================
       ACTUALIZACIÓN DEL PASO DE ANÁLISIS
       ========================================================================== */
    const slider = document.getElementById('pushover-slider');
    const stepDisplay = document.getElementById('step-display');
    const dispDisplay = document.getElementById('disp-display');
    const driftDisplay = document.getElementById('drift-display');

    const kpiDrift = document.getElementById('kpi-drift');
    const kpiDisp = document.getElementById('kpi-disp');
    const kpiShear = document.getElementById('kpi-shear');
    const kpiVw = document.getElementById('kpi-vw');
    const kpiCouple = document.getElementById('kpi-couple');
    const kpiState = document.getElementById('kpi-state');
    const kpiStateDesc = document.getElementById('kpi-state-desc');

    if (slider) {
      slider.max = totalStates > 0 ? totalStates - 1 : 52;
    }

    function updateStep(idx) {
      if (totalStates === 0) return;
      currentStepIdx = Math.max(0, Math.min(idx, totalStates - 1));

      if (slider) slider.value = currentStepIdx;

      const st = states[currentStepIdx];
      if (stepDisplay) stepDisplay.textContent = `${currentStepIdx} / ${totalStates - 1}`;
      if (dispDisplay) dispDisplay.textContent = `${st.roof_disp_m.toFixed(4)} m`;
      if (driftDisplay) driftDisplay.textContent = `${st.roof_drift_pct.toFixed(3)} % Drift`;

      if (kpiDrift) kpiDrift.textContent = `${st.roof_drift_pct.toFixed(3)} %`;
      if (kpiDisp) kpiDisp.textContent = `Desplazamiento: ${st.roof_disp_m.toFixed(4)} m`;
      if (kpiShear) kpiShear.textContent = `${st.base_shear_kN.toLocaleString('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kN`;
      if (kpiVw) kpiVw.textContent = st.coeff_vw.toFixed(3);
      if (kpiCouple) kpiCouple.textContent = `${st.moments_kNm.couple_ratio_pct.toFixed(1)} %`;

      const phys = getPhysicalState(st.roof_drift_pct);
      if (kpiState) kpiState.textContent = phys.name;
      if (kpiStateDesc) kpiStateDesc.textContent = phys.desc;

      // Actualizar botones de presets
      document.querySelectorAll('.btn-preset').forEach(btn => {
        const bStep = parseInt(btn.dataset.step);
        if (Math.abs(bStep - currentStepIdx) <= 1) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });

      renderAllCanvases();
    }

    if (slider) {
      slider.addEventListener('input', (e) => {
        updateStep(parseInt(e.target.value));
      });
    }

    // Controles Play / Pause
    const btnPlay = document.getElementById('btn-play');
    function togglePlay() {
      isPlaying = !isPlaying;
      if (isPlaying) {
        if (btnPlay) {
          btnPlay.innerHTML = '⏸️ Pausar';
          btnPlay.classList.add('active');
        }
        if (currentStepIdx >= totalStates - 1) currentStepIdx = 0;
        playTimer = setInterval(() => {
          if (currentStepIdx < totalStates - 1) {
            updateStep(currentStepIdx + 1);
          } else {
            togglePlay();
          }
        }, 140 / playSpeed);
      } else {
        if (btnPlay) {
          btnPlay.innerHTML = '▶️ Reproducir';
          btnPlay.classList.remove('active');
        }
        if (playTimer) clearInterval(playTimer);
      }
    }
    if (btnPlay) btnPlay.addEventListener('click', togglePlay);

    const btnPrev = document.getElementById('btn-prev');
    if (btnPrev) btnPrev.addEventListener('click', () => updateStep(currentStepIdx - 1));

    const btnNext = document.getElementById('btn-next');
    if (btnNext) btnNext.addEventListener('click', () => updateStep(currentStepIdx + 1));

    const btnReset = document.getElementById('btn-reset');
    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (isPlaying) togglePlay();
        updateStep(0);
      });
    }

    const speedSelect = document.getElementById('speed-select');
    if (speedSelect) {
      speedSelect.addEventListener('change', (e) => {
        playSpeed = parseFloat(e.target.value);
        if (isPlaying) {
          clearInterval(playTimer);
          playTimer = setInterval(() => {
            if (currentStepIdx < totalStates - 1) {
              updateStep(currentStepIdx + 1);
            } else {
              togglePlay();
            }
          }, 140 / playSpeed);
        }
      });
    }

    // Botones de presets
    document.querySelectorAll('.btn-preset').forEach(btn => {
      btn.addEventListener('click', () => {
        updateStep(parseInt(btn.dataset.step));
      });
    });

    // Toolbars de Canvases
    const btnScale = document.getElementById('btn-scale-toggle');
    if (btnScale) {
      btnScale.addEventListener('click', (e) => {
        if (scaleAmp === 15) {
          scaleAmp = 30;
          e.target.textContent = 'Escala: 30x (Amplificada)';
        } else if (scaleAmp === 30) {
          scaleAmp = 5;
          e.target.textContent = 'Escala: 5x (Sutil)';
        } else {
          scaleAmp = 15;
          e.target.textContent = 'Escala: 15x';
        }
        renderCanvasBuilding();
      });
    }

    const btnCurveVw = document.getElementById('btn-curve-vw');
    const btnCurveDim = document.getElementById('btn-curve-dim');
    if (btnCurveVw && btnCurveDim) {
      btnCurveVw.addEventListener('click', () => {
        activeCurveMode = 'vw';
        btnCurveVw.classList.add('active');
        btnCurveDim.classList.remove('active');
        renderCanvasPushover();
      });
      btnCurveDim.addEventListener('click', () => {
        activeCurveMode = 'dim';
        btnCurveDim.classList.add('active');
        btnCurveVw.classList.remove('active');
        renderCanvasPushover();
      });
    }

    const btnWall1 = document.getElementById('btn-wall-select');
    const btnWall2 = document.getElementById('btn-wall-select2');
    if (btnWall1 && btnWall2) {
      btnWall1.addEventListener('click', () => {
        activeWallIdx = 0;
        btnWall1.classList.add('active');
        btnWall2.classList.remove('active');
        renderCanvasFibers();
      });
      btnWall2.addEventListener('click', () => {
        activeWallIdx = 1;
        btnWall2.classList.add('active');
        btnWall1.classList.remove('active');
        renderCanvasFibers();
      });
    }

    const btnViewDrift = document.getElementById('btn-view-drift');
    const btnViewMoments = document.getElementById('btn-view-moments');
    if (btnViewDrift && btnViewMoments) {
      btnViewDrift.addEventListener('click', () => {
        activeViewD = 'drift';
        btnViewDrift.classList.add('active');
        btnViewMoments.classList.remove('active');
        const titleD = document.getElementById('title-canvas-d');
        if (titleD) titleD.textContent = '📊 Perfil de Deriva de Entrepiso en la Altura';
        const legD = document.getElementById('legend-canvas-d');
        if (legD) {
          legD.innerHTML = `
            <div class="legend-item"><span class="legend-swatch" style="background: #0d6f73;"></span> Deriva Entrepiso \\(\\Delta_i / h_i\\) (%)</div>
            <div class="legend-item"><span class="legend-swatch" style="background: #e11d48;"></span> Límite NSR-10 (1.0%)</div>
          `;
          if (window.renderMathInElement) window.renderMathInElement(legD);
        }
        renderCanvasDrift();
      });
      btnViewMoments.addEventListener('click', () => {
        activeViewD = 'moments';
        btnViewMoments.classList.add('active');
        btnViewDrift.classList.remove('active');
        const titleD = document.getElementById('title-canvas-d');
        if (titleD) titleD.textContent = '⚖️ Descomposición del Momento de Volcamiento (M_OTM)';
        const legD = document.getElementById('legend-canvas-d');
        if (legD) {
          legD.innerHTML = `
            <div class="legend-item"><span class="legend-swatch" style="background: #7c3aed;"></span> Par de Acople (\\(T \\cdot L\\))</div>
            <div class="legend-item"><span class="legend-swatch" style="background: #0284c7;"></span> Flexión Muro 1 (\\(M_1\\))</div>
            <div class="legend-item"><span class="legend-swatch" style="background: #0d6f73;"></span> Flexión Muro 2 (\\(M_2\\))</div>
          `;
          if (window.renderMathInElement) window.renderMathInElement(legD);
        }
        renderCanvasDrift();
      });
    }

    /* ==========================================================================
       CANVAS 2D: RENDERIZADORES GRÁFICOS CON SOPORTE HiDPI
       ========================================================================== */
    function setupCanvas(canvas) {
      if (!canvas) return null;
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      const w = rect.width > 0 ? rect.width : (canvas.parentElement ? canvas.parentElement.clientWidth : 400);
      const h = rect.height > 0 ? rect.height : 380;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      const ctx = canvas.getContext('2d');
      ctx.resetTransform();
      ctx.scale(dpr, dpr);
      return { ctx, width: w, height: h };
    }

    function isDark() {
      return document.body.classList.contains('dark-theme');
    }

    // LIENZO A: ELEVACIÓN DEL EDIFICIO DE 16 PISOS
    function renderCanvasBuilding() {
      const canvas = document.getElementById('canvas-building');
      const setup = setupCanvas(canvas);
      if (!setup) return;
      const { ctx, width, height } = setup;

      const dark = isDark();
      const colGrid = dark ? '#1e293b' : '#e2e8f0';
      const colText = dark ? '#94a3b8' : '#64748b';
      const colGround = dark ? '#334155' : '#cbd5e1';

      ctx.clearRect(0, 0, width, height);

      if (states.length === 0) return;
      const st = states[currentStepIdx];
      const floorDisps = st.floor_disps_m;
      const H = (MVLEM.metadata && MVLEM.metadata.total_height_m) ? MVLEM.metadata.total_height_m : 41.6;
      const numStories = 16;
      const wallDist = 9.15; // m
      const wallLen = 7.65;  // m

      // Márgenes y escalas de dibujo
      const padBottom = 35;
      const padTop = 25;
      const plotH = height - padBottom - padTop;
      const scaleY = plotH / H;

      // Centro geométrico en X
      const centerX = width * 0.45;
      const scaleX_geom = width * 0.022; // Escala para la distancia entre muros
      const ampX = scaleAmp * 45; // Amplificación visual del desplazamiento

      const xW1_orig = centerX - (wallDist / 2) * scaleX_geom;
      const xW2_orig = centerX + (wallDist / 2) * scaleX_geom;
      const wWallPx = wallLen * scaleX_geom * 0.45;

      // 1. Suelo / Cimentación
      const yGround = height - padBottom;
      ctx.strokeStyle = colGround;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(20, yGround);
      ctx.lineTo(width - 20, yGround);
      ctx.stroke();

      // Hachurado de empotramiento en la base
      ctx.strokeStyle = colGrid;
      ctx.lineWidth = 1;
      for (let x = 30; x < width - 30; x += 12) {
        ctx.beginPath();
        ctx.moveTo(x, yGround);
        ctx.lineTo(x - 8, yGround + 10);
        ctx.stroke();
      }

      // 2. Dibujar pisos y deformada
      ctx.font = '10px Inter, sans-serif';
      ctx.fillStyle = colText;

      // Nivel de daño según la deriva
      const drift = st.roof_drift_pct;
      let colBeam = '#10b981'; // Verde elástico
      if (drift > 0.4) colBeam = '#f59e0b'; // Ámbar plastificación
      if (drift > 0.9) colBeam = '#e11d48'; // Rojo daño extenso

      // Coordenadas calculadas piso a piso
      const ptsW1 = [];
      const ptsW2 = [];

      for (let j = 0; j <= numStories; j++) {
        const z = j * 2.6;
        const yPx = yGround - z * scaleY;
        const uLat = floorDisps[j] * ampX;

        const x1 = xW1_orig + uLat;
        const x2 = xW2_orig + uLat;

        ptsW1.push({ x: x1, y: yPx });
        ptsW2.push({ x: x2, y: yPx });

        // Líneas guía de piso
        if (j > 0 && j % 4 === 0) {
          ctx.strokeStyle = colGrid;
          ctx.setLineDash([3, 3]);
          ctx.beginPath();
          ctx.moveTo(35, yPx);
          ctx.lineTo(width - 35, yPx);
          ctx.stroke();
          ctx.setLineDash([]);
          ctx.fillText(`Piso ${j} (${z.toFixed(1)}m)`, 10, yPx + 3);
        }
      }

      // 3. Dibujar Muros deformados como columnas anchas (polígonos)
      // Muro 1 (Barlovento / Tracción Neta)
      ctx.fillStyle = dark ? 'rgba(2, 132, 199, 0.25)' : 'rgba(2, 132, 199, 0.15)';
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 2.5;

      ctx.beginPath();
      for (let j = 0; j <= numStories; j++) {
        const pt = ptsW1[j];
        if (j === 0) ctx.moveTo(pt.x - wWallPx / 2, pt.y);
        else ctx.lineTo(pt.x - wWallPx / 2, pt.y);
      }
      for (let j = numStories; j >= 0; j--) {
        const pt = ptsW1[j];
        ctx.lineTo(pt.x + wWallPx / 2, pt.y);
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Muro 2 (Sotavento / Compresión Neta)
      ctx.fillStyle = dark ? 'rgba(13, 111, 115, 0.28)' : 'rgba(13, 111, 115, 0.15)';
      ctx.strokeStyle = dark ? '#2dd4bf' : '#0d6f73';
      ctx.lineWidth = 2.5;

      ctx.beginPath();
      for (let j = 0; j <= numStories; j++) {
        const pt = ptsW2[j];
        if (j === 0) ctx.moveTo(pt.x - wWallPx / 2, pt.y);
        else ctx.lineTo(pt.x - wWallPx / 2, pt.y);
      }
      for (let j = numStories; j >= 0; j--) {
        const pt = ptsW2[j];
        ctx.lineTo(pt.x + wWallPx / 2, pt.y);
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // 4. Vigas de acople en cada piso
      ctx.strokeStyle = colBeam;
      ctx.lineWidth = 3;
      for (let j = 1; j <= numStories; j++) {
        const p1 = ptsW1[j];
        const p2 = ptsW2[j];
        ctx.beginPath();
        ctx.moveTo(p1.x + wWallPx / 2, p1.y);
        ctx.lineTo(p2.x - wWallPx / 2, p2.y);
        ctx.stroke();

        // Rótulas plásticas en extremos de vigas si hay plastificación
        if (drift > 0.4) {
          ctx.fillStyle = '#e11d48';
          ctx.beginPath();
          ctx.arc(p1.x + wWallPx / 2 + 3, p1.y, 2.5, 0, Math.PI * 2);
          ctx.arc(p2.x - wWallPx / 2 - 3, p2.y, 2.5, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Rótulas plásticas basales en muros
      if (drift > 0.17) {
        ctx.fillStyle = '#e11d48';
        ctx.beginPath();
        ctx.arc(ptsW1[0].x, ptsW1[0].y - 8, 4, 0, Math.PI * 2);
        ctx.arc(ptsW2[0].x, ptsW2[0].y - 8, 4, 0, Math.PI * 2);
        ctx.fill();
      }

      // 5. Flechas de fuerzas laterales aplicadas (distribución triangular invertida)
      ctx.strokeStyle = dark ? '#fbbf24' : '#d97706';
      ctx.fillStyle = dark ? '#fbbf24' : '#d97706';
      ctx.lineWidth = 1.5;
      for (let j = 4; j <= numStories; j += 4) {
        const pt = ptsW1[j];
        const fLen = (j / numStories) * 35;
        const xStart = pt.x - wWallPx / 2 - fLen - 8;
        const xEnd = pt.x - wWallPx / 2 - 4;

        ctx.beginPath();
        ctx.moveTo(xStart, pt.y);
        ctx.lineTo(xEnd, pt.y);
        ctx.stroke();

        // Punta de flecha
        ctx.beginPath();
        ctx.moveTo(xEnd, pt.y);
        ctx.lineTo(xEnd - 5, pt.y - 3);
        ctx.lineTo(xEnd - 5, pt.y + 3);
        ctx.closePath();
        ctx.fill();
      }

      // Rótulos de Muros en la parte superior
      ctx.font = '700 11px Inter, sans-serif';
      ctx.fillStyle = '#0284c7';
      ctx.fillText("Muro 1 (M1)", ptsW1[numStories].x - 25, ptsW1[numStories].y - 12);
      ctx.fillStyle = dark ? '#2dd4bf' : '#0d6f73';
      ctx.fillText("Muro 2 (M2)", ptsW2[numStories].x - 25, ptsW2[numStories].y - 12);

      // Leyenda de amplificación
      ctx.font = '10px JetBrains Mono, monospace';
      ctx.fillStyle = colText;
      ctx.fillText(`Amplificación visual: ${scaleAmp}x`, width - 170, height - 12);
    }

    // LIENZO B: CURVA DE CAPACIDAD PUSHOVER
    function renderCanvasPushover() {
      const canvas = document.getElementById('canvas-pushover');
      const setup = setupCanvas(canvas);
      if (!setup) return;
      const { ctx, width, height } = setup;

      const dark = isDark();
      const colGrid = dark ? '#1e293b' : '#e2e8f0';
      const colText = dark ? '#94a3b8' : '#64748b';
      const colCurve = dark ? '#2dd4bf' : '#0d6f73';

      ctx.clearRect(0, 0, width, height);

      const pCurve = MVLEM.pushover_curve;
      if (!pCurve) return;

      const isVw = activeCurveMode === 'vw';

      // Parámetros de ejes
      const padLeft = 60;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 45;
      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      // Rangos máximos
      const xMax = isVw ? 1.6 : 0.65; // % Drift o Metros
      const yMax = isVw ? 0.52 : 12500; // V/W o kN

      const getX = (val) => padLeft + (val / xMax) * plotW;
      const getY = (val) => padTop + plotH - (val / yMax) * plotH;

      // 1. Rejilla y Ejes
      ctx.strokeStyle = colGrid;
      ctx.lineWidth = 1;
      ctx.font = '10px Inter, sans-serif';
      ctx.fillStyle = colText;
      ctx.textAlign = 'center';

      // Divisiones en X
      const numXDivs = 5;
      for (let i = 0; i <= numXDivs; i++) {
        const valX = (xMax / numXDivs) * i;
        const xPx = getX(valX);
        ctx.beginPath();
        ctx.moveTo(xPx, padTop);
        ctx.lineTo(xPx, padTop + plotH);
        ctx.stroke();
        ctx.fillText(isVw ? `${valX.toFixed(1)}%` : `${valX.toFixed(2)}m`, xPx, padTop + plotH + 16);
      }

      // Divisiones en Y
      ctx.textAlign = 'right';
      const numYDivs = 5;
      for (let i = 0; i <= numYDivs; i++) {
        const valY = (yMax / numYDivs) * i;
        const yPx = getY(valY);
        ctx.beginPath();
        ctx.moveTo(padLeft, yPx);
        ctx.lineTo(padLeft + plotW, yPx);
        ctx.stroke();
        ctx.fillText(isVw ? valY.toFixed(2) : Math.round(valY), padLeft - 8, yPx + 4);
      }

      // Ejes principales
      ctx.strokeStyle = dark ? '#475569' : '#94a3b8';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(padLeft, padTop);
      ctx.lineTo(padLeft, padTop + plotH);
      ctx.lineTo(padLeft + plotW, padTop + plotH);
      ctx.stroke();

      // Títulos de ejes
      ctx.font = '600 11px Inter, sans-serif';
      ctx.fillStyle = dark ? '#f1f5f9' : '#0f172a';
      ctx.textAlign = 'center';
      ctx.fillText(isVw ? "Deriva de Techo (%)" : "Desplazamiento de Techo D_roof (m)", padLeft + plotW / 2, padTop + plotH + 34);

      ctx.save();
      ctx.translate(16, padTop + plotH / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(isVw ? "Coeficiente Sísmico (V / W)" : "Cortante Basal Total Vb (kN)", 0, 0);
      ctx.restore();

      // 2. Línea de límite NSR-10 (Deriva 1.0%)
      const xNsr = getX(1.0);
      if (isVw && xNsr < padLeft + plotW) {
        ctx.strokeStyle = 'rgba(225, 29, 72, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(xNsr, padTop);
        ctx.lineTo(xNsr, padTop + plotH);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#e11d48';
        ctx.font = '9px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText("Límite NSR-10 (1.0%)", xNsr + 4, padTop + 14);
      }

      // 3. Dibujar Curva Pushover Completa
      const curveX = isVw ? pCurve.drift_pct : pCurve.disp_m;
      const curveY = isVw ? pCurve.coeff_vw : pCurve.shear_kN;

      ctx.strokeStyle = colCurve;
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (let i = 0; i < curveX.length; i++) {
        const px = getX(curveX[i]);
        const py = getY(curveY[i]);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Área sombreada bajo la curva
      ctx.lineTo(getX(curveX[curveX.length - 1]), getY(0));
      ctx.lineTo(getX(0), getY(0));
      ctx.closePath();
      ctx.fillStyle = dark ? 'rgba(45, 212, 191, 0.08)' : 'rgba(13, 111, 115, 0.06)';
      ctx.fill();

      // 4. Marcadores de Hitos Clave
      const hitos = [
        { name: "Fluencia Borde (0.17%)", drift: 0.173, vw: 0.305, shear: 7784 },
        { name: "Capacidad Máx Vb (0.43%)", drift: 0.433, vw: 0.443, shear: 11299 },
        { name: "Aplastamiento (0.75%)", drift: 0.75, vw: 0.333, shear: 8503 }
      ];

      hitos.forEach(h => {
        const hx = getX(isVw ? h.drift : h.drift * 0.416);
        const hy = getY(isVw ? h.vw : h.shear);
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(hx, hy, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // 5. Marcador del Estado Actual
      if (states.length > 0) {
        const st = states[currentStepIdx];
        const curX = getX(isVw ? st.roof_drift_pct : st.roof_disp_m);
        const curY = getY(isVw ? st.coeff_vw : st.base_shear_kN);

        // Líneas guía al punto actual
        ctx.strokeStyle = 'rgba(225, 29, 72, 0.4)';
        ctx.setLineDash([3, 3]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(padLeft, curY);
        ctx.lineTo(curX, curY);
        ctx.lineTo(curX, padTop + plotH);
        ctx.stroke();
        ctx.setLineDash([]);

        // Punto pulsante actual
        ctx.fillStyle = '#e11d48';
        ctx.beginPath();
        ctx.arc(curX, curY, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Rótulo con coordenadas del punto
        ctx.fillStyle = dark ? '#ffffff' : '#0f172a';
        ctx.font = '700 11px JetBrains Mono, monospace';
        ctx.textAlign = curX > width - 120 ? 'right' : 'left';
        const txtLabel = isVw
          ? `(${st.roof_drift_pct.toFixed(2)}%, ${st.coeff_vw.toFixed(3)})`
          : `(${st.roof_disp_m.toFixed(3)}m, ${Math.round(st.base_shear_kN)}kN)`;
        ctx.fillText(txtLabel, curX + (curX > width - 120 ? -10 : 10), curY - 10);
      }
    }

    // LIENZO C: PERFIL SECCIONAL DE DEFORMACIONES DE LAS 8 MACROFIBRAS
    function renderCanvasFibers() {
      const canvas = document.getElementById('canvas-fibers');
      const setup = setupCanvas(canvas);
      if (!setup) return;
      const { ctx, width, height } = setup;

      const dark = isDark();
      const colGrid = dark ? '#1e293b' : '#e2e8f0';
      const colText = dark ? '#94a3b8' : '#64748b';

      ctx.clearRect(0, 0, width, height);
      if (states.length === 0 || !MVLEM.metadata) return;

      const st = states[currentStepIdx];
      const strains = activeWallIdx === 0 ? st.wall1_strains : st.wall2_strains;
      const xCoords = MVLEM.metadata.fiber_coords_x_m; // [-3.675 ... 3.675]
      const widths = MVLEM.metadata.fiber_widths_m;
      const numFibers = 8;
      const wallTitle = activeWallIdx === 0 ? "Muro 1 (Barlovento / Tracción Neta)" : "Muro 2 (Sotavento / Compresión Neta)";

      // Márgenes
      const padLeft = 65;
      const padRight = 35;
      const padTop = 35;
      const padBottom = 45;
      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      // Rangos de deformación en Y: de -0.025 (compresión) a +0.035 (tracción)
      const epsMin = -0.025;
      const epsMax = 0.035;

      const getX = (valX) => padLeft + ((valX + 3.825) / 7.65) * plotW;
      const getY = (valEps) => padTop + plotH - ((valEps - epsMin) / (epsMax - epsMin)) * plotH;

      // 1. Rejilla y Eje Neutro (eps = 0)
      ctx.strokeStyle = colGrid;
      ctx.lineWidth = 1;

      // Líneas horizontales de deformación
      const gridEps = [-0.02, -0.01, 0, 0.01, 0.02, 0.03];
      ctx.font = '10px JetBrains Mono, monospace';
      ctx.fillStyle = colText;
      ctx.textAlign = 'right';

      gridEps.forEach(epsVal => {
        const yPx = getY(epsVal);
        ctx.beginPath();
        ctx.moveTo(padLeft, yPx);
        ctx.lineTo(padLeft + plotW, yPx);
        ctx.stroke();
        ctx.fillText((epsVal * 1000).toFixed(0) + "‰", padLeft - 8, yPx + 4);
      });

      // EJE NEUTRO DESTACADO (eps = 0)
      const yZero = getY(0);
      ctx.strokeStyle = dark ? '#64748b' : '#94a3b8';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(padLeft, yZero);
      ctx.lineTo(padLeft + plotW, yZero);
      ctx.stroke();

      // Límites de materiales
      // Fluencia acero tracción eps_y = 0.0021
      const yEy = getY(0.0021);
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.7)';
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(padLeft, yEy);
      ctx.lineTo(padLeft + plotW, yEy);
      ctx.stroke();
      ctx.fillStyle = '#f59e0b';
      ctx.font = '9px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText("Fluencia Acero (\u03B5y = +0.0021)", padLeft + 8, yEy - 3);

      // Aplastamiento concreto confinado eps_cu = -0.018
      const yEcu = getY(-0.018);
      ctx.strokeStyle = 'rgba(225, 29, 72, 0.7)';
      ctx.beginPath();
      ctx.moveTo(padLeft, yEcu);
      ctx.lineTo(padLeft + plotW, yEcu);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#e11d48';
      ctx.fillText("Aplastamiento Concreto Confinado (\u03B5cu = -0.018)", padLeft + 8, yEcu - 3);

      // 2. Dibujar las 8 barras de macrofibra
      for (let k = 0; k < numFibers; k++) {
        const xCent = xCoords[k];
        const bW = widths[k];
        const eps = strains[k];

        const xLeft = getX(xCent - bW / 2);
        const xRight = getX(xCent + bW / 2);
        const barW = Math.max(xRight - xLeft, 2);
        const yVal = getY(eps);

        // Color según el estado
        let colBar = '#0284c7'; // Compresión
        if (eps > 0.0021) {
          colBar = '#e11d48'; // Fluencia tracción
        } else if (eps > 0) {
          colBar = '#f59e0b'; // Tracción elástica
        } else if (eps < -0.018) {
          colBar = '#7f1d1d'; // Aplastamiento severo
        }

        ctx.fillStyle = colBar;
        const rectTop = Math.min(yZero, yVal);
        const rectHeight = Math.abs(yVal - yZero);
        ctx.fillRect(xLeft, rectTop, barW - 1, rectHeight);

        // Borde de la barra
        ctx.strokeStyle = dark ? '#0b1320' : '#ffffff';
        ctx.lineWidth = 1;
        ctx.strokeRect(xLeft, rectTop, barW - 1, rectHeight);

        // Rótulo del número de fibra
        ctx.font = '9px Inter, sans-serif';
        ctx.fillStyle = colText;
        ctx.textAlign = 'center';
        ctx.fillText(`F${k + 1}`, (xLeft + xRight) / 2, padTop + plotH + 16);
      }

      // 3. Línea continua de sección plana (Navier-Bernoulli: eps(x) = eps0 + x * phi)
      ctx.strokeStyle = dark ? '#ffffff' : '#0f172a';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (let k = 0; k < numFibers; k++) {
        const px = getX(xCoords[k]);
        const py = getY(strains[k]);
        if (k === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();

      // Puntos sobre la línea
      for (let k = 0; k < numFibers; k++) {
        const px = getX(xCoords[k]);
        const py = getY(strains[k]);
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(px, py, 3.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#0f172a';
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // Título de la pared activa
      ctx.font = '700 11px Inter, sans-serif';
      ctx.fillStyle = dark ? '#ffffff' : '#0f172a';
      ctx.textAlign = 'center';
      ctx.fillText(wallTitle, padLeft + plotW / 2, padTop - 12);
    }

    // LIENZO D: DERIVAS DE ENTREPISO Y DESCOMPOSICIÓN DE VOLCAMIENTO
    function renderCanvasDrift() {
      const canvas = document.getElementById('canvas-drift');
      const setup = setupCanvas(canvas);
      if (!setup) return;
      const { ctx, width, height } = setup;

      const dark = isDark();
      const colGrid = dark ? '#1e293b' : '#e2e8f0';
      const colText = dark ? '#94a3b8' : '#64748b';

      ctx.clearRect(0, 0, width, height);
      if (states.length === 0) return;

      const st = states[currentStepIdx];
      const isDrift = activeViewD === 'drift';

      const padLeft = 60;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 45;
      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      if (isDrift) {
        // ==========================================
        // VISTA 1: PERFIL DE DERIVA DE ENTREPISO (%)
        // ==========================================
        const numStories = 16;
        const drifts = st.story_drifts_pct;
        const driftMax = 1.6; // % escala máxima

        const getX = (valD) => padLeft + (valD / driftMax) * plotW;
        const getY = (story) => padTop + plotH - (story / numStories) * plotH;

        // Rejilla
        ctx.strokeStyle = colGrid;
        ctx.lineWidth = 1;
        ctx.font = '10px Inter, sans-serif';
        ctx.fillStyle = colText;
        ctx.textAlign = 'center';

        for (let d = 0; d <= driftMax; d += 0.4) {
          const xPx = getX(d);
          ctx.beginPath();
          ctx.moveTo(xPx, padTop);
          ctx.lineTo(xPx, padTop + plotH);
          ctx.stroke();
          ctx.fillText(`${d.toFixed(1)}%`, xPx, padTop + plotH + 16);
        }

        ctx.textAlign = 'right';
        for (let s = 2; s <= numStories; s += 2) {
          const yPx = getY(s);
          ctx.beginPath();
          ctx.moveTo(padLeft, yPx);
          ctx.lineTo(padLeft + plotW, yPx);
          ctx.stroke();
          ctx.fillText(`P${s}`, padLeft - 8, yPx + 4);
        }

        // Límite NSR-10 (1.0%)
        const xLimit = getX(1.0);
        ctx.strokeStyle = 'rgba(225, 29, 72, 0.7)';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(xLimit, padTop);
        ctx.lineTo(xLimit, padTop + plotH);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#e11d48';
        ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText("Límite NSR-10 (1.0%)", xLimit + 4, padTop + 14);

        // Perfil de Deriva
        ctx.strokeStyle = dark ? '#2dd4bf' : '#0d6f73';
        ctx.lineWidth = 3;
        ctx.beginPath();
        for (let s = 1; s <= numStories; s++) {
          const dVal = drifts[s - 1];
          const px = getX(dVal);
          const py = getY(s);
          if (s === 1) ctx.moveTo(px, py);
          else ctx.lineTo(px, py);
        }
        ctx.stroke();

        // Puntos
        for (let s = 1; s <= numStories; s++) {
          const dVal = drifts[s - 1];
          const px = getX(dVal);
          const py = getY(s);
          ctx.fillStyle = dVal > 1.0 ? '#e11d48' : '#0d6f73';
          ctx.beginPath();
          ctx.arc(px, py, 4, 0, Math.PI * 2);
          ctx.fill();
        }

        // Título eje X
        ctx.font = '600 11px Inter, sans-serif';
        ctx.fillStyle = dark ? '#f1f5f9' : '#0f172a';
        ctx.textAlign = 'center';
        ctx.fillText("Deriva de Entrepiso (% altura de entrepiso)", padLeft + plotW / 2, padTop + plotH + 34);

      } else {
        // ==========================================
        // VISTA 2: DESCOMPOSICIÓN DE VOLCAMIENTO
        // ==========================================
        const mData = st.moments_kNm;
        const m1 = Math.abs(mData.m_wall1);
        const m2 = Math.abs(mData.m_wall2);
        const mCouple = Math.abs(mData.m_couple);
        const mTotal = m1 + m2 + mCouple;

        const maxM = 280000; // kNm escala
        const barW = 60;

        // Barras de momentos: M1, M2, T*L, Total
        const items = [
          { label: "Muro 1 (M1)", val: m1, col: "#0284c7" },
          { label: "Muro 2 (M2)", val: m2, col: dark ? "#2dd4bf" : "#0d6f73" },
          { label: "Par T·L", val: mCouple, col: "#7c3aed" },
          { label: "M_OTM Total", val: mTotal, col: "#d97706" }
        ];

        const spacing = plotW / items.length;

        // Rejilla horizontal
        ctx.strokeStyle = colGrid;
        ctx.lineWidth = 1;
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillStyle = colText;
        ctx.textAlign = 'right';

        for (let mVal = 0; mVal <= maxM; mVal += 50000) {
          const yPx = padTop + plotH - (mVal / maxM) * plotH;
          ctx.beginPath();
          ctx.moveTo(padLeft, yPx);
          ctx.lineTo(padLeft + plotW, yPx);
          ctx.stroke();
          ctx.fillText((mVal / 1000).toFixed(0) + "k", padLeft - 8, yPx + 4);
        }

        // Dibujar barras
        items.forEach((item, idx) => {
          const xCenter = padLeft + spacing * idx + spacing / 2;
          const barH = (item.val / maxM) * plotH;
          const yPx = padTop + plotH - barH;

          ctx.fillStyle = item.col;
          ctx.fillRect(xCenter - barW / 2, yPx, barW, barH);
          ctx.strokeStyle = dark ? '#0b1320' : '#ffffff';
          ctx.lineWidth = 1;
          ctx.strokeRect(xCenter - barW / 2, yPx, barW, barH);

          // Rótulo con valor
          ctx.font = '700 10px JetBrains Mono, monospace';
          ctx.fillStyle = dark ? '#f1f5f9' : '#0f172a';
          ctx.textAlign = 'center';
          ctx.fillText(`${(item.val / 1000).toFixed(1)}k`, xCenter, yPx - 6);

          // Rótulo de categoría
          ctx.font = '600 10px Inter, sans-serif';
          ctx.fillStyle = colText;
          ctx.fillText(item.label, xCenter, padTop + plotH + 16);

          // Porcentaje del total
          if (mTotal > 0 && idx < 3) {
            const pct = ((item.val / mTotal) * 100).toFixed(1);
            ctx.font = '700 9px Inter, sans-serif';
            ctx.fillStyle = item.col;
            ctx.fillText(`${pct}%`, xCenter, padTop + plotH + 28);
          }
        });

        ctx.font = '600 11px Inter, sans-serif';
        ctx.fillStyle = dark ? '#f1f5f9' : '#0f172a';
        ctx.textAlign = 'center';
        ctx.fillText("Componentes del Momento de Volcamiento (kN·m)", padLeft + plotW / 2, padTop - 12);
      }
    }

    function renderAllCanvases() {
      renderCanvasBuilding();
      renderCanvasPushover();
      renderCanvasFibers();
      renderCanvasDrift();
    }

    window.addEventListener('resize', renderAllCanvases);

    /* ==========================================================================
       SNIPPETS DE CÓDIGO OPENSEESPY
       ========================================================================== */
    const CODE_SNIPPETS = [
      `# 1. DEFINICIÓN DE GEOMETRÍA Y NODOS DEL EDIFICIO DE 16 PISOS
import openseespy.opensees as ops

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

# Parámetros del Edificio
N_stories = 16
h_story = 2.6  # Altura de entrepiso en metros
L_wall = 7.65   # Longitud de cada muro en metros
L_arm = 9.15    # Distancia entre ejes centroidales de muros
c_shear = 0.40  # Altura relativa del resorte de cortante MVLEM

# Generación de nodos principales de muros
for j in range(N_stories + 1):
    y = j * h_story
    # Muro 1 (Centroide en X = 0.0)
    ops.node(1000 + j, 0.0, y)
    # Muro 2 (Centroide en X = 9.15)
    ops.node(2000 + j, L_arm, y)

# Empotramiento en la base (Piso 0)
ops.fix(1000, 1, 1, 1)
ops.fix(2000, 1, 1, 1)`,

      `# 2. DEFINICIÓN DE MATERIALES UNIAXIALES
# Material 1: Concreto confinado en bulbos de borde (Concrete02)
fc_conf = -45.5e3  # 45.5 MPa (Confinado Mander)
eps_0_conf = -0.004
fcu_conf = -9.1e3   # 20% resistencia residual
epsu_conf = -0.018  # Gran ductilidad por estribos
lambda_ratio = 0.1
ft_conf = 2070.0
Ets = 2.0e6
ops.uniaxialMaterial('Concrete02', 1, fc_conf, eps_0_conf, fcu_conf, epsu_conf, lambda_ratio, ft_conf, Ets)

# Material 2: Concreto no confinado en el alma
fc_unconf = -35.0e3  # 35 MPa
eps_0_unconf = -0.002
fcu_unconf = 0.0
epsu_unconf = -0.006
ops.uniaxialMaterial('Concrete02', 2, fc_unconf, eps_0_unconf, fcu_unconf, epsu_unconf, lambda_ratio, ft_conf, Ets)

# Material 3: Acero de refuerzo longitudinal (Hysteretic)
Fy = 420.0e3    # 420 MPa
Es = 200.0e6    # 200 GPa
eps_y = Fy / Es # 0.0021
ops.uniaxialMaterial('Hysteretic', 3,
    Fy, eps_y, 1.25*Fy, 0.05, 0.2*Fy, 0.10,
    -Fy, -eps_y, -1.25*Fy, -0.05, -0.2*Fy, -0.10,
    0.5, 0.5, 0.0, 0.0)`,

      `# 3. CONSTRUCCIÓN DE ELEMENTOS MVLEM EN LA ALTURA
# Cada muro tiene 8 macrofibras (bulbos de 7.5m espesor y alma de 0.3m)
fiber_thick_W1 = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 7.5]
fiber_thick_W2 = [7.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
fiber_widths = [0.3, 1.175, 1.175, 1.175, 1.175, 1.175, 1.175, 0.3]
rebar_ratio = [0.012]*8

# Propiedades del resorte de cortante a altura c*h
G = 9.8e6  # Módulo de corte
Av = 0.3 * 7.65 * 0.83  # Área de cortante efectiva
Kh = (G * Av) / h_story

for j in range(1, N_stories + 1):
    tag_ele1 = 100 + j
    tag_ele2 = 200 + j
    # Elemento MVLEM: tag, dens, ndI, ndJ, m, c
    ops.element('MVLEM', tag_ele1, 0.0, 1000 + j - 1, 1000 + j, 8, c_shear,
                '-thick', *fiber_thick_W1, '-width', *fiber_widths,
                '-rho', *rebar_ratio, '-matConcrete', 1, 2, 2, 2, 2, 2, 2, 1,
                '-matSteel', 3, 3, 3, 3, 3, 3, 3, 3, '-matShear', 4)`,

      `# 4. CONECTIVIDAD DE VIGAS DE ACOPLE Y DIAFRAGMAS RÍGIDOS
# Viga de enlace elástica con rigidez reducida por agrietamiento
L_clear_beam = 1.50 # m (Viga corta de acople)
h_beam = 0.60
b_beam = 0.30
I_beam_cracked = 0.35 * (b_beam * h_beam**3 / 12.0)
A_beam = b_beam * h_beam

# Conectar nodos de borde mediante elementos viga
for j in range(1, N_stories + 1):
    beam_tag = 5000 + j
    # Conexión entre cara derecha de Muro 1 y cara izquierda de Muro 2
    ops.element('elasticBeamColumn', beam_tag, 1000 + j, 2000 + j,
                A_beam, 2.5e7, I_beam_cracked, 1)`,

      `# 5. PROTOCOLO DE ANÁLISIS PUSHOVER MONOTÓNICO
# Patrón de cargas laterales triangulares invertidas
ops.pattern('Plain', 2, 1)
for j in range(1, N_stories + 1):
    z = j * h_story
    F_lat = (z / 41.6) * 100.0  # Distribución de fuerza proporcional a la altura
    ops.load(1000 + j, F_lat, 0.0, 0.0)
    ops.load(2000 + j, F_lat, 0.0, 0.0)

# Algoritmo de control por desplazamiento en el nodo de cubierta
node_ctrl = 1000 + N_stories
D_max = 0.015 * 41.6  # 1.5% deriva = 0.624 m
d_incr = 0.0005       # Pasos de 0.5 mm

ops.integrator('DisplacementControl', node_ctrl, 1, d_incr)
ops.analysis('Static')
# Ejecución del pushover registrando cortante basal y derivas...`
    ];

    const codeDisplay = document.getElementById('code-display');
    if (codeDisplay) {
      codeDisplay.textContent = CODE_SNIPPETS[0];
    }

    document.querySelectorAll('.code-tab').forEach(tab => {
      tab.addEventListener('click', (e) => {
        document.querySelectorAll('.code-tab').forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        const tabIdx = parseInt(e.target.dataset.tab);
        if (codeDisplay) codeDisplay.textContent = CODE_SNIPPETS[tabIdx];
      });
    });

    const btnCopy = document.getElementById('btn-copy-code');
    if (btnCopy) {
      btnCopy.addEventListener('click', () => {
        if (!codeDisplay) return;
        navigator.clipboard.writeText(codeDisplay.textContent).then(() => {
          btnCopy.textContent = '✅ ¡Copiado!';
          setTimeout(() => btnCopy.textContent = '📋 Copiar Código', 2000);
        });
      });
    }

    /* ==========================================================================
       EVALUACIÓN FORMATIVA (QUIZ INTERACTIVO)
       ========================================================================== */
    const QUIZ_ANSWERS = {
      q1: { correct: 1, explanation: "¡Correcto! En muros esbeltos dominados por flexión, el punto de inflexión de momento flector se ubica aproximadamente al 40% de la altura de entrepiso (c = 0.40). Ubicar allí el resorte de cortante minimiza el momento espurio introducido por la rotación de los nodos." },
      q2: { correct: 1, explanation: "¡Correcto! La acumulación del cortante vertical transferido por las vigas de acople crea un par axial de tracción/compresión T · L que resiste más del 60% del momento de volcamiento total, aligerando drásticamente los flectores en la base de cada muro." },
      q3: { correct: 1, explanation: "¡Correcto! El confinamiento provisto por los estribos cerrados incrementa tanto la resistencia máxima a compresión (Mander k = 1.3 -> 45.5 MPa) como la ductilidad de deformación última (ecu = 0.018), evitando fallas frágiles por compresión en los extremos del muro." },
      q4: { correct: 1, explanation: "¡Correcto! La fuerza axial de tracción neta inducida por el acople reduce la zona comprimida del muro de barlovento, empujando el eje neutro hacia el extremo más comprimido y provocando que casi todas las macrofibras del alma entren en fluencia por tracción." }
    };

    document.querySelectorAll('.quiz-card').forEach(card => {
      const qId = card.id;
      const qData = QUIZ_ANSWERS[qId];
      if (!qData) return;

      const fb = card.querySelector('.quiz-feedback');
      const options = card.querySelectorAll('.quiz-option');

      options.forEach(btn => {
        btn.addEventListener('click', () => {
          options.forEach(b => {
            b.classList.remove('correct', 'incorrect');
            b.disabled = true;
          });
          const chosen = parseInt(btn.dataset.opt);

          if (chosen === qData.correct) {
            btn.classList.add('correct');
            if (fb) {
              fb.style.display = 'block';
              fb.style.background = 'rgba(5, 150, 105, 0.15)';
              fb.style.color = '#059669';
              fb.textContent = qData.explanation;
            }
          } else {
            btn.classList.add('incorrect');
            const correctBtn = card.querySelector(`[data-opt="${qData.correct}"]`);
            if (correctBtn) correctBtn.classList.add('correct');
            if (fb) {
              fb.style.display = 'block';
              fb.style.background = 'rgba(225, 29, 72, 0.15)';
              fb.style.color = '#e11d48';
              fb.textContent = 'Respuesta incorrecta. ' + qData.explanation;
            }
          }
        });
      });
    });

    /* ==========================================================================
       RENDERIZADO DE ECUACIONES MATEMÁTICAS CON KaTeX
       ========================================================================== */
    function initKaTeX() {
      if (typeof window !== 'undefined' && typeof window.renderMathInElement === 'function') {
        try {
          window.renderMathInElement(document.body, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '\\[', right: '\\]', display: true },
              { left: '\\(', right: '\\)', display: false },
              { left: '$', right: '$', display: false }
            ],
            throwOnError: false,
            ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
          });
          return true;
        } catch (e) {
          console.warn('KaTeX render error:', e);
        }
      }
      return false;
    }

    // Inicialización al cargar la ventana y el DOM
    window.addEventListener('DOMContentLoaded', () => {
      isInitialized = true;
      initKaTeX();
      updateStep(0);
    });

    window.addEventListener('load', () => {
      isInitialized = true;
      initKaTeX();
      updateStep(0);
      renderAllCanvases();
    });

    // Intervalo de reintento para KaTeX (en caso de carga asíncrona desde CDN)
    let katexAttempts = 0;
    const katexTimer = setInterval(() => {
      katexAttempts++;
      if (initKaTeX() || katexAttempts > 30) {
        clearInterval(katexTimer);
      }
    }, 120);
  </script>
</body>
</html>
'''

# Reemplazamos el marcador de datos con el JSON real de simulación
final_html = template_raw.replace("/*MVLEM_JSON_DATA*/", json_str)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"HTML generado exitosamente en: {html_path}")
print(f"Tamaño: {os.path.getsize(html_path)} bytes")
