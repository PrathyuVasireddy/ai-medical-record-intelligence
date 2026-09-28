import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def extract_medical_data_with_ai(record_text):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are extracting structured information from a synthetic medical record.

Return ONLY valid JSON using this structure:

{{
  "name": null,
  "birthDate": null,
  "gender": null,
  "diagnosis": null,
  "medication": null,
  "allergy": null
}}

Rules:
- Do not invent information.
- If a value is missing, return null.
- Preserve clinically relevant wording.
- This is synthetic demonstration data only.

Medical record:

{record_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    return json.loads(result)