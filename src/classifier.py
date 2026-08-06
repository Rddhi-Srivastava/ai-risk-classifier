"""
Core classification logic: sends a system description to Gemini and
returns a validated, structured result.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List

from google import genai

from prompt import SYSTEM_PROMPT, build_user_message

VALID_TIERS = {"prohibited", "high-risk", "limited-risk", "minimal-risk"}
VALID_CONFIDENCE = {"high", "medium", "low"}

REQUIRED_KEYS = {
    "tier",
    "confidence",
    "primary_article_or_annex",
    "reasoning",
    "documentation_checklist",
    "borderline",
    "borderline_note",
}


class ClassificationError(Exception):
    """Raised when the model response can't be parsed or fails validation."""


@dataclass
class ClassificationResult:
    tier: str
    confidence: str
    primary_article_or_annex: str
    reasoning: str
    documentation_checklist: List[str]
    borderline: bool
    borderline_note: str
    system_description: str = ""
    raw_response: str = field(default="", repr=False)


def _get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ClassificationError(
            "GEMINI_API_KEY environment variable is not set. "
            "Get a free key at https://aistudio.google.com/apikey and set it, "
            "e.g. export GEMINI_API_KEY='your-key-here'"
        )
    return genai.Client(api_key=api_key)


def _strip_code_fences(text: str) -> str:
    """Gemini sometimes wraps JSON in ```json ... ``` even when told not to."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return text


def _validate(data: dict) -> None:
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ClassificationError(f"Model response missing required keys: {missing}")

    if data["tier"] not in VALID_TIERS:
        raise ClassificationError(
            f"Invalid tier '{data['tier']}'. Must be one of {VALID_TIERS}"
        )
    if data["confidence"] not in VALID_CONFIDENCE:
        raise ClassificationError(
            f"Invalid confidence '{data['confidence']}'. Must be one of {VALID_CONFIDENCE}"
        )
    if not isinstance(data["documentation_checklist"], list):
        raise ClassificationError("documentation_checklist must be a list")
    if not isinstance(data["borderline"], bool):
        raise ClassificationError("borderline must be a boolean")


def classify_system(
    system_description: str,
    model: str = "gemini-2.5-flash-lite",
    max_retries: int = 2,
) -> ClassificationResult:
    """
    Sends a plain-language AI system description to Gemini and returns a
    validated ClassificationResult.

    Raises ClassificationError if the model output can't be parsed/validated
    after retries.
    """
    if not system_description or not system_description.strip():
        raise ClassificationError("system_description cannot be empty")

    client = _get_client()
    user_message = build_user_message(system_description)

    last_error = None
    for attempt in range(max_retries + 1):
        response = client.models.generate_content(
            model=model,
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.1,  # low temperature: we want consistent, repeatable classification
                "response_mime_type": "application/json",
            },
        )
        raw_text = response.text or ""

        try:
            cleaned = _strip_code_fences(raw_text)
            data = json.loads(cleaned)
            _validate(data)
            return ClassificationResult(
                tier=data["tier"],
                confidence=data["confidence"],
                primary_article_or_annex=data["primary_article_or_annex"],
                reasoning=data["reasoning"],
                documentation_checklist=data["documentation_checklist"],
                borderline=data["borderline"],
                borderline_note=data.get("borderline_note", ""),
                system_description=system_description,
                raw_response=raw_text,
            )
        except (json.JSONDecodeError, ClassificationError) as e:
            last_error = e
            continue  # retry

    raise ClassificationError(
        f"Failed to get a valid classification after {max_retries + 1} attempts. "
        f"Last error: {last_error}. Last raw response: {raw_text[:500]}"
    )


if __name__ == "__main__":
    # Quick manual smoke test: python classifier.py "some description"
    import sys

    description = (
        " ".join(sys.argv[1:])
        or "An AI tool that scans job applicants' CVs and ranks them for recruiters."
    )
    result = classify_system(description)
    print(json.dumps(result.__dict__, indent=2))
