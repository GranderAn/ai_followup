import httpx
from app.core.config import get_settings

settings = get_settings()


AI_SYSTEM_PROMPT = """
You are an AI assistant helping a small business respond to new leads.
Your job is to write short, clear, friendly messages that sound human and encourage the lead to reply or book an appointment.

Rules:
- Keep messages under 3–5 sentences.
- Use a friendly, professional, conversational tone.
- No emojis.
- No long paragraphs.
- No hype or salesy language.
- Always include the booking link when appropriate.
- Always ask a simple question to encourage a reply.
- Never mention AI or automation.
- Never invent details not provided.
"""


async def generate_message(
    message_type: str,
    business_name: str,
    service: str,
    lead_name: str,
    booking_link: str | None = None,
    lead_message: str | None = None,
) -> str:
    user_prompt_parts = [
        f"Business Name: {business_name}",
        f"Service: {service}",
        f"Lead Name: {lead_name}",
        f"Message Type: {message_type}",
    ]
    if booking_link:
        user_prompt_parts.append(f"Booking Link: {booking_link}")
    if lead_message:
        user_prompt_parts.append(f"Lead Message: {lead_message}")

    user_prompt = "\n".join(user_prompt_parts)

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": AI_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()