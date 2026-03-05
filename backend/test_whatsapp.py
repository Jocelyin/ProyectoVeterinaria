"""
Script de prueba para Twilio WhatsApp.
Ejecutar desde la carpeta backend:
    python test_whatsapp.py +52XXXXXXXXXX
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID   = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN    = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

def test_send(phone_number: str):
    print(f"\n{'='*50}")
    print(f"  Test Twilio WhatsApp")
    print(f"{'='*50}")
    print(f"  ACCOUNT_SID : {TWILIO_ACCOUNT_SID[:8]}... (oculto)")
    print(f"  AUTH_TOKEN  : {'OK' if TWILIO_AUTH_TOKEN else '❌ VACÍO'}")
    print(f"  FROM        : {TWILIO_WHATSAPP_FROM}")
    print(f"  TO          : whatsapp:{phone_number}")
    print(f"{'='*50}\n")

    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("❌ ERROR: TWILIO_ACCOUNT_SID o TWILIO_AUTH_TOKEN no están configurados en el .env")
        return

    if not phone_number.startswith("+52"):
        print("❌ ERROR: El número debe empezar con +52 (México). Ejemplo: +5215512345678")
        return

    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{phone_number}",
            body=(
                "🐾 Prueba de notificación\n\n"
                "Este es un mensaje de prueba del sistema VeterinariaTest.\n"
                "¡Twilio WhatsApp funciona correctamente! ✅"
            )
        )
        print(f"✅ Mensaje enviado exitosamente!")
        print(f"   SID     : {message.sid}")
        print(f"   Status  : {message.status}")

    except Exception as e:
        print(f"❌ Error al enviar: {e}")
        print()
        if "21608" in str(e):
            print("💡 Causa: El número de destino no está unido al Sandbox de Twilio.")
            print("   Solución: Envía 'join <tu-palabra>' al +14155238886 desde tu WhatsApp.")
        elif "20003" in str(e):
            print("💡 Causa: Credenciales incorrectas (Account SID o Auth Token).")
        elif "21211" in str(e):
            print("💡 Causa: El número de teléfono tiene formato incorrecto.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python test_whatsapp.py +52XXXXXXXXXX")
        print("Ejemplo: python test_whatsapp.py +5215512345678")
        sys.exit(1)
    test_send(sys.argv[1])
