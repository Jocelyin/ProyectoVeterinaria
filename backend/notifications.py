"""
Servicio de notificaciones para confirmación de citas.
- Email: Gmail vía SMTP (contraseña de aplicación)
- WhatsApp: Twilio WhatsApp API (oficial)

Configurar credenciales en el archivo .env del backend.
"""

import os
import smtplib
import threading
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("notifications")

# --- Email (SMTP) ---
SMTP_EMAIL    = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))

# --- Twilio WhatsApp ---
TWILIO_ACCOUNT_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN    = os.getenv("TWILIO_AUTH_TOKEN", "")
# Número de WhatsApp de Twilio (Sandbox: "whatsapp:+14155238886")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _format_phone_for_whatsapp(phone: str) -> Optional[str]:
    """
    Limpia el número y lo devuelve en formato 'whatsapp:+52XXXXXXXXXX'.
    Solo acepta números mexicanos (+52). Cualquier otro código de país
    es rechazado silenciosamente.
    Devuelve None si el formato no es válido o no es México.
    """
    if not phone:
        return None
    cleaned = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not cleaned.startswith("+52"):
        logger.warning(f"[WhatsApp/Twilio] Número ignorado (solo se permiten números +52 México): {phone}")
        return None
    if len(cleaned) < 12:  # +52 + 10 dígitos mínimo
        logger.warning(f"[WhatsApp/Twilio] Número +52 demasiado corto: {phone}")
        return None
    return f"whatsapp:{cleaned}"


def _build_message(nombre_cliente: str, nombre_mascota: str,
                   fecha_hora, nombre_veterinaria: str) -> dict:
    """Genera el mensaje de confirmación en texto plano y HTML."""
    fecha_str = fecha_hora.strftime("%d de %B de %Y")
    hora_str  = fecha_hora.strftime("%I:%M %p")

    text = (
        f"Hola {nombre_cliente} 👋\n\n"
        f"Tu cita para {nombre_mascota} ha sido agendada 🐾\n\n"
        f"📅 {fecha_str}\n"
        f"⏰ {hora_str}\n\n"
        f"Veterinaria: {nombre_veterinaria}\n\n"
        f"¡Te esperamos! 😊"
    )

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto;
                background: #f9f9f9; border-radius: 12px; padding: 28px;">
      <h2 style="color: #2d7d46;">✅ Cita Confirmada</h2>
      <p>Hola <strong>{nombre_cliente}</strong> 👋</p>
      <p>Tu cita para <strong>{nombre_mascota}</strong> ha sido agendada 🐾</p>
      <table style="background:#fff; border-radius:8px; padding:16px; width:100%;
                    border-collapse:collapse; margin-top:12px;">
        <tr>
          <td style="padding:6px; color:#555;">📅 Fecha</td>
          <td style="padding:6px; font-weight:bold;">{fecha_str}</td>
        </tr>
        <tr>
          <td style="padding:6px; color:#555;">⏰ Hora</td>
          <td style="padding:6px; font-weight:bold;">{hora_str}</td>
        </tr>
        <tr>
          <td style="padding:6px; color:#555;">🏥 Veterinaria</td>
          <td style="padding:6px;">{nombre_veterinaria}</td>
        </tr>
      </table>
      <p style="margin-top:20px; color:#2d7d46; font-weight:bold;">¡Te esperamos! 😊</p>
    </div>
    """
    return {"text": text, "html": html}


# ── Email (SMTP / Gmail) ──────────────────────────────────────────────────────

def _send_email(to_email: str, nombre_cliente: str, nombre_mascota: str,
                fecha_hora, nombre_veterinaria: str):
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        logger.warning("[Email] No configurado (SMTP_EMAIL / SMTP_PASSWORD vacíos)")
        return

    msg_data = _build_message(nombre_cliente, nombre_mascota, fecha_hora, nombre_veterinaria)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🐾 Cita confirmada para {nombre_mascota} — {nombre_veterinaria}"
    msg["From"]    = SMTP_EMAIL
    msg["To"]      = to_email

    msg.attach(MIMEText(msg_data["text"], "plain", "utf-8"))
    msg.attach(MIMEText(msg_data["html"], "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        logger.info(f"[Email] ✅ Enviado a {to_email}")
    except Exception as e:
        logger.error(f"[Email] ❌ Error al enviar a {to_email}: {e}")


# ── WhatsApp (Twilio) ─────────────────────────────────────────────────────────

def _send_whatsapp_twilio(phone: str, nombre_cliente: str, nombre_mascota: str,
                          fecha_hora, nombre_veterinaria: str):
    """Envía mensaje de WhatsApp usando la API oficial de Twilio."""
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.warning("[WhatsApp/Twilio] No configurado (TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN vacíos)")
        return

    to_whatsapp = _format_phone_for_whatsapp(phone)
    if not to_whatsapp:
        logger.warning(f"[WhatsApp/Twilio] Número inválido (requiere código de país +xx): {phone}")
        return

    try:
        from twilio.rest import Client  # Import aquí para que el servidor arranque aunque no esté instalado
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        msg_data = _build_message(nombre_cliente, nombre_mascota, fecha_hora, nombre_veterinaria)

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=to_whatsapp,
            body=msg_data["text"]
        )
        logger.info(f"[WhatsApp/Twilio] ✅ Enviado a {to_whatsapp} — SID: {message.sid}")
    except ImportError:
        logger.error("[WhatsApp/Twilio] ❌ Paquete 'twilio' no instalado. Ejecuta: pip install twilio")
    except Exception as e:
        logger.error(f"[WhatsApp/Twilio] ❌ Error al enviar a {to_whatsapp}: {e}")


# ── Punto de entrada público ──────────────────────────────────────────────────

def notify_cita_created(
    email: Optional[str],
    telefono: Optional[str],
    nombre_cliente: str,
    nombre_mascota: str,
    fecha_hora,
    nombre_veterinaria: str,
):
    """
    Envía notificaciones de confirmación en un hilo separado (no bloquea HTTP).
    - Email: si el cliente tiene email y SMTP está configurado.
    - WhatsApp: si el cliente tiene teléfono con código de país y Twilio está configurado.
    """
    def _run():
        if email and email.strip():
            _send_email(email.strip(), nombre_cliente, nombre_mascota,
                        fecha_hora, nombre_veterinaria)
        if telefono and telefono.strip():
            _send_whatsapp_twilio(telefono.strip(), nombre_cliente, nombre_mascota,
                                  fecha_hora, nombre_veterinaria)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
