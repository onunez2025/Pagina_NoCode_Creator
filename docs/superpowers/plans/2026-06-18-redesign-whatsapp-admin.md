# NoCode Creator — Rediseño + WhatsApp + Admin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rediseñar completamente la landing page con identidad azul de marca, agregar notificación automática a WhatsApp del admin cuando llega un lead, y crear un panel `/admin` para gestionar el pipeline de clientes.

**Architecture:** Remapear los tokens de color de Tailwind (`brand-cyan` → `#38bdf8`, `brand-indigo` → `#3b82f6`) para propagar el nuevo esquema de color a todo el HTML existente sin tocar Alpine.js. Reescribir `neon.css` con nuevas variables CSS azules. Agregar 2 nuevas rutas FastAPI (`/admin` con HTTP Basic Auth, `PATCH /api/leads/{id}/status`) y una función de notificación Callmebot vía HTTP GET.

**Tech Stack:** FastAPI · Jinja2 · Alpine.js · Tailwind CSS (CDN Play) · JetBrains Mono · Space Grotesk · Lucide Icons · Callmebot API (WhatsApp gratuito) · Supabase REST API · httpx

## Global Constraints

- Python backend: FastAPI en `main.py` — no crear archivos Python adicionales
- CSS: Mantener todos los nombres de clases CSS existentes (`.os-card`, `.os-cta`, etc.) — solo cambiar propiedades visuales
- Alpine.js: No modificar ninguna lógica Alpine.js — solo clases Tailwind de color/estilo
- Tailwind: Usar CDN Play (`https://cdn.tailwindcss.com`) — no hay build step
- Colores de marca: `brand-electric=#38bdf8`, `brand-blue=#3b82f6`, `brand-deep=#1e3a8a`, `brand-navy=#050c1a`
- Aliases Tailwind que persisten: `brand-cyan` → `#38bdf8`, `brand-indigo` → `#3b82f6`, `brand-dark` → `#050c1a`
- Servidor: `uvicorn main:app --reload --port 8000`
- El proyecto NO tiene test runner configurado — verificación es manual corriendo el servidor
- Variables de entorno en `.env` en la raíz del proyecto
- Windows: usar PowerShell para comandos, git con `windows.appendAtomically false`

---

## Mapa de archivos

| Acción | Archivo | Responsabilidad |
|---|---|---|
| Modificar | `static/css/neon.css` | Sistema de diseño CSS completo (reescritura) |
| Modificar | `templates/base.html` | Tipografía Space Grotesk, Tailwind config remap, header, footer, boot |
| Modificar | `templates/index.html` | Nuevo Hero, nueva sección "Lo que construimos", nueva sección "Cómo trabajamos", stats rediseñadas, rediseño visual de secciones existentes |
| Modificar | `templates/success.html` | Rediseño visual |
| Modificar | `main.py` | +`enviar_whatsapp_admin()`, +`GET /admin`, +`PATCH /api/leads/{id}/status` |
| Crear | `templates/admin.html` | Panel de gestión de leads |

---

## Task 1: Nueva identidad CSS + Remapeo de colores Tailwind

**Files:**
- Modify: `static/css/neon.css` (reescritura completa)
- Modify: `templates/base.html` (líneas 34-61: fonts + Tailwind config)

**Interfaces:**
- Produces: Variables CSS `--primary=#38bdf8`, `--secondary=#3b82f6`, `--bg=#050c1a`. Clases CSS `.os-card`, `.os-cta`, `.os-cta-ghost`, `.os-pill`, `.os-metric`, `.os-topbar`, `.boot-screen`, `.terminal-modal`, `.hero-mesh`, `.bento-card`, `.step-connector` disponibles para Tasks 2-6.

- [ ] **Step 1: Reemplazar neon.css completo**

Reemplazar el contenido COMPLETO de `static/css/neon.css` con:

