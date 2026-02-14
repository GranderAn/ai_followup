import httpx
from app.core.config import get_settings

settings = get_settings()


async def send_email(to_email: str, subject: str, body: str) -> None:
    # Example using SendGrid API
    url = "https://api.sendgrid.com/v3/mail/send"
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": settings.EMAIL_FROM},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"},
        )
        resp.raise_for_status()