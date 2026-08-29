from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMProvider:
    def __init__(self) -> None:
        self.provider = os.getenv(
            "LLM_PROVIDER",
            "ollama",
        ).lower()

        self.api_key = os.getenv(
            "LLM_API_KEY",
            "",
        )

        self.base_url = os.getenv(
            "LLM_BASE_URL",
            "",
        )

        self.model = os.getenv(
            "LLM_MODEL",
            "",
        )

        self.client = self._create_client()

    def _create_client(self) -> OpenAI:
        if self.provider == "ollama":
            return OpenAI(
                api_key=self.api_key or "ollama",
                base_url=self.base_url
                or "http://localhost:11434/v1",
            )

        if not self.api_key:
            raise ValueError(
                "LLM_API_KEY is required for "
                f"provider '{self.provider}'."
            )

        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url or None,
        )

    def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        request = {
            "model": self.model,
            "messages": messages,
        }

        if not (
            self.provider == "gemini"
            and self.model.startswith("gemini-3.")
        ):
            request["temperature"] = temperature

        if (
            self.provider == "gemini"
            and self.model.startswith("gemini-3.")
        ):
            request["reasoning_effort"] = "low"

        response = self.client.chat.completions.create(
            **request
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return content

    def info(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "base_url": self.base_url
            or (
                "http://localhost:11434/v1"
                if self.provider == "ollama"
                else None
            ),
            "model": self.model,
        }


def get_llm() -> LLMProvider:
    return LLMProvider()