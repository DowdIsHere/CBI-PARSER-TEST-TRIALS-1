"""Model adapters.

The executor model receives the seven read-engine documents as SEPARATE
system blocks, in the fixed load order — never concatenated into one blob.
"""

from __future__ import annotations

from typing import Protocol, Sequence

from .modules import Module

DEFAULT_MODEL = "claude-opus-4-8"


class ModelAdapter(Protocol):
    def generate(self, system_modules: Sequence[Module], user_prompt: str) -> str:
        """Run one pass. system_modules arrive as distinct, ordered blocks."""
        ...


class AnthropicAdapter:
    """Claude API adapter. One system text block per module preserves the
    module separation at the API level; the stable, ordered prefix is cached.
    """

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 64000):
        import anthropic  # deferred so tests never need the SDK

        self._client = anthropic.Anthropic()
        self._model = model
        self._max_tokens = max_tokens

    def generate(self, system_modules: Sequence[Module], user_prompt: str) -> str:
        system = [
            {"type": "text", "text": f"<module name=\"{m.name}\">\n{m.text}\n</module>"}
            for m in system_modules
        ]
        if system:
            system[-1]["cache_control"] = {"type": "ephemeral"}
        with self._client.messages.stream(
            model=self._model,
            max_tokens=self._max_tokens,
            thinking={"type": "adaptive"},
            system=system,
            messages=[{"role": "user", "content": user_prompt}],
        ) as stream:
            message = stream.get_final_message()
        return "".join(b.text for b in message.content if b.type == "text")


class ScriptedModel:
    """Test double: returns queued outputs in order and records every call."""

    def __init__(self, outputs: Sequence[str]):
        self._outputs = list(outputs)
        self.calls: list[dict] = []

    def generate(self, system_modules: Sequence[Module], user_prompt: str) -> str:
        self.calls.append(
            {
                "module_names": [m.name for m in system_modules],
                "user_prompt": user_prompt,
            }
        )
        if not self._outputs:
            raise AssertionError("ScriptedModel ran out of queued outputs")
        return self._outputs.pop(0)
