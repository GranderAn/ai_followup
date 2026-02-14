import hmac
import hashlib
import time
from fastapi import Request, HTTPException, status
from app.core.config import settings


MAX_SKEW_SECONDS = 300  # 5 minutes


async def verify_calendly_signature(request: Request) -> None:
    secret = settings.CALENDLY_WEBHOOK_SECRET
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Calendly signing secret not configured",
        )

    sig_header = request.headers.get("Calendly-Webhook-Signature")
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Calendly signature",
        )

    # Parse header: t=...,v1=...
    parts = dict(
        item.split("=", 1) for item in sig_header.split(",") if "=" in item
    )
    timestamp = parts.get("t")
    signature = parts.get("v1")

    if not timestamp or not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Calendly signature format",
        )

    # Replay protection
    now = int(time.time())
    try:
        ts_int = int(timestamp)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid timestamp in Calendly signature",
        )

    if abs(now - ts_int) > MAX_SKEW_SECONDS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Calendly signature timestamp too old",
        )

    body = await request.body()
    signed_payload = f"{timestamp}.{body.decode()}".encode()

    expected = hmac.new(
        key=secret.encode(),
        msg=signed_payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Calendly signature",
        )