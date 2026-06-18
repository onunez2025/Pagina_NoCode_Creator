# Diseño: Rediseño Visual + Flujo WhatsApp + Panel Admin
**Fecha:** 2026-06-18  
**Proyecto:** NoCode Creator — Landing Page  
**Stack:** FastAPI + Jinja2 + Alpine.js + Tailwind CSS  

---

## 1. Resumen

Tres objetivos en paralelo:

1. **Rediseño visual completo** — nueva identidad "plasma azul" fiel a la paleta del logo, con bento grid, animaciones de partículas y tipografía Space Grotesk pesada. Demuestra capacidad para construir cualquier tipo de plataforma.
2. **Notificación WhatsApp al admin** — cuando llega un lead, el admin recibe un mensaje instantáneo en su WhatsApp vía Callmebot (gratis).
3. **Panel de admin `/admin`** — página protegida por contraseña para gestionar el pipeline de leads con estados y botón directo a WhatsApp de cada cliente.

---

## 2. Identidad Visual

### Paleta de colores (basada en el logo)
| Token | Valor | Uso |
|---|---|---|
| `brand-navy` | `#050c1a` | Fondo general |
| `brand-deep` | `#1e3a8a` | Capas profundas, fondos de cards |
| `brand-blue` | `#3b82f6` | Color primario, botones, highlights |
| `brand-electric` | `#38bdf8` | Acento brillante, bordes activos, neon |
| `brand-white` | `#f8fafc` | Texto principal |
| `brand-muted` | `#64748b` | Texto secundario |

**Gradiente firma:** `linear-gradient(135deg, #1e3a8a, #3b82f6, #38bdf8)`

### Tipografía
- **Headings:** Space Grotesk 700–900 (Google Fonts)
- **Mono/técnico:** JetBrains Mono 500–700 (ya incluido)
- **Body:** Space Grotesk 400–500

### Efectos visuales
- Fondo hero: mesh de partículas animadas en CSS (sin librerías extra)
- Cards: borde con gradiente animado tipo "aurora"
- Texto hero: efecto shimmer/glow en la palabra clave
- Botones CTA: gradiente animado + sombra azul eléctrica

### Layout
- Sistema **Bento Grid** en la sección "Lo que construimos" (2x2 con cards de tamaños mixtos)
- Resto de secciones: max-width container con grid responsive estándar

---

## 3. Estructura de Secciones (nueva página)

### 3.1 Hero (full-screen)
- Fondo: negro navy con mesh de partículas azules CSS
- Headline principal: **"Construimos cualquier plataforma digital que imagines"**
- Subheadline: propuesta de valor (precio, velocidad, Lima)
- Badge animado: "⚡ IA + LOW-CODE · LIMA, PERÚ"
- CTAs: `[Cotizar mi proyecto]` `[Ver lo que hacemos ↓]`
- Visual derecho: mockup de browser con la imagen actual del dashboard

### 3.2 Lo que construimos (NUEVA SECCIÓN)
Bento grid 2×2 con los 4 tipos de proyecto:

| Card | Título | Descripción breve | Ejemplos |
|---|---|---|---|
| Páginas web | Landings & Sitios Web | Sitios institucionales, portfolios, blogs | Landing de producto, portafolio profesional |
| Apps móviles | Apps iOS & Android | Apps híbridas React Native / Flutter | App de pedidos, app de reservas |
| ERP / CRM | Sistemas de Gestión | Paneles admin, inventario, reportes | POS, control de stock, CRM de clientes |
| E-commerce | Tiendas Online | Catálogo con carrito, Yape/Plin integrado | Tienda de ropa, minimarket online |

Cada card tiene: icono grande (Lucide), título, descripción, 2 tags de tecnología.

### 3.3 Cómo trabajamos (NUEVA SECCIÓN)
3 pasos en línea horizontal:
1. **Cotizas** — Usas el cotizador AI o escribes al chat
2. **Diseñamos** — En tiempo récord con IA y Low-Code
3. **Entregamos** — Con soporte local por WhatsApp

