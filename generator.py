from google import genai
import os
from dotenv import load_dotenv
from config import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_code(
    language: str,
    prompt: str,
    level: str = "intermediate",
    stream_placeholder=None,
    explain: bool = False,
    model: str = "models/gemini-2.5-flash",
) -> tuple[str, dict]:
    try:
        level_instruction = {
            "beginner": "Write simple, easy-to-understand code with many comments.",
            "intermediate": "Write clean, production-ready code with clear comments.",
            "production": "Write highly optimized, enterprise-grade code with full error handling, logging, and type hints.",
        }.get(level, "")

        explain_instruction = (
            "\n\nAfter the code block, add a section titled '## Explanation' "
            "that explains what each part does in simple terms."
            if explain else ""
        )

        full_prompt = (
            f"{SYSTEM_PROMPT}\n{level_instruction}{explain_instruction}\n\n"
            f"Language: {language}\nTask: {prompt}"
        )

        if stream_placeholder:
            # New SDK: use client.models.generate_content_stream()
            full_text = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=full_prompt,
            ):
                if chunk.text:
                    full_text += chunk.text
                    stream_placeholder.code(full_text, language=language.lower())
            return full_text, {}

        else:
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
            )
            meta = getattr(response, "usage_metadata", None)
            usage = {
                "prompt_tokens": getattr(meta, "prompt_token_count", "—"),
                "output_tokens": getattr(meta, "candidates_token_count", "—"),
            }
            return response.text or "No response generated.", usage

    except Exception as e:
        return f"# Error occurred\n# {str(e)}", {}
