import json
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from fastapi import FastAPI, Request, Form, status, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import httpx

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SMTP_USER = os.getenv("SMTP_USER", "no.code.creator.adm@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
except (ValueError, TypeError):
    SMTP_PORT = 587

app = FastAPI(
    title="No-Code-Creator Landing Page API",
    description="Backend en FastAPI para gestionar la landing page interactiva, base de datos en Supabase y alertas de leads por correo.",
    version="1.2.0"
)

# Definir directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
LEADS_FILE = os.path.join(BASE_DIR, "leads.json")

# Crear carpetas necesarias si no existen
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "images"), exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Configurar Jinja2 Templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)


class LeadSchema(BaseModel):
    nombre: str
    correo: str
    telefono: str
    empresa: Optional[str] = "No especificado"
    rubro: str
    problema: str
    costo_estimado: str
    tiempo_estimado: str
    timestamp: str


def guardar_lead_local(lead_data: dict):
    """Guarda un lead de prospecto en un archivo JSON local como respaldo."""
    leads = []
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except Exception:
            leads = []
            
    leads.append(lead_data)
    
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=4)


async def guardar_lead_supabase(lead_data: dict) -> bool:
    """Guarda un lead en la base de datos de Supabase usando su API REST."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Advertencia: No se encontraron las credenciales de Supabase en el archivo .env")
        return False

    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/leads"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=lead_data, headers=headers, timeout=8.0)
            if response.status_code in [200, 201, 204]:
                print("Éxito: Lead guardado correctamente en la base de datos de Supabase.")
                return True
            else:
                print(f"Error Supabase (Código {response.status_code}): {response.text}")
                return False
    except Exception as e:
        print(f"Excepción al conectar con Supabase: {str(e)}")
        return False


def enviar_correo_notificacion(lead_data: dict):
    """Envía un correo de notificación al administrador cuando se capta un nuevo lead."""
    if not SMTP_PASSWORD:
        print("Advertencia: No se configuró SMTP_PASSWORD en el archivo .env. Alerta de correo omitida.")
        return False

    # Crear la estructura del mensaje
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚡ Nuevo Lead Captado: {lead_data.get('nombre')} - {lead_data.get('empresa')}"
    msg["From"] = SMTP_USER
    msg["To"] = SMTP_USER  # Te lo envías a ti mismo para seguimiento

    # Cuerpo del correo en HTML premium adaptado a la estética de la marca
    html_content = f"""
    <html>
      <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #020617; color: #f8fafc; padding: 20px; margin: 0;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 30px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);">
          
          <!-- Encabezado -->
          <div style="text-align: center; border-bottom: 1px solid #1e293b; padding-bottom: 20px; margin-bottom: 25px;">
            <div style="display: inline-block; background-color: #0f172a; padding: 8px 16px; border: 1px solid #06b6d4; border-radius: 8px; color: #06b6d4; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-bottom: 10px;">
                ⚡ Alerta de Sistema
            </div>
            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 800;">¡Nuevo Lead Registrado!</h1>
            <p style="color: #94a3b8; font-size: 13px; margin: 5px 0 0 0;">Landing Page de No-Code-Creator (Lima)</p>
          </div>
          
          <!-- Detalles en Tabla -->
          <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 25px; border: 1px solid #334155;">
            <table style="width: 100%; border-collapse: collapse;">
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155; width: 35%;"><strong>Nombre:</strong></td>
                <td style="padding: 10px 0; color: #ffffff; font-size: 14px; border-bottom: 1px solid #334155;"><strong>{lead_data.get('nombre')}</strong></td>
              </tr>
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155;"><strong>Empresa / Negocio:</strong></td>
                <td style="padding: 10px 0; color: #ffffff; font-size: 14px; border-bottom: 1px solid #334155;">{lead_data.get('empresa')}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155;"><strong>Rubro Comercial:</strong></td>
                <td style="padding: 10px 0; color: #06b6d4; font-size: 14px; border-bottom: 1px solid #334155; font-weight: bold;">{lead_data.get('rubro')}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155;"><strong>WhatsApp / Tel:</strong></td>
                <td style="padding: 10px 0; color: #ffffff; font-size: 14px; border-bottom: 1px solid #334155;"><a href="https://wa.me/51{lead_data.get('telefono')}" style="color: #22c55e; text-decoration: none; font-weight: bold;">+51 {lead_data.get('telefono')}</a></td>
              </tr>
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155;"><strong>Correo Electrónico:</strong></td>
                <td style="padding: 10px 0; color: #ffffff; font-size: 14px; border-bottom: 1px solid #334155;"><a href="mailto:{lead_data.get('correo')}" style="color: #6366f1; text-decoration: none;">{lead_data.get('correo')}</a></td>
              </tr>
              <tr>
                <td style="padding: 10px 0; color: #94a3b8; font-size: 13px; border-bottom: 1px solid #334155;"><strong>Cotización AI:</strong></td>
                <td style="padding: 10px 0; color: #f59e0b; font-size: 14px; border-bottom: 1px solid #334155; font-weight: bold;">{lead_data.get('costo_estimado')} ({lead_data.get('tiempo_estimado')})</td>
              </tr>
              <tr>
                <td style="padding: 12px 0 0 0; color: #94a3b8; font-size: 13px; vertical-align: top;"><strong>Problema / Necesidad:</strong></td>
                <td style="padding: 12px 0 0 0; color: #f8fafc; font-size: 13px; line-height: 1.5; vertical-align: top;">{lead_data.get('problema')}</td>
              </tr>
            </table>
          </div>
          
          <!-- Botón de Acción -->
          <div style="text-align: center; margin-top: 15px; margin-bottom: 10px;">
            <a href="https://wa.me/51{lead_data.get('telefono')}?text=Hola%20{lead_data.get('nombre')},%20vi%20tu%20cotizaci%C3%B3n%20con%20No-Code-Creator.%20Conversemos%20sobre%20tu%20proyecto!" 
               style="display: inline-block; background-color: #22c55e; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.2);">
               Abrir Chat de WhatsApp
            </a>
          </div>
          
          <div style="border-top: 1px solid #1e293b; margin-top: 30px; padding-top: 15px; text-align: center; color: #64748b; font-size: 11px;">
            Este correo fue generado y enviado automáticamente en tiempo real por el backend de No-Code-Creator en Lima, Perú.
          </div>
        </div>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Enviar de forma segura por SMTP TLS
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, SMTP_USER, msg.as_string())
        print("Éxito: Correo de notificación enviado correctamente al administrador.")
        return True
    except Exception as e:
        print(f"Error al enviar correo SMTP: {str(e)}")
        return False


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """Renderiza la página de inicio (Landing Page)."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/contact")
async def handle_contact(
    background_tasks: BackgroundTasks,
    nombre: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    empresa: Optional[str] = Form("No especificado"),
    rubro: str = Form("General"),
    problema: str = Form("No especificado"),
    costo_estimado: str = Form("Por cotizar"),
    tiempo_estimado: str = Form("Por definir")
):
    """Procesa el envío del formulario de cotización/contacto."""
    lead_data = {
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "empresa": empresa or "No especificado",
        "rubro": rubro,
        "problema": problema,
        "costo_estimado": costo_estimado,
        "tiempo_estimado": tiempo_estimado,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 1. Guardar en base de datos local JSON (Respaldo)
    guardar_lead_local(lead_data)
    
    # 2. Guardar en la nube (Supabase)
    await guardar_lead_supabase(lead_data)
    
    # 3. Enviar correo de notificación de forma no bloqueante (Background Task)
    background_tasks.add_task(enviar_correo_notificacion, lead_data)
    
    # Redireccionar a la página de éxito pasando información personalizada como parámetros query
    redirect_url = f"/success?nombre={nombre}&rubro={rubro}&empresa={empresa or ''}"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/success", response_class=HTMLResponse)
async def read_success(
    request: Request,
    nombre: str = "Emprendedor",
    rubro: str = "su negocio",
    empresa: str = ""
):
    """Renderiza la página de éxito personalizada."""
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={
            "nombre": nombre,
            "rubro": rubro,
            "empresa": empresa
        }
    )


@app.get("/api/leads")
async def get_all_leads():
    """Endpoint administrativo simulado para ver los leads registrados."""
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"error": "No se pudo leer el archivo de leads."}
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