### 3.4 Stats (actualizada)
4 métricas animadas con contadores JS. Los valores son configurables directamente en el HTML del template (no vienen del backend):
- **Proyectos entregados:** definir número real (ej. "12+", "20+")
- **Ahorro vs agencia tradicional:** 85% (ya establecido en el sitio actual)
- **Precio base:** S/ 500 (ya establecido)
- **Soporte incluido:** 90 días (ya establecido)

> El usuario debe definir el número de "proyectos entregados" antes de implementar esta sección.

### 3.5 Cotizador AI (rediseñado visualmente)
Misma funcionalidad actual (Alpine.js), nuevo estilo visual con la paleta azul y bento layout.

### 3.6 Plataformas Activas (rediseñada)
Mismo contenido actual, nuevo estilo visual.

### 3.7 Comparativa (rediseñada)
Misma tabla actual, nuevo estilo visual.

### 3.8 Wizard de Leads (rediseñado)
Mismo formulario de 3 pasos, nuevo estilo visual.

### 3.9 FAQ (rediseñada)
Mismo acordeón, nuevo estilo visual.

### 3.10 Footer (actualizado)
Igual al actual + redes sociales (placeholders).

### Elementos persistentes
- Chatbot flotante Gemini (sin cambios funcionales, solo estilo)
- Terminal overlay (sin cambios funcionales, solo estilo)
- Boot screen (sin cambios funcionales, solo paleta)

---

## 4. Notificación WhatsApp al Admin (Callmebot)

### Servicio usado
**Callmebot API** — gratuito, sin cuentas, sin WhatsApp Business API. El admin registra su número una vez enviando un mensaje al bot de Callmebot.

### Setup requerido (solo una vez, manual)
El admin (tú) debe enviar desde tu WhatsApp personal al número de Callmebot: `"I allow callmebot to send me messages"`. Callmebot te responde con tu `apikey`.

### Implementación en backend
Nueva función en `main.py`:

```python
async def enviar_whatsapp_admin(lead_data: dict):
    phone = os.getenv("CALLMEBOT_PHONE")   # Tu número sin + ej: 51960560064
    apikey = os.getenv("CALLMEBOT_APIKEY") # La apikey que te da Callmebot
    if not phone or not apikey:
        return
    mensaje = (
        f"⚡ NUEVO LEAD - NoCode Creator\n\n"
        f"👤 {lead_data['nombre']}\n"
        f"🏢 {lead_data.get('empresa', '-')}\n"
        f"📱 +51{lead_data['telefono']}\n"
        f"📧 {lead_data['correo']}\n"
        f"🏷️ Rubro: {lead_data['rubro']}\n"
        f"💰 Cotización: {lead_data['costo_estimado']}\n"
        f"📝 {lead_data['problema'][:100]}\n\n"
        f"👉 Responder: wa.me/51{lead_data['telefono']}"
    )
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={urllib.parse.quote(mensaje)}&apikey={apikey}"
    async with httpx.AsyncClient() as client:
        await client.get(url, timeout=8.0)
```

Se llama como `background_task` junto al email, para no bloquear la respuesta al usuario.

### Variables de entorno nuevas
```
CALLMEBOT_PHONE=51960560064
CALLMEBOT_APIKEY=<tu-apikey-de-callmebot>
```

---

## 5. Panel Admin `/admin`

### Autenticación
HTTP Basic Auth con usuario y contraseña definidos en variables de entorno:
```
ADMIN_USER=admin
ADMIN_PASSWORD=<contraseña-segura>
```
FastAPI usa `fastapi.security.HTTPBasic` para proteger la ruta. Sin sesiones ni tokens — simple y sin dependencias extra.

### Ruta GET `/admin`
Renderiza `templates/admin.html` con la lista de leads ordenados por timestamp descendente. Lee de Supabase si está disponible, con fallback a `leads.json` local.