```css
/* ==========================================================================
   NoCode Creator Design System — Blue Brand Identity
   ========================================================================== */

:root {
  --primary:      #38bdf8;
  --secondary:    #3b82f6;
  --deep:         #1e3a8a;
  --bg:           #050c1a;
  --surface:      #0d1f3c;
  --surface-2:    #0a1628;
  --text:         #f8fafc;
  --muted:        rgba(148, 163, 184, 0.7);
  --accent-green: #22c55e;
  --warn:         #f59e0b;
  --danger:       #ef4444;

  --card-bg:           rgba(13, 31, 60, 0.7);
  --card-bg-hover:     rgba(56, 189, 248, 0.05);
  --card-border:       rgba(255, 255, 255, 0.08);
  --card-border-hover: rgba(56, 189, 248, 0.4);

  --glow-primary:        0 8px 24px rgba(56, 189, 248, 0.25);
  --glow-primary-strong: 0 10px 32px rgba(56, 189, 248, 0.45);
  --glow-dot:            0 0 8px rgba(56, 189, 248, 0.7);
  --glow-green:          0 0 8px rgba(34, 197, 94, 0.7);
  --glow-warn:           0 0 6px rgba(245, 158, 11, 0.7);
  --glow-danger:         0 0 8px rgba(239, 68, 68, 0.55);
}

html {
  scroll-behavior: smooth;
  scroll-padding-top: 80px;
}

body {
  font-family: 'Space Grotesk', 'Inter', -apple-system, sans-serif;
  color: var(--text);
  background-color: var(--bg);
  background-image:
    radial-gradient(ellipse 800px 600px at 20% -5%, rgba(30, 58, 138, 0.35), transparent 60%),
    radial-gradient(ellipse 600px 500px at 90% 110%, rgba(59, 130, 246, 0.12), transparent 60%);
  background-attachment: fixed;
  line-height: 1.6;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

::selection {
  background: var(--primary);
  color: #000;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text);
}

code, .mono {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
}

/* ---- Eyebrows ---- */
.eyebrow {
  display: inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--primary);
  margin-bottom: 8px;
}
.eyebrow--muted { color: var(--muted); }
.eyebrow--warn  { color: var(--warn); }
.eyebrow--block::before {
  content: '█  ';
  color: var(--primary);
}
.eyebrow--block.eyebrow--muted::before { color: var(--muted); }

/* ---- Section head layout ---- */
.section-head {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.muted { color: var(--muted); }
.t-xs  { font-size: 10px; }

/* ---- Prompt / cursor ---- */
.prompt {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px;
  font-weight: 700;
  color: var(--muted);
}
.prompt::before { content: 'ncc@os:~$'; color: var(--primary); font-weight: 700; }

.cursor {
  display: inline-block;
  width: 0.5em;
  height: 0.92em;
  background: var(--primary);
  margin-left: 4px;
  vertical-align: -0.12em;
  box-shadow: 0 0 8px var(--primary);
  animation: blink 1.05s steps(1) infinite;
}
@keyframes blink {
  0%, 50%   { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* ---- OS Cards ---- */
.os-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  padding: 22px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.os-card:hover {
  border-color: var(--card-border-hover);
  background: var(--card-bg-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(56, 189, 248, 0.06);
}
.os-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  opacity: 0;
  transition: opacity 0.25s ease;
}
.os-card:hover::before { opacity: 1; }

/* ---- Bento Cards (new sections) ---- */
.bento-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 18px;
  padding: 28px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}
.bento-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 18px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.3), rgba(59, 130, 246, 0.1), transparent);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s ease;
}
.bento-card:hover::after { opacity: 1; }
.bento-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 16px 40px rgba(56, 189, 248, 0.08);
}

/* ---- Step connector (Cómo trabajamos) ---- */
.step-connector {
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(56, 189, 248, 0.3);
  font-size: 20px;
}

/* ---- Hero mesh background ---- */
.hero-mesh {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}
.hero-mesh::before {
  content: '';
  position: absolute;
  width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(30, 58, 138, 0.5) 0%, transparent 70%);
  top: -200px; left: -100px;
  border-radius: 50%;
  animation: mesh-pulse 8s ease-in-out infinite;
}
.hero-mesh::after {
  content: '';
  position: absolute;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
  bottom: -100px; right: -50px;
  border-radius: 50%;
  animation: mesh-pulse 10s ease-in-out infinite reverse;
}
@keyframes mesh-pulse {
  0%, 100% { transform: scale(1) translate(0, 0); opacity: 0.6; }
  50%       { transform: scale(1.1) translate(20px, -20px); opacity: 1; }
}

/* ---- Gradient text ---- */
.text-gradient-blue {
  background: linear-gradient(135deg, #38bdf8, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.text-gradient-cyan-indigo {
  background: linear-gradient(135deg, #38bdf8, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ---- Shimmer badge ---- */
.shimmer-badge {
  background: linear-gradient(
    90deg,
    rgba(56, 189, 248, 0.1) 0%,
    rgba(56, 189, 248, 0.2) 50%,
    rgba(56, 189, 248, 0.1) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

/* ---- Pills ---- */
.os-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  padding: 4px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 600;
  color: var(--muted);
}
.os-pill--primary  { color: var(--primary);      border-color: rgba(56, 189, 248, 0.3); }
.os-pill--secondary{ color: var(--secondary);    border-color: rgba(59, 130, 246, 0.3); }
.os-pill--warn     { color: var(--warn);         border-color: rgba(245, 158, 11, 0.3); }
.os-pill--green    { color: var(--accent-green); border-color: rgba(34, 197, 94, 0.3); }

/* ---- Metrics ---- */
.os-metric { display: flex; flex-direction: column; gap: 4px; }
.os-metric__value {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  font-size: 24px;
  color: var(--text);
  line-height: 1;
}
.os-metric__value--accent {
  color: var(--primary);
  text-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
}
.os-metric__label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--muted);
}

/* ---- Status dots ---- */
.os-dot {
  display: inline-block;
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: var(--glow-dot);
  flex-shrink: 0;
}
.os-dot--live   { animation: pulse-glow 2.4s ease-out infinite; }
.os-dot--green  { background: var(--accent-green); box-shadow: var(--glow-green); }
.os-dot--warn   { background: var(--warn); box-shadow: var(--glow-warn); }

@keyframes pulse-glow {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%      { opacity: 0.45; transform: scale(0.85); }
}

/* ---- CTAs ---- */
.os-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #000;
  border: none;
  border-radius: 10px;
  padding: 12px 24px;
  font-weight: 700;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  box-shadow: var(--glow-primary);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}
.os-cta:hover {
  transform: translateY(-2px);
  box-shadow: var(--glow-primary-strong);
  filter: brightness(1.1);
}
.os-cta:active { transform: translateY(0); }

.os-cta-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: transparent;
  color: var(--text);
  border: 1px solid var(--card-border);
  border-radius: 10px;
  padding: 12px 24px;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
}
.os-cta-ghost:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: rgba(56, 189, 248, 0.05);
}

/* ==========================================================================
   BOOT SCREEN
   ========================================================================== */
.boot-screen {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 24px;
  background: var(--bg);
  background-image: radial-gradient(ellipse 800px 600px at 50% 30%, rgba(30, 58, 138, 0.35), transparent 60%);
  font-family: 'JetBrains Mono', monospace;
  color: var(--text);
  transition: opacity 0.5s ease, visibility 0.5s;
}
.boot-screen.is-hidden {
  opacity: 0;
  pointer-events: none;
  visibility: hidden;
}

.boot-logo {
  font-family: 'JetBrains Mono', monospace;
  color: var(--primary);
  font-size: clamp(8px, 2.5vw, 12px);
  line-height: 1.1;
  white-space: pre;
  filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.5));
  animation: boot-glow 2.2s ease-in-out infinite;
}
@keyframes boot-glow {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.4)); }
  50%      { filter: drop-shadow(0 0 20px rgba(56, 189, 248, 0.7)); }
}

.boot-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  font-size: clamp(26px, 6vw, 36px);
  margin-top: 4px;
  letter-spacing: -0.03em;
}
.boot-title__accent { color: var(--primary); }
.boot-meta {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--muted);
}

.boot-progress {
  width: min(340px, 80vw);
  height: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 8px;
}
.boot-progress__fill {
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--deep), var(--primary));
  border-radius: 999px;
  box-shadow: 0 0 12px var(--primary);
  transition: width 0.15s ease-out;
}
.boot-pct { font-size: 11px; font-weight: 700; color: var(--primary); letter-spacing: 0.06em; }

.boot-log {
  width: min(520px, 92vw);
  margin-top: 6px;
  font-size: 11px;
  color: var(--muted);
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 130px;
}
.boot-log__line {
  opacity: 0;
  animation: boot-line-in 0.25s ease-out forwards;
  display: flex;
  align-items: baseline;
  gap: 8px;
}
@keyframes boot-line-in {
  from { opacity: 0; transform: translateX(-6px); }
  to   { opacity: 0.6; transform: translateX(0); }
}
.boot-log__line.is-current { opacity: 1; }
.boot-log__cur { color: var(--text); }
.boot-log__ok  { color: var(--primary); }
.boot-log__done {
  color: var(--bg);
  background: var(--primary);
  padding: 0 6px;
  border-radius: 3px;
  box-shadow: 0 0 8px var(--primary);
}
.boot-log__warn { color: var(--warn); }
.boot-log__pending { color: var(--primary); font-weight: 700; display: inline-block; width: 18px; }
.boot-log__pending::after {
  content: '...';
  animation: boot-dots 1s steps(4, end) infinite;
}
@keyframes boot-dots {
  0%  { content: ''; }  25% { content: '.'; }
  50% { content: '..'; } 75%  { content: '...'; }
}

.boot-screen::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.5) 100%),
    repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(0,0,0,0.12) 2px, rgba(0,0,0,0.12) 3px);
  pointer-events: none;
  opacity: 0.6;
}
.boot-screen::before {
  content: '';
  position: absolute;
  left: 0; right: 0; top: 0;
  height: 2px;
  background: linear-gradient(to bottom, transparent, var(--primary), transparent);
  opacity: 0.4;
  pointer-events: none;
  animation: boot-scanline 6s linear infinite;
}
@keyframes boot-scanline {
  from { transform: translateY(-10px); }
  to   { transform: translateY(100vh); }
}

.boot-skip {
  position: absolute;
  top: 20px; right: 20px;
  background: transparent;
  border: 1px solid var(--card-border);
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  z-index: 10;
  cursor: pointer;
}
.boot-skip:hover { color: var(--primary); border-color: var(--primary); }

/* ==========================================================================
   DESKTOP SHELL
   ========================================================================== */
.os-desktop {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 1000px 600px at 20% 0%, rgba(30, 58, 138, 0.25), transparent 60%),
    radial-gradient(ellipse 700px 500px at 90% 100%, rgba(59, 130, 246, 0.08), transparent 60%);
  background-attachment: fixed;
  opacity: 0;
  transition: opacity 0.4s ease;
}
.os-desktop.is-ready { opacity: 1; }
.os-desktop::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(56, 189, 248, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56, 189, 248, 0.025) 1px, transparent 1px);
  background-size: 40px 40px;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 85%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 40%, transparent 85%);
  opacity: 0.5;
}

/* ---- Top bar ---- */
.os-topbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 50px;
  padding: 0 24px;
  background: rgba(5, 12, 26, 0.85);
  border-bottom: 1px solid rgba(56, 189, 248, 0.1);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.os-topbar__left { display: flex; align-items: center; gap: 12px; }
.os-topbar__brand {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 14px;
  color: var(--text);
  text-decoration: none;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 8px;
}
.os-topbar__brand:hover { color: var(--primary); }
.os-topbar__right { display: flex; align-items: center; gap: 16px; }

.os-tray__seg {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
}
.os-tray__seg--hide-mobile { display: none; }
@media (min-width: 640px) {
  .os-tray__seg--hide-mobile { display: inline-flex; }
}

/* ==========================================================================
   TERMINAL MODAL
   ========================================================================== */
.terminal-modal {
  position: fixed;
  inset: 0;
  z-index: 90;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s;
}
.terminal-modal.is-open { opacity: 1; visibility: visible; }
.terminal-modal__window {
  width: min(720px, 100%);
  height: min(480px, 80vh);
  background: rgba(5, 12, 26, 0.97);
  border: 1px solid rgba(56, 189, 248, 0.3);
  border-radius: 14px;
  box-shadow: 0 20px 50px rgba(56, 189, 248, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: scale(0.96);
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.terminal-modal.is-open .terminal-modal__window { transform: scale(1); }
.terminal-modal__chrome {
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  height: 40px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  user-select: none;
}
.terminal-modal__chrome__left {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
}
.terminal-modal__close {
  background: transparent;
  border: 0;
  padding: 4px;
  color: var(--muted);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.15s ease;
  cursor: pointer;
}
.terminal-modal__close:hover { color: var(--danger); background: rgba(239, 68, 68, 0.1); }
.terminal-modal__body {
  flex: 1 1 auto;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.term {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--text);
}
.term__output {
  flex: 1 1 auto;
  overflow-y: auto;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  scroll-behavior: smooth;
}
.term__line { white-space: pre-wrap; }
.term__line--prompt { font-weight: 700; color: var(--muted); }
.term__line--prompt::before { content: 'ncc@os:~$ '; color: var(--primary); }
.term__line--err  { color: var(--danger); }
.term__line--info { color: var(--primary); }
.term__line--out  { color: #e2e8f0; }
.term__input-line {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  border-top: 1px solid rgba(255, 255, 255, 0.03);
  padding-top: 10px;
}
.term__prompt { color: var(--primary); font-weight: 700; flex-shrink: 0; }
.term__input {
  flex: 1 1 auto;
  background: transparent;
  border: 0;
  outline: 0;
  font-family: inherit;
  font-size: inherit;
  color: var(--text);
  caret-color: var(--primary);
}
.motd {
  background: rgba(56, 189, 248, 0.04);
  border: 1px solid rgba(56, 189, 248, 0.15);
  border-radius: 8px;
  padding: 12px;
  color: var(--muted);
}

/* ==========================================================================
   MISC UTILITIES
   ========================================================================== */
.glow-backdrop {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  z-index: -10;
  pointer-events: none;
}
.glow-backdrop--cyan {
  background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
}
.glow-backdrop--indigo {
  background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, transparent 70%);
}

.tech-grid-overlay {
  background-size: 30px 30px;
  background-image:
    linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
}

.os-glass-panel {
  background: rgba(13, 31, 60, 0.65);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.os-animate-float {
  animation: os-float 6s ease-in-out infinite;
}
@keyframes os-float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-10px); }
}

/* Typing animation (chatbot) */
.typing-dot {
  width: 6px; height: 6px;
  background: var(--primary);
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30%            { transform: translateY(-6px); opacity: 1; }
}

.no-scrollbar::-webkit-scrollbar { display: none !important; }
.no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
.os-no-scrollbar::-webkit-scrollbar { display: none !important; }
.os-no-scrollbar { -ms-overflow-style: none !important; scrollbar-width: none !important; }
```

- [ ] **Step 2: Actualizar Tailwind config y fuente en base.html**

En `templates/base.html`, reemplazar el bloque de Google Fonts (líneas 35-37) con:

```html
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
```

Reemplazar el bloque `<script>tailwind.config = {...}</script>` (líneas 44-61) con:

```html
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            navy:     '#050c1a',
                            deep:     '#1e3a8a',
                            blue:     '#3b82f6',
                            electric: '#38bdf8',
                            dark:     '#050c1a',
                            cyan:     '#38bdf8',
                            indigo:   '#3b82f6',
                            amber:    '#f59e0b',
                        }
                    },
                    fontFamily: {
                        sans: ['Space Grotesk', 'Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }
                }
            }
        }
    </script>
```

- [ ] **Step 3: Iniciar servidor y verificar cambio de colores**

```powershell
cd "C:\Users\onunez\OneDrive - MT INDUSTRIAL S.A.C\Escritorio\ProyectosNoCodeCreator\Pagina_NoCode_Creator"
.\.venv\Scripts\uvicorn main:app --reload --port 8000
```

Abrir `http://127.0.0.1:8000` en el navegador. Verificar:
- Fondo: navy oscuro `#050c1a` (antes slate muy oscuro)
- Acentos cyan ahora son azul eléctrico `#38bdf8`
- Botones CTA tienen gradiente azul (antes cyan sólido)
- Boot screen en azul eléctrico
- Tipografía de headings: Space Grotesk (más geométrica/pesada)

- [ ] **Step 4: Commit**

```powershell
git add static/css/neon.css templates/base.html
git commit -m "design: remap brand colors to blue identity and add Space Grotesk font"
```

---

## Task 2: Nuevo Hero + Sección "Lo que construimos"

**Files:**
- Modify: `templates/index.html` (reemplazar sección Hero existente líneas 107-199, agregar nueva sección después)

**Interfaces:**
- Consumes: `.hero-mesh`, `.bento-card`, `.shimmer-badge`, `.os-cta`, `.os-cta-ghost`, `.os-animate-float`, `.os-glass-panel` de Task 1
- Produces: Sección `#servicios` conservada como anchor, nueva sección `#lo-que-construimos`

- [ ] **Step 1: Reemplazar sección Hero (líneas 107-199 del index.html)**

Reemplazar todo el bloque `<!-- ==================== ── █ HERO / GREETING SECTION ── ====================  -->` hasta el cierre de su `</section>` con:

