"""Target LLM adapters for real end-to-end security evaluation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import yaml

from src.adapti_guard.evaluation.llm_cache import LLMCache


@dataclass
class GenerationRequest:
    prompt: str
    system_prompt: str = ""
    model_id: str = ""
    temperature: float = 0.0
    max_tokens: int = 512
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    text: str
    model_id: str
    latency_ms: float
    cache_hit: bool = False
    usage: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class TargetModel(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise NotImplementedError

    def generate_batch(
        self,
        requests: list[GenerationRequest],
    ) -> list[GenerationResult]:
        return [self.generate(req) for req in requests]


class MockTargetModel(TargetModel):
    """Unit tests only — real experiments must not silently use this."""

    def __init__(self, response: str = "MOCK_RESPONSE"):
        self.response = response
        self.calls: list[GenerationRequest] = []

    def generate(self, request: GenerationRequest) -> GenerationResult:
        self.calls.append(request)
        return GenerationResult(
            text=self.response,
            model_id=request.model_id or "mock",
            latency_ms=0.0,
        )


class OpenAICompatibleTargetModel(TargetModel):
    """OpenRouter / OpenAI-compatible chat completions."""

    def __init__(
        self,
        model_id: str,
        *,
        base_url: str,
        api_key: str | None = None,
        api_key_env: str = "OPENROUTER_API_KEY",
        temperature: float = 0.0,
        max_tokens: int = 512,
        timeout_seconds: float = 120.0,
        max_retries: int = 3,
        retry_backoff_seconds: float = 2.0,
        cache: LLMCache | None = None,
    ):
        self.model_id = model_id
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv(api_key_env)
        self.api_key_env = api_key_env
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.cache = cache

        if not self.api_key:
            raise RuntimeError(
                f"{api_key_env} is not set. Real experiments are BLOCKED."
            )

        from openai import OpenAI

        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout_seconds,
        )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        model = request.model_id or self.model_id
        temperature = request.temperature if request.temperature is not None else self.temperature
        max_tokens = request.max_tokens or self.max_tokens

        cache_key = _cache_key(model, request.system_prompt, request.prompt, temperature, max_tokens)
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return GenerationResult(
                    text=cached["text"],
                    model_id=model,
                    latency_ms=0.0,
                    cache_hit=True,
                    usage=cached.get("usage", {}),
                    raw=cached.get("raw", {}),
                )

        messages: list[dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            start = time.perf_counter()
            try:
                response = self._client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                latency_ms = (time.perf_counter() - start) * 1000.0
                text = response.choices[0].message.content or ""
                usage: dict[str, Any] = {}
                if response.usage:
                    usage = {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }
                raw = {"id": getattr(response, "id", ""), "model": response.model}
                result = GenerationResult(
                    text=text,
                    model_id=model,
                    latency_ms=latency_ms,
                    usage=usage,
                    raw=raw,
                )
                if self.cache:
                    self.cache.set(cache_key, {"text": text, "usage": usage, "raw": raw})
                return result
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))

        return GenerationResult(
            text="",
            model_id=model,
            latency_ms=0.0,
            error=last_error or "unknown_error",
        )


OpenRouterTargetModel = OpenAICompatibleTargetModel


class OllamaTargetModel(TargetModel):
    """Local Ollama chat API."""

    def __init__(
        self,
        model_id: str,
        *,
        base_url: str = "http://localhost:11434",
        temperature: float = 0.0,
        max_tokens: int = 512,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
        retry_backoff_seconds: float = 1.0,
        cache: LLMCache | None = None,
    ):
        self.model_id = model_id
        self.base_url = base_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.cache = cache

    def generate(self, request: GenerationRequest) -> GenerationResult:
        import urllib.error
        import urllib.request

        model = request.model_id or self.model_id
        cache_key = _cache_key(model, request.system_prompt, request.prompt, self.temperature, self.max_tokens)
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return GenerationResult(
                    text=cached["text"],
                    model_id=model,
                    latency_ms=0.0,
                    cache_hit=True,
                    usage=cached.get("usage", {}),
                )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": request.system_prompt or "You are a helpful assistant."},
                {"role": "user", "content": request.prompt},
            ],
            "stream": False,
            "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        last_error: str | None = None
        for attempt in range(self.max_retries + 1):
            start = time.perf_counter()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                    body = json.loads(resp.read().decode("utf-8"))
                latency_ms = (time.perf_counter() - start) * 1000.0
                text = body.get("message", {}).get("content", "")
                usage = {
                    "prompt_tokens": body.get("prompt_eval_count", 0),
                    "completion_tokens": body.get("eval_count", 0),
                    "total_tokens": body.get("prompt_eval_count", 0) + body.get("eval_count", 0),
                }
                if self.cache:
                    self.cache.set(cache_key, {"text": text, "usage": usage})
                return GenerationResult(text=text, model_id=model, latency_ms=latency_ms, usage=usage)
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))

        return GenerationResult(text="", model_id=model, latency_ms=0.0, error=last_error)


def _cache_key(model: str, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> str:
    payload = json.dumps(
        {
            "model": model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_model_config(path: str | Path = "configs/models.yaml") -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_target_model(
    config_key: str,
    *,
    config_path: str | Path = "configs/models.yaml",
    cache: LLMCache | None = None,
    allow_mock: bool = False,
) -> TargetModel:
    cfg = load_model_config(config_path)
    models = cfg.get("models", {})
    if config_key not in models:
        raise KeyError(f"Unknown model config key: {config_key}")

    spec = models[config_key]
    provider = spec.get("provider", "openrouter")

    if provider == "mock":
        if not allow_mock:
            raise RuntimeError("MockTargetModel is not allowed for real experiments.")
        return MockTargetModel()

    cache_cfg = cfg.get("cache", {})
    llm_cache = cache
    if llm_cache is None and cache_cfg.get("enabled", True):
        llm_cache = LLMCache(Path(cache_cfg.get("directory", ".llm_cache")))

    if provider in {"openrouter", "openai_compatible"}:
        openrouter = cfg.get("openrouter", {})
        return OpenAICompatibleTargetModel(
            model_id=spec["model"],
            base_url=openrouter.get("base_url", "https://openrouter.ai/api/v1"),
            api_key_env=spec.get("api_key_env", "OPENROUTER_API_KEY"),
            temperature=float(spec.get("temperature", 0.0)),
            max_tokens=int(spec.get("max_tokens", 512)),
            timeout_seconds=float(openrouter.get("timeout_seconds", 120)),
            max_retries=int(openrouter.get("max_retries", 3)),
            retry_backoff_seconds=float(openrouter.get("retry_backoff_seconds", 2.0)),
            cache=llm_cache,
        )

    if provider == "ollama":
        ollama = cfg.get("ollama", {})
        return OllamaTargetModel(
            model_id=spec["model"],
            base_url=ollama.get("base_url", "http://localhost:11434"),
            temperature=float(spec.get("temperature", 0.0)),
            max_tokens=int(spec.get("max_tokens", 512)),
            timeout_seconds=float(ollama.get("timeout_seconds", 120)),
            cache=llm_cache,
        )

    raise ValueError(f"Unsupported provider: {provider}")