### Estado del lead
Se agrega campo `status` al schema de leads con valores:
- `nuevo` (default)
- `contactado`
- `en_negociacion`
- `ganado`
- `perdido`

El estado se persiste en Supabase mediante nueva columna `status TEXT DEFAULT 'nuevo'`. Para el fallback JSON local, se actualiza el archivo directamente.

### Ruta PATCH `/api/leads/{lead_id}/status`
```python
@app.patch("/api/leads/{lead_id}/status")
async def update_lead_status(lead_id: str, status: str, credentials: ...):
    # Actualiza en Supabase: PATCH /rest/v1/leads?id=eq.{lead_id}
    # Retorna {"ok": true}
```
Llamado via `fetch()` desde el frontend del admin con Alpine.js, sin recargar página.

### UI del panel admin
- Misma identidad visual del sitio (dark navy + azul eléctrico)
- Tabla responsive con columnas: Fecha, Cliente, Empresa, Rubro, Teléfono, Cotización, Estado, Acciones
- Dropdown de estado por fila (cambia vía PATCH al backend)
- Botón "Abrir WhatsApp" por fila → abre `wa.me/51{telefono}?text=...` con mensaje pre-llenado
- Botón "Enviar email" por fila (opcional, fase 2)
- Contador de leads por estado en la cabecera

### Identificador de lead
Supabase genera un `id` UUID automáticamente en cada inserción. Se usará ese `id` para el PATCH. En el fallback JSON local, se usará el `timestamp` como identificador (menos ideal pero funcional).

---

## 6. Cambios en archivos existentes

| Archivo | Cambio |
|---|---|
| `static/css/neon.css` | Reemplazado completamente con nueva identidad azul |
| `templates/base.html` | Nueva paleta Tailwind, Space Grotesk, nuevo header/footer/boot |
| `templates/index.html` | Nuevas secciones Hero, Lo que construimos, Cómo trabajamos + rediseño de secciones existentes |
| `templates/success.html` | Rediseño visual |
| `main.py` | +`enviar_whatsapp_admin()`, +ruta `/admin`, +ruta `PATCH /api/leads/{id}/status` |

### Archivos nuevos
| Archivo | Descripción |
|---|---|
| `templates/admin.html` | Panel de admin de leads |
| `static/css/design.css` | CSS base del nuevo diseño (complementa Tailwind) |

---

## 7. Variables de entorno nuevas (.env)

```
CALLMEBOT_PHONE=51960560064
CALLMEBOT_APIKEY=<apikey-de-callmebot>
ADMIN_USER=admin
ADMIN_PASSWORD=<contraseña-segura>
```

---

## 8. Supabase — Migración requerida

Agregar columna `status` a la tabla `leads`:
```sql
ALTER TABLE leads ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'nuevo';
ALTER TABLE leads ADD COLUMN IF NOT EXISTS id UUID DEFAULT gen_random_uuid() PRIMARY KEY;
```
(Si la tabla ya tiene `id`, omitir la segunda línea.)

---

## 9. Lo que NO cambia

- Lógica del cotizador AI (Alpine.js) — solo estilo visual
- Wizard de 3 pasos — solo estilo visual
- Chatbot Gemini — solo estilo visual
- Terminal overlay — solo estilo visual
- Boot screen — solo paleta de colores
- Integración con Supabase para guardar leads
- Notificación por email SMTP (se mantiene, se agrega WhatsApp encima)

---

## 10. Criterios de éxito

- [ ] La página comunica claramente los 4 tipos de proyectos que se pueden construir
- [ ] El admin recibe un WhatsApp dentro de los 15 segundos de que un cliente envía el formulario
- [ ] El panel `/admin` muestra todos los leads y permite cambiar su estado sin recargar la página
- [ ] El botón "Abrir WhatsApp" del admin incluye el nombre del cliente y su cotización en el mensaje
- [ ] El sitio pasa el "test de 5 segundos": un visitante nuevo entiende qué hace la empresa y qué puede pedir
- [ ] El diseño es visualmente coherente con los colores del logo en todas las secciones