```html
    <!-- ==================== HERO ==================== -->
    <section class="relative min-h-[90vh] flex items-center overflow-hidden">
        <!-- Mesh background -->
        <div class="hero-mesh"></div>
        <!-- Grid overlay -->
        <div class="absolute inset-0 tech-grid-overlay opacity-20 pointer-events-none"></div>

        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 flex flex-col md:flex-row items-center justify-between gap-16 relative z-10">
            <!-- Text -->
            <div class="flex-1 space-y-8 text-center md:text-left">
                <!-- Badge -->
                <div class="inline-flex items-center space-x-2 shimmer-badge border border-brand-electric/20 px-4 py-2 rounded-full text-brand-electric text-xs font-mono tracking-wider">
                    <span class="flex h-2 w-2 relative">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-electric opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-brand-electric"></span>
                    </span>
                    <span>IA + LOW-CODE · LIMA, PERÚ</span>
                </div>

                <!-- Headline -->
                <div class="space-y-4">
                    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.05] text-white">
                        Construimos<br>
                        <span class="text-gradient-blue">cualquier plataforma</span><br>
                        digital que imagines
                    </h1>
                    <p class="text-slate-400 text-base sm:text-lg max-w-xl mx-auto md:mx-0 leading-relaxed">
                        Páginas web, apps móviles, sistemas ERP o tiendas online — las creamos con IA y Low-Code en tiempo récord. <strong class="text-white">Desde S/ 500.</strong> Soporte local en Lima.
                    </p>
                </div>

                <!-- CTAs -->
                <div class="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4">
                    <a href="#cotizador" class="w-full sm:w-auto os-cta font-mono uppercase tracking-wider text-sm">
                        <i data-lucide="calculator" class="w-4 h-4"></i>
                        Cotizar mi proyecto
                    </a>
                    <a href="#lo-que-construimos" class="w-full sm:w-auto os-cta-ghost font-mono uppercase tracking-wider text-sm">
                        Ver lo que hacemos
                        <i data-lucide="arrow-down" class="w-4 h-4"></i>
                    </a>
                </div>

                <!-- Social proof micro -->
                <div class="flex items-center justify-center md:justify-start gap-6 pt-2 font-mono text-xs text-slate-500">
                    <span class="flex items-center gap-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-electric"></i>85% más barato</span>
                    <span class="flex items-center gap-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-electric"></i>Entrega acelerada</span>
                    <span class="flex items-center gap-1.5"><i data-lucide="check-circle" class="w-3.5 h-3.5 text-brand-electric"></i>Soporte Lima</span>
                </div>
            </div>

            <!-- Browser mockup -->
            <div class="flex-1 w-full max-w-lg md:max-w-none relative os-animate-float">
                <div class="absolute -inset-2 rounded-2xl bg-gradient-to-tr from-brand-deep to-brand-blue opacity-20 blur-3xl -z-10"></div>
                <div class="os-glass-panel rounded-2xl p-2 shadow-2xl border border-brand-electric/15">
                    <div class="bg-brand-navy/90 rounded-xl overflow-hidden border border-white/5 relative">
                        <div class="bg-brand-navy px-4 py-2 flex items-center justify-between border-b border-white/5 font-mono text-[10px]">
                            <div class="flex space-x-1.5">
                                <span class="w-2.5 h-2.5 rounded-full bg-red-500/60"></span>
                                <span class="w-2.5 h-2.5 rounded-full bg-yellow-500/60"></span>
                                <span class="w-2.5 h-2.5 rounded-full bg-green-500/60"></span>
                            </div>
                            <div class="bg-brand-deep/80 text-slate-500 px-3 py-0.5 rounded border border-white/5 w-1/2 truncate text-center">
                                nocodecreator.pe/demo
                            </div>
                            <div class="text-brand-electric font-bold">200 OK</div>
                        </div>
                        <img
                            src="/static/images/dashboard_preview.png"
                            alt="Panel creado con IA"
                            class="w-full h-auto object-cover border-b border-white/5 opacity-85"
                            onerror="this.src='https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80'"
                        />
                        <div class="absolute bottom-4 left-4 os-glass-panel rounded-xl p-3 shadow-lg border border-brand-electric/20 flex items-center space-x-3">
                            <div class="w-7 h-7 rounded-lg bg-brand-electric/20 flex items-center justify-center text-brand-electric">
                                <i data-lucide="zap" class="w-4 h-4"></i>
                            </div>
                            <div class="font-mono text-left">
                                <p class="text-[9px] text-slate-500 leading-none">VELOCIDAD</p>
                                <p class="text-xs font-bold text-white mt-1">Despliegue Acelerado</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
```

- [ ] **Step 2: Agregar sección "Lo que construimos" después del Hero y antes del Stats strip**

Insertar inmediatamente después del cierre `</section>` del Hero y antes del div con `aria-label="Track record"`:

```html
    <!-- ==================== LO QUE CONSTRUIMOS ==================== -->
    <section id="lo-que-construimos" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative">
        <div class="section-head mb-12 text-center">
            <span class="eyebrow eyebrow--block">CAPACIDADES</span>
            <h2 class="text-3xl sm:text-4xl font-extrabold text-white mt-3">Construimos cualquier tipo de plataforma</h2>
            <p class="text-slate-400 text-sm mt-3 max-w-xl mx-auto">Sin importar tu industria o tamaño, si lo imaginas, lo construimos con IA y Low-Code.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <!-- Card 1: Páginas web -->
            <div class="bento-card group">
                <div class="flex items-start gap-4 mb-5">
                    <div class="w-12 h-12 rounded-xl bg-brand-electric/10 border border-brand-electric/20 flex items-center justify-center text-brand-electric flex-shrink-0">
                        <i data-lucide="globe" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-white">Páginas Web & Landings</h3>
                        <p class="text-slate-400 text-sm mt-1 leading-relaxed">Sitios institucionales, portfolios, blogs y landing pages de producto que convierten visitas en clientes.</p>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2 mt-auto">
                    <span class="os-pill os-pill--primary font-mono text-[9px]">LANDING PAGE</span>
                    <span class="os-pill font-mono text-[9px]">PORTAFOLIO</span>
                    <span class="os-pill font-mono text-[9px]">BLOG CORPORATIVO</span>
                </div>
            </div>

            <!-- Card 2: Apps móviles -->
            <div class="bento-card group">
                <div class="flex items-start gap-4 mb-5">
                    <div class="w-12 h-12 rounded-xl bg-brand-blue/10 border border-brand-blue/20 flex items-center justify-center text-brand-blue flex-shrink-0">
                        <i data-lucide="smartphone" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-white">Apps Móviles iOS & Android</h3>
                        <p class="text-slate-400 text-sm mt-1 leading-relaxed">Aplicaciones híbridas para cualquier dispositivo: apps de pedidos, reservas, entregas y más.</p>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2 mt-auto">
                    <span class="os-pill os-pill--secondary font-mono text-[9px]">iOS & ANDROID</span>
                    <span class="os-pill font-mono text-[9px]">REACT NATIVE</span>
                    <span class="os-pill font-mono text-[9px]">FLUTTER</span>
                </div>
            </div>

            <!-- Card 3: ERP / CRM -->
            <div class="bento-card group">
                <div class="flex items-start gap-4 mb-5">
                    <div class="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
                        <i data-lucide="layout-dashboard" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-white">Sistemas ERP & CRM</h3>
                        <p class="text-slate-400 text-sm mt-1 leading-relaxed">Paneles administrativos, control de inventario, POS, reportes con IA y dashboards de gestión completos.</p>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2 mt-auto">
                    <span class="os-pill os-pill--green font-mono text-[9px]">POS & CAJA</span>
                    <span class="os-pill font-mono text-[9px]">INVENTARIO</span>
                    <span class="os-pill font-mono text-[9px]">DASHBOARD AI</span>
                </div>
            </div>

            <!-- Card 4: E-commerce -->
            <div class="bento-card group">
                <div class="flex items-start gap-4 mb-5">
                    <div class="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 flex-shrink-0">
                        <i data-lucide="shopping-cart" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-white">E-commerce & Tiendas Online</h3>
                        <p class="text-slate-400 text-sm mt-1 leading-relaxed">Tiendas con carrito, catálogo, pasarelas Yape/Plin/Culqi y facturación electrónica peruana integrada.</p>
                    </div>
                </div>
                <div class="flex flex-wrap gap-2 mt-auto">
                    <span class="os-pill os-pill--warn font-mono text-[9px]">YAPE / PLIN</span>
                    <span class="os-pill font-mono text-[9px]">CULQI / NIUBIZ</span>
                    <span class="os-pill font-mono text-[9px]">FACTURA ELECTRÓNICA</span>
                </div>
            </div>
        </div>
    </section>
```

- [ ] **Step 3: Verificar en navegador**

Con el servidor corriendo (`http://127.0.0.1:8000`):
- Hero ocupa casi toda la pantalla con fondo mesh de gradientes azules
- Headline dice "Construimos cualquier plataforma digital que imagines"
- Sección "Lo que construimos" muestra 4 cards en grid 2x2
- Cada card tiene ícono, título, descripción y tags
- El botón "Ver lo que hacemos" hace scroll suave a la sección

- [ ] **Step 4: Commit**

```powershell
git add templates/index.html
git commit -m "feat: add new hero section and Lo que construimos bento grid"
```

---

## Task 3: Sección "Cómo trabajamos" + Stats rediseñados

**Files:**
- Modify: `templates/index.html` (insertar sección "Cómo trabajamos" antes de `#servicios`, reemplazar el div de stats)

**Interfaces:**
- Consumes: `.bento-card`, `.os-metric` de Task 1
- Produces: Sección `#como-trabajamos`, stats actualizados

- [ ] **Step 1: Insertar "Cómo trabajamos" antes de la sección `#servicios`**

Insertar este bloque entre la sección "Lo que construimos" y la sección `id="servicios"`:

```html
    <!-- ==================== CÓMO TRABAJAMOS ==================== -->
    <section id="como-trabajamos" class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative">
        <div class="section-head mb-12 text-center">
            <span class="eyebrow eyebrow--block">PROCESO</span>
            <h2 class="text-3xl font-extrabold text-white mt-3">Simple como 1, 2, 3</h2>
        </div>

        <div class="flex flex-col md:flex-row items-center justify-center gap-0 md:gap-0">
            <!-- Step 1 -->
            <div class="flex-1 bento-card text-center mx-2 my-2 md:my-0">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-deep to-brand-blue flex items-center justify-center mx-auto mb-4 shadow-lg shadow-brand-blue/20">
                    <i data-lucide="calculator" class="w-7 h-7 text-white"></i>
                </div>
                <div class="font-mono text-brand-electric text-xs font-bold mb-2 tracking-widest">PASO 01</div>
                <h3 class="text-lg font-bold text-white mb-2">Cotizas</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Usa nuestro cotizador AI o escríbenos al chat. En minutos tienes un presupuesto transparente.</p>
            </div>

            <!-- Connector -->
            <div class="hidden md:flex step-connector px-2">
                <i data-lucide="arrow-right" class="w-6 h-6"></i>
            </div>
            <div class="md:hidden step-connector py-2">
                <i data-lucide="arrow-down" class="w-6 h-6"></i>
            </div>

            <!-- Step 2 -->
            <div class="flex-1 bento-card text-center mx-2 my-2 md:my-0">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-blue to-brand-electric flex items-center justify-center mx-auto mb-4 shadow-lg shadow-brand-electric/20">
                    <i data-lucide="brain-circuit" class="w-7 h-7 text-white"></i>
                </div>
                <div class="font-mono text-brand-electric text-xs font-bold mb-2 tracking-widest">PASO 02</div>
                <h3 class="text-lg font-bold text-white mb-2">Diseñamos</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Nuestro equipo usa IA y Low-Code para construir tu plataforma en tiempo récord, con calidad premium.</p>
            </div>

            <!-- Connector -->
            <div class="hidden md:flex step-connector px-2">
                <i data-lucide="arrow-right" class="w-6 h-6"></i>
            </div>
            <div class="md:hidden step-connector py-2">
                <i data-lucide="arrow-down" class="w-6 h-6"></i>
            </div>

            <!-- Step 3 -->
            <div class="flex-1 bento-card text-center mx-2 my-2 md:my-0">
                <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-brand-electric to-emerald-400 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-emerald-400/20">
                    <i data-lucide="rocket" class="w-7 h-7 text-white"></i>
                </div>
                <div class="font-mono text-brand-electric text-xs font-bold mb-2 tracking-widest">PASO 03</div>
                <h3 class="text-lg font-bold text-white mb-2">Entregamos</h3>
                <p class="text-slate-400 text-sm leading-relaxed">Recibes tu plataforma lista y funcional. Con 90 días de soporte local por WhatsApp en Lima.</p>
            </div>
        </div>
    </section>
```

- [ ] **Step 2: Reemplazar el div de Stats strip**

Reemplazar el bloque `<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8" aria-label="Track record">` completo (hasta su `</div>` de cierre) con:

```html
    <!-- ==================== STATS ==================== -->
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8" aria-label="Stats de valor">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 rounded-2xl bg-brand-deep/20 border border-brand-electric/10">
            <div class="os-metric">
                <span class="os-metric__value os-metric__value--accent">85%</span>
                <span class="os-metric__label">Ahorro vs agencia</span>
            </div>
            <div class="os-metric border-t md:border-t-0 md:border-l border-white/5 pt-4 md:pt-0 md:pl-6">
                <span class="os-metric__value">S/ 500</span>
                <span class="os-metric__label">Precio base</span>
            </div>
            <div class="os-metric border-t md:border-t-0 md:border-l border-white/5 pt-4 md:pt-0 md:pl-6">
                <span class="os-metric__value os-metric__value--accent">90 días</span>
                <span class="os-metric__label">Soporte incluido</span>
            </div>
            <div class="os-metric border-t md:border-t-0 md:border-l border-white/5 pt-4 md:pt-0 md:pl-6">
                <span class="os-metric__value">GRATIS</span>
                <span class="os-metric__label">Primer mes hosting</span>
            </div>
        </div>
    </div>
```

- [ ] **Step 3: Verificar en navegador**

- Sección "Cómo trabajamos" muestra 3 cards con pasos conectados por flechas
- En móvil las flechas apuntan hacia abajo
- Stats muestran: 85%, S/ 500, 90 días, GRATIS

- [ ] **Step 4: Commit**

```powershell
git add templates/index.html
git commit -m "feat: add Como trabajamos section and update stats strip"
```

---

## Task 4: Rediseño visual de secciones existentes (cotizador, showcase, comparativa, wizard, FAQ)

**Files:**
- Modify: `templates/index.html` — solo cambios de clases CSS/Tailwind en las secciones existentes, sin tocar lógica Alpine.js

**Interfaces:**
- Consumes: Todas las clases de Task 1. Las clases `brand-cyan` y `brand-indigo` ya tienen los nuevos colores por el remapeo de Task 1.
- Produces: Todas las secciones existentes con nuevo estilo visual coherente

- [ ] **Step 1: Actualizar sección Capacidades (`id="servicios"`)**

En la sección `id="servicios"`, reemplazar el eyebrow y el subtítulo:

```html
        <div class="section-head mb-12">
            <span class="eyebrow eyebrow--block">CAPACIDADES TÉCNICAS</span>
            <span class="mono muted t-xs">4 ESPECIALIDADES CORE</span>
        </div>
```

- [ ] **Step 2: Actualizar sección Cotizador (`id="cotizador"`)**

En el `<div class="absolute inset-0 ...">` que es el glow de fondo del cotizador, cambiar de `bg-brand-cyan/5` a `bg-brand-deep/30`:

```html
        <div class="absolute inset-0 bg-brand-deep/30 rounded-3xl blur-3xl -z-10"></div>
```

En el `<div class="absolute top-0 left-0 w-full bg-gradient-to-r from-brand-cyan to-brand-indigo h-[4px]">` (Chrome Header Ribbon del summary card), es correcto tal cual — los colores remapeados ya lo actualizan.

- [ ] **Step 3: Actualizar sección Plataformas Activas (`id="prototipos"`)**

Solo actualizar el eyebrow:

```html
        <div class="section-head mb-12">
            <span class="eyebrow eyebrow--block">PLATAFORMAS DEMO</span>
            <span class="mono muted t-xs">3 PROTOTIPOS INTERACTIVOS</span>
        </div>
```

- [ ] **Step 4: Actualizar sección Comparativa (`id="beneficios"`)**

Solo actualizar el eyebrow:

```html
        <div class="section-head mb-12">
            <span class="eyebrow eyebrow--block">POR QUÉ ELEGIRNOS</span>
            <span class="mono muted t-xs">COMPARATIVA DE VALOR</span>
        </div>
```

En el encabezado de la tabla, la columna de NoCode Creator dice "No-Code-Creator (IA)". Actualizar a:

```html
                            <th class="p-5 text-brand-cyan bg-brand-cyan/5 border-x border-white/5">NoCode Creator + IA</th>
```

- [ ] **Step 5: Actualizar sección Wizard (`id="leads-wizard"`)**

Actualizar el eyebrow y subtítulo:

```html
        <div class="section-head mb-12">
            <span class="eyebrow eyebrow--block">SOLICITAR PROYECTO</span>
            <span class="mono muted t-xs">3 PASOS · 2 MINUTOS</span>
        </div>
        <div class="text-center space-y-3 max-w-xl mx-auto mb-12">
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Inicia tu Proyecto Digital</h2>
            <p class="text-slate-400 text-sm font-mono">Cuéntanos qué necesitas. Un asesor en Lima te contacta por WhatsApp en menos de 24 horas.</p>
        </div>
```

- [ ] **Step 6: Actualizar sección FAQ (`id="faq"`)**

Actualizar el eyebrow:

```html
        <div class="section-head mb-12">
            <span class="eyebrow eyebrow--block">PREGUNTAS FRECUENTES</span>
            <span class="mono muted t-xs">LO MÁS CONSULTADO</span>
        </div>
```

- [ ] **Step 7: Actualizar sección Filosofía (`id="ethos"`)**

Actualizar el eyebrow:

```html
        <div class="section-head mb-8">
            <span class="eyebrow eyebrow--block">NUESTRA FILOSOFÍA</span>
        </div>
```

- [ ] **Step 8: Verificar todo en navegador**

Con el servidor corriendo: hacer scroll completo por la página verificando que todas las secciones tienen el nuevo estilo azul coherente y el cotizador interactivo sigue funcionando (seleccionar rubro, marcar módulos, ver precio cambiar).

- [ ] **Step 9: Commit**

```powershell
git add templates/index.html
git commit -m "design: update eyebrows and visual consistency across all existing sections"
```

---

## Task 5: Rediseño de success.html

**Files:**
- Modify: `templates/success.html` (reescritura completa del bloque content)

**Interfaces:**
- Consumes: `.os-card`, `.os-cta`, `.bento-card`, `.text-gradient-blue` de Task 1. Variables Jinja2: `{{ nombre }}`, `{{ rubro }}`, `{{ empresa }}`

- [ ] **Step 1: Reemplazar contenido de success.html**

Reemplazar el contenido COMPLETO del archivo `templates/success.html` con:

```html
{% extends "base.html" %}

{% block content %}
<section class="relative min-h-[85vh] flex items-center justify-center overflow-hidden">
    <div class="hero-mesh"></div>
    <div class="absolute inset-0 tech-grid-overlay opacity-10 pointer-events-none"></div>

    <div class="max-w-2xl mx-auto px-4 sm:px-6 py-16 relative z-10 w-full">
        <div class="bento-card p-8 md:p-12 text-center">
            <!-- Animated check -->
            <div class="w-20 h-20 rounded-full bg-gradient-to-tr from-brand-deep to-brand-electric flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-brand-electric/25">
                <i data-lucide="check" class="w-10 h-10 text-white stroke-[2.5]"></i>
            </div>

            <!-- Greeting -->
            <div class="font-mono text-brand-electric text-xs font-bold tracking-widest mb-3">SOLICITUD REGISTRADA ✓</div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-white mb-4">
                ¡Listo, <span class="text-gradient-blue">{{ nombre }}</span>!
            </h1>
            <p class="text-slate-400 text-sm max-w-md mx-auto mb-8 leading-relaxed">
                Recibimos tu solicitud para el rubro de <strong class="text-brand-electric">{{ rubro }}</strong>{% if empresa and empresa != 'No especificado' %} de <strong class="text-white">{{ empresa }}</strong>{% endif %}. Un asesor en Lima se contactará contigo muy pronto.
            </p>

            <!-- Status grid -->
            <div class="grid grid-cols-2 gap-4 max-w-sm mx-auto mb-8 text-left">
                <div class="bg-brand-deep/30 border border-brand-electric/10 rounded-xl p-4 font-mono">
                    <p class="text-[9px] text-slate-500 uppercase tracking-widest font-bold mb-1">Estado</p>
                    <p class="text-brand-electric font-bold text-sm flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full bg-brand-electric animate-pulse"></span>
                        Asesor asignado
                    </p>
                </div>
                <div class="bg-brand-deep/30 border border-brand-electric/10 rounded-xl p-4 font-mono">
                    <p class="text-[9px] text-slate-500 uppercase tracking-widest font-bold mb-1">Respuesta</p>
                    <p class="text-white font-bold text-sm">Menos de 24h</p>
                </div>
            </div>

            <!-- CTAs -->
            <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
                <a
                    href="https://wa.me/51960560064?text=Hola%20NoCode%20Creator,%20acabo%20de%20registrar%20mi%20solicitud.%20Soy%20{{ nombre | urlencode }}%20del%20rubro%20{{ rubro | urlencode }}."
                    target="_blank"
                    class="os-cta font-mono uppercase tracking-wider text-sm w-full sm:w-auto justify-center"
                >
                    <i data-lucide="message-square" class="w-4 h-4"></i>
                    Acelerar por WhatsApp
                </a>
                <a href="/" class="os-cta-ghost font-mono uppercase tracking-wider text-sm w-full sm:w-auto justify-center">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    Volver al inicio
                </a>
            </div>
        </div>
    </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Verificar**

Navegar a `http://127.0.0.1:8000/success?nombre=Juan&rubro=Restaurante&empresa=La%20Buena%20Mesa` y verificar que la página muestra el diseño nuevo con el nombre y rubro interpolados correctamente.

- [ ] **Step 3: Commit**

```powershell
git add templates/success.html
git commit -m "design: rewrite success page with new blue brand identity"
```

---

## Task 6: Notificación WhatsApp al Admin (Callmebot)

**Files:**
- Modify: `main.py` (agregar función `enviar_whatsapp_admin` y llamarla en `/contact`)

**Interfaces:**
- Consumes: Variables de entorno `CALLMEBOT_PHONE`, `CALLMEBOT_APIKEY`. `httpx.AsyncClient` ya importado.
- Produces: Función `enviar_whatsapp_admin(lead_data: dict)` disponible en el scope de `main.py`

- [ ] **Step 1: Agregar import de urllib.parse en main.py**

Al inicio de `main.py`, agregar `urllib.parse` al bloque de imports existente. Reemplazar la línea `import httpx` con:

```python
import httpx
import urllib.parse
```

- [ ] **Step 2: Agregar función enviar_whatsapp_admin en main.py**

Insertar esta función después de la función `enviar_correo_notificacion` (después de su `return False` al final), antes del decorador `@app.get("/")`:

```python
async def enviar_whatsapp_admin(lead_data: dict):
    """Envía notificación instantánea al WhatsApp del admin via Callmebot (gratuito)."""
    phone = os.getenv("CALLMEBOT_PHONE")
    apikey = os.getenv("CALLMEBOT_APIKEY")
    if not phone or not apikey:
        print("Advertencia: CALLMEBOT_PHONE o CALLMEBOT_APIKEY no configurados. Notificación WhatsApp omitida.")
        return

    problema_corto = str(lead_data.get("problema", ""))[:100]
    mensaje = (
        f"⚡ NUEVO LEAD - NoCode Creator\n\n"
        f"👤 {lead_data.get('nombre')}\n"
        f"🏢 {lead_data.get('empresa', '-')}\n"
        f"📱 +51{lead_data.get('telefono')}\n"
        f"📧 {lead_data.get('correo')}\n"
        f"🏷️ Rubro: {lead_data.get('rubro')}\n"
        f"💰 Cotización: {lead_data.get('costo_estimado')}\n"
        f"📝 {problema_corto}\n\n"
        f"👉 Responder: wa.me/51{lead_data.get('telefono')}"
    )
    encoded = urllib.parse.quote(mensaje)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded}&apikey={apikey}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=8.0)
            if response.status_code == 200:
                print("Éxito: Notificación WhatsApp enviada al admin via Callmebot.")
            else:
                print(f"Error Callmebot (Status {response.status_code}): {response.text[:100]}")
    except Exception as e:
        print(f"Excepción al enviar WhatsApp via Callmebot: {str(e)}")
```

- [ ] **Step 3: Agregar la llamada a enviar_whatsapp_admin en el handler /contact**

En la función `handle_contact`, después de la línea `background_tasks.add_task(enviar_correo_notificacion, lead_data)`, agregar:

```python
    background_tasks.add_task(enviar_whatsapp_admin, lead_data)
```

El bloque de background tasks debe quedar así:

```python
    # 3. Enviar notificaciones de forma no bloqueante
    background_tasks.add_task(enviar_correo_notificacion, lead_data)
    background_tasks.add_task(enviar_whatsapp_admin, lead_data)
```

- [ ] **Step 4: Configurar variables de entorno**

Abrir `.env` en la raíz del proyecto y agregar las dos líneas nuevas:

```
CALLMEBOT_PHONE=51960560064
CALLMEBOT_APIKEY=TU_APIKEY_AQUI
```

**Importante — cómo obtener tu CALLMEBOT_APIKEY (hacer UNA sola vez):**
1. Desde tu WhatsApp personal (+51 960 560 064), enviar el mensaje `I allow callmebot to send me messages` al número de Callmebot: **+34 644 45 70 93**
2. Callmebot te responderá con tu `apikey` personal
3. Pegar esa apikey en el `.env`

- [ ] **Step 5: Verificar**

Con el servidor corriendo, submittir el formulario wizard completo en `http://127.0.0.1:8000`. Verificar en la consola del servidor que aparece: `Éxito: Notificación WhatsApp enviada al admin via Callmebot.` Y verificar que llega el WhatsApp a tu celular.

Si la apikey aún no está configurada, la consola mostrará la advertencia y el flujo continúa normalmente (sin error para el usuario).

- [ ] **Step 6: Commit**

```powershell
git add main.py
git commit -m "feat: add Callmebot WhatsApp notification to admin on new lead"
```

---

## Task 7: Panel de Admin `/admin`

**Files:**
- Modify: `main.py` (agregar imports, rutas GET /admin y PATCH /api/leads/{id}/status)
- Create: `templates/admin.html`

**Interfaces:**
- Consumes: `LeadSchema` ya definido. Variables de entorno `ADMIN_USER`, `ADMIN_PASSWORD`. `SUPABASE_URL`, `SUPABASE_KEY` ya configurados.
- Produces: Ruta `GET /admin` con autenticación Basic. Ruta `PATCH /api/leads/{lead_id}/status` que actualiza Supabase y el JSON local.

- [ ] **Step 1: Agregar imports necesarios en main.py**

Agregar al bloque de imports existente:

```python
from fastapi import FastAPI, Request, Form, status, BackgroundTasks, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
```

Reemplazar la línea de import de FastAPI actual:

```python
from fastapi import FastAPI, Request, Form, status, BackgroundTasks
```

Con:

```python
from fastapi import FastAPI, Request, Form, status, BackgroundTasks, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
```

- [ ] **Step 2: Agregar configuración de HTTP Basic Auth y variables admin**

Después de las variables `SMTP_*` y antes de `app = FastAPI(...)`, agregar:

```python
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

security = HTTPBasic()

def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    user_ok = secrets.compare_digest(credentials.username.encode(), ADMIN_USER.encode())
    pass_ok = secrets.compare_digest(credentials.password.encode(), ADMIN_PASSWORD.encode())
    if not (user_ok and pass_ok) or not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
```

- [ ] **Step 3: Agregar ruta GET /admin en main.py**

Agregar después de la ruta `GET /api/leads`:

```python
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, _: str = Depends(verificar_admin)):
    """Panel de administración de leads protegido con HTTP Basic Auth."""
    leads = []
    if SUPABASE_URL and SUPABASE_KEY:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/leads?order=timestamp.desc"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=8.0)
                if response.status_code == 200:
                    leads = response.json()
        except Exception as e:
            print(f"Error leyendo leads de Supabase: {e}")

    if not leads and os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
                leads = list(reversed(leads))
        except Exception:
            leads = []

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={"leads": leads}
    )


@app.patch("/api/leads/{lead_id}/status")
async def update_lead_status(lead_id: str, request: Request, _: str = Depends(verificar_admin)):
    """Actualiza el estado de un lead en Supabase."""
    body = await request.json()
    new_status = body.get("status", "nuevo")
    valid_statuses = {"nuevo", "contactado", "en_negociacion", "ganado", "perdido"}
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Usar: {valid_statuses}")

    if SUPABASE_URL and SUPABASE_KEY:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/leads?id=eq.{lead_id}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(url, json={"status": new_status}, headers=headers, timeout=8.0)
                if response.status_code in [200, 204]:
                    return {"ok": True, "status": new_status}
                else:
                    raise HTTPException(status_code=502, detail="Error actualizando en Supabase")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=502, detail=str(e))

    return {"ok": True, "status": new_status, "note": "Supabase no configurado, estado no persistido"}
```

- [ ] **Step 4: Agregar variables admin al .env**

Agregar al archivo `.env`:

```
ADMIN_USER=admin
ADMIN_PASSWORD=nocode2026
```

Cambiar `nocode2026` por una contraseña segura de tu elección.

- [ ] **Step 5: Crear templates/admin.html**

Crear el archivo `templates/admin.html` con este contenido completo:

```html
{% extends "base.html" %}

{% block content %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
        <div>
            <div class="eyebrow eyebrow--block mb-1">PANEL ADMIN</div>
            <h1 class="text-2xl font-extrabold text-white">Gestión de Leads</h1>
        </div>
        <div class="flex items-center gap-4">
            <div class="font-mono text-xs text-slate-500">
                Total: <span class="text-brand-electric font-bold">{{ leads | length }}</span> leads
            </div>
            <a href="/" class="os-cta-ghost font-mono text-xs uppercase tracking-wider py-2 px-4">
                <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
                Ir al sitio
            </a>
        </div>
    </div>

    <!-- Status summary badges -->
    <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 mb-8">
        {% set estados = {'nuevo': 'brand-electric', 'contactado': 'blue-400', 'en_negociacion': 'amber-400', 'ganado': 'emerald-400', 'perdido': 'slate-400'} %}
        {% for estado, color in [('nuevo','brand-electric'),('contactado','blue-400'),('en_negociacion','amber-400'),('ganado','emerald-400'),('perdido','slate-400')] %}
        <div class="bento-card py-3 text-center">
            <div class="text-xl font-black text-white">{{ leads | selectattr('status', 'equalto', estado) | list | length if leads else 0 }}</div>
            <div class="font-mono text-[9px] text-slate-500 uppercase tracking-widest mt-1">{{ estado | replace('_', ' ') }}</div>
        </div>
        {% endfor %}
    </div>

    <!-- Leads table -->
    {% if leads %}
    <div class="os-card p-0 overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-left font-mono text-xs">
                <thead>
                    <tr class="bg-brand-deep/40 border-b border-white/10 text-slate-400 uppercase tracking-wider">
                        <th class="p-4">Fecha</th>
                        <th class="p-4">Cliente</th>
                        <th class="p-4">Empresa</th>
                        <th class="p-4">Rubro</th>
                        <th class="p-4">Cotización</th>
                        <th class="p-4">Estado</th>
                        <th class="p-4">Acciones</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-white/5">
                    {% for lead in leads %}
                    <tr
                        class="hover:bg-brand-deep/20 transition-colors"
                        x-data="{ status: '{{ lead.get('status', 'nuevo') }}', saving: false }"
                        id="lead-{{ loop.index }}"
                    >
                        <td class="p-4 text-slate-500 whitespace-nowrap">
                            {{ lead.get('timestamp', '-')[:16] }}
                        </td>
                        <td class="p-4">
                            <div class="font-bold text-white">{{ lead.get('nombre', '-') }}</div>
                            <div class="text-slate-500 text-[10px] mt-0.5">{{ lead.get('correo', '-') }}</div>
                        </td>
                        <td class="p-4 text-slate-300">{{ lead.get('empresa', '-') }}</td>
                        <td class="p-4">
                            <span class="os-pill os-pill--primary text-[9px]">{{ lead.get('rubro', '-') }}</span>
                        </td>
                        <td class="p-4 text-brand-electric font-bold">
                            {{ lead.get('costo_estimado', '-') }}
                        </td>
                        <td class="p-4">
                            <select
                                x-model="status"
                                @change="
                                    saving = true;
                                    fetch('/api/leads/{{ lead.get('id', loop.index) }}/status', {
                                        method: 'PATCH',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({status: status})
                                    }).then(r => r.json()).then(() => { saving = false; }).catch(() => { saving = false; })
                                "
                                :class="{
                                    'text-brand-electric': status === 'nuevo',
                                    'text-blue-400': status === 'contactado',
                                    'text-amber-400': status === 'en_negociacion',
                                    'text-emerald-400': status === 'ganado',
                                    'text-slate-400': status === 'perdido'
                                }"
                                class="bg-brand-deep/50 border border-white/10 rounded-lg px-2 py-1 text-[10px] font-bold uppercase tracking-wider focus:outline-none focus:border-brand-electric cursor-pointer"
                            >
                                <option value="nuevo">Nuevo</option>
                                <option value="contactado">Contactado</option>
                                <option value="en_negociacion">En negociación</option>
                                <option value="ganado">Ganado</option>
                                <option value="perdido">Perdido</option>
                            </select>
                            <span x-show="saving" class="ml-2 inline-block w-3 h-3 border-2 border-brand-electric border-t-transparent rounded-full animate-spin"></span>
                        </td>
                        <td class="p-4">
                            <div class="flex items-center gap-2">
                                <a
                                    href="https://wa.me/51{{ lead.get('telefono', '') }}?text={{ ('Hola ' + lead.get('nombre', '') + ', vi tu cotización de ' + lead.get('costo_estimado', '') + ' con NoCode Creator. ¿Conversamos?') | urlencode }}"
                                    target="_blank"
                                    class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 hover:bg-emerald-500/20 transition-colors text-[10px] font-bold uppercase"
                                    title="Abrir WhatsApp"
                                >
                                    <i data-lucide="message-circle" class="w-3.5 h-3.5"></i>
                                    WA
                                </a>
                                <a
                                    href="mailto:{{ lead.get('correo', '') }}"
                                    class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-brand-blue/10 border border-brand-blue/20 text-brand-blue hover:bg-brand-blue/20 transition-colors text-[10px] font-bold uppercase"
                                    title="Enviar Email"
                                >
                                    <i data-lucide="mail" class="w-3.5 h-3.5"></i>
                                    Email
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    {% else %}
    <div class="bento-card text-center py-16">
        <i data-lucide="inbox" class="w-12 h-12 text-slate-600 mx-auto mb-4"></i>
        <p class="text-slate-500 font-mono text-sm">No hay leads registrados aún.</p>
        <p class="text-slate-600 font-mono text-xs mt-2">Los leads aparecerán aquí cuando los clientes completen el formulario.</p>
    </div>
    {% endif %}

    <!-- Notas de problema por lead (expandible) -->
    {% if leads %}
    <div class="mt-8">
        <div class="eyebrow eyebrow--block mb-4">DETALLE DE SOLICITUDES</div>
        <div class="space-y-3">
            {% for lead in leads %}
            {% if lead.get('problema') %}
            <div class="os-card py-3 px-4">
                <div class="flex items-start justify-between gap-4">
                    <div class="flex-1">
                        <span class="font-bold text-white text-sm">{{ lead.get('nombre', '-') }}</span>
                        <span class="text-slate-500 text-xs mx-2">·</span>
                        <span class="text-brand-electric text-xs font-mono">{{ lead.get('rubro', '-') }}</span>
                        <p class="text-slate-400 text-xs mt-1 leading-relaxed">{{ lead.get('problema', '-') }}</p>
                    </div>
                    <span class="text-slate-600 text-[10px] font-mono whitespace-nowrap">{{ lead.get('timestamp', '-')[:10] }}</span>
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
```

- [ ] **Step 6: Agregar columna status a Supabase**

Ejecutar este SQL en el editor SQL de Supabase (dashboard → SQL Editor):

```sql
ALTER TABLE leads ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'nuevo';
```

Si la tabla `leads` no tiene columna `id` de tipo UUID, ejecutar también:

```sql
ALTER TABLE leads ADD COLUMN IF NOT EXISTS id UUID DEFAULT gen_random_uuid();
```

- [ ] **Step 7: Verificar el panel admin**

Navegar a `http://127.0.0.1:8000/admin`. El navegador pedirá usuario y contraseña:
- Usuario: `admin`
- Contraseña: la que pusiste en `.env`

Verificar:
- Lista de leads con columnas correctas
- Dropdown de estado por lead cambia al seleccionar (spinner aparece)
- Botón WA abre WhatsApp con mensaje pre-llenado
- Si no hay leads aún: aparece el mensaje "No hay leads registrados aún"

Submittir un lead de prueba en `http://127.0.0.1:8000`, luego volver al admin y verificar que aparece con status "nuevo".

- [ ] **Step 8: Commit final**

```powershell
git add main.py templates/admin.html
git commit -m "feat: add admin panel with HTTP Basic Auth and lead status management"
```

---

## Verificación final integral

- [ ] Navegar toda la página en escritorio — verificar scroll completo sin errores de consola
- [ ] Navegar en móvil (DevTools → Toggle device toolbar) — verificar responsive en 375px
- [ ] Sección "Lo que construimos": 4 cards visibles y correctas
- [ ] Sección "Cómo trabajamos": 3 pasos con conectores
- [ ] Cotizador AI: seleccionar rubro y módulos → precio cambia dinámicamente
- [ ] Chatbot: abrir, escribir mensaje, verificar respuesta Gemini
- [ ] Terminal (tecla ` o botón): abrir, escribir `ayuda`, verificar lista de comandos
- [ ] Boot screen: recargar con Ctrl+Shift+R para ver el boot (en nueva sesión)
- [ ] Formulario: completar los 3 pasos → verificar redirección a success.html
- [ ] WhatsApp admin: verificar recepción del mensaje en tu celular
- [ ] Admin panel: verificar leads, cambiar status de uno
- [ ] Admin: verificar que URL `/admin` sin credenciales pide autenticación

```powershell
git add .
git commit -m "feat: complete visual redesign and WhatsApp admin flow"
```
