from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


RuntimeMode = Literal["local", "llm"]
LLMProviderName = Literal["ollama", "huggingface"]


@dataclass(frozen=True)
class Settings:
    runtime_mode: RuntimeMode = "local"
    llm_provider: LLMProviderName = "ollama"
    llm_model: str = "qwen3:14b"
    llm_api_key: str | None = None
    llm_base_url: str = "https://ollama.com"


def load_settings() -> Settings:
    _load_local_env()
    provider = _provider_name(os.getenv("ATSL_LLM_PROVIDER", "ollama"))
    return Settings(
        runtime_mode=_runtime_mode(os.getenv("ATSL_RUNTIME_MODE", "local")),
        llm_provider=provider,
        llm_model=_model_for(provider),
        llm_api_key=_api_key_for(provider),
        llm_base_url=_base_url_for(provider),
    )


def _runtime_mode(value: str) -> RuntimeMode:
    if value not in {"local", "llm"}:
        raise ValueError("ATSL_RUNTIME_MODE must be 'local' or 'llm'.")
    return value  # type: ignore[return-value]


def _provider_name(value: str) -> LLMProviderName:
    normalized = value.lower().replace("_", "-")
    if normalized not in {"ollama", "huggingface"}:
        raise ValueError("ATSL_LLM_PROVIDER must be 'ollama' or 'huggingface'.")
    return normalized  # type: ignore[return-value]


def _model_for(provider: LLMProviderName) -> str:
    explicit = os.getenv("ATSL_LLM_MODEL")
    if explicit:
        return explicit
    if provider == "huggingface":
        return os.getenv("ATSL_HUGGINGFACE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    return os.getenv("ATSL_OLLAMA_MODEL", "qwen3:14b")


def _api_key_for(provider: LLMProviderName) -> str | None:
    if provider == "huggingface":
        return os.getenv("ATSL_HUGGINGFACE_API_KEY")
    return os.getenv("ATSL_OLLAMA_API_KEY")


def _base_url_for(provider: LLMProviderName) -> str:
    if provider == "huggingface":
        return os.getenv("ATSL_HUGGINGFACE_BASE_URL", "https://router.huggingface.co/v1")
    return os.getenv("ATSL_OLLAMA_BASE_URL", "https://ollama.com")


def _load_local_env() -> None:
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
