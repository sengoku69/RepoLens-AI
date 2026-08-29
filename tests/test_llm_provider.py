from types import SimpleNamespace

import pytest

from agents.llm_provider import LLMProvider


def test_ollama_provider_uses_default_configuration(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_API_KEY", "")
    monkeypatch.setenv("LLM_BASE_URL", "")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    provider = LLMProvider()

    info = provider.info()

    assert info["provider"] == "ollama"
    assert info["base_url"] == "http://localhost:11434/v1"
    assert info["model"] == "test-model"


def test_non_ollama_provider_requires_api_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("LLM_API_KEY", "")
    monkeypatch.setenv("LLM_BASE_URL", "")
    monkeypatch.setenv("LLM_MODEL", "gemini-test")

    with pytest.raises(
        ValueError,
        match="LLM_API_KEY is required",
    ):
        LLMProvider()


def test_generate_returns_response_content(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv(
        "LLM_BASE_URL",
        "http://localhost:11434/v1",
    )
    monkeypatch.setenv("LLM_MODEL", "test-model")

    provider = LLMProvider()

    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Test analysis response"
                )
            )
        ]
    )

    captured_request = {}

    def fake_create(**kwargs):
        captured_request.update(kwargs)
        return response

    monkeypatch.setattr(
        provider.client.chat.completions,
        "create",
        fake_create,
    )

    result = provider.generate(
        [
            {
                "role": "user",
                "content": "Analyze this repository.",
            }
        ]
    )

    assert result == "Test analysis response"
    assert captured_request["model"] == "test-model"
    assert captured_request["messages"][0]["role"] == "user"
    assert captured_request["temperature"] == 0.2


def test_generate_uses_reasoning_effort_for_gemini_3(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv(
        "LLM_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    monkeypatch.setenv(
        "LLM_MODEL",
        "gemini-3.6-flash",
    )

    provider = LLMProvider()

    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Gemini response"
                )
            )
        ]
    )

    captured_request = {}

    def fake_create(**kwargs):
        captured_request.update(kwargs)
        return response

    monkeypatch.setattr(
        provider.client.chat.completions,
        "create",
        fake_create,
    )

    result = provider.generate(
        [
            {
                "role": "user",
                "content": "Analyze this repository.",
            }
        ],
        temperature=0.8,
    )

    assert result == "Gemini response"
    assert captured_request["model"] == "gemini-3.6-flash"
    assert captured_request["reasoning_effort"] == "low"
    assert "temperature" not in captured_request


def test_generate_raises_on_empty_response(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv(
        "LLM_BASE_URL",
        "http://localhost:11434/v1",
    )
    monkeypatch.setenv("LLM_MODEL", "test-model")

    provider = LLMProvider()

    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=""
                )
            )
        ]
    )

    def fake_create(**kwargs):
        return response

    monkeypatch.setattr(
        provider.client.chat.completions,
        "create",
        fake_create,
    )

    with pytest.raises(
        RuntimeError,
        match="empty response",
    ):
        provider.generate(
            [
                {
                    "role": "user",
                    "content": "Analyze this repository.",
                }
            ]
        )


def test_info_returns_gemini_configuration(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("LLM_API_KEY", "test-key")
    monkeypatch.setenv(
        "LLM_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    monkeypatch.setenv(
        "LLM_MODEL",
        "gemini-3.6-flash",
    )

    provider = LLMProvider()

    info = provider.info()

    assert info["provider"] == "gemini"
    assert info["base_url"] == (
        "https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    assert info["model"] == "gemini-3.6-flash"