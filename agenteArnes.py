"""
Harness básico para un agente de IA con Anthropic Claude.

Incluye:
- Loop de conversación con tool calling
- Registro de herramientas extensible (decorador @tool)
- Manejo de errores y reintentos
- Historial de conversación persistente en memoria

Requisitos:
    pip install anthropic

Uso:
    export ANTHROPIC_API_KEY="tu-api-key"
    python agent_harness.py
"""

import os
import json
import time
import traceback
from typing import Any, Callable, Dict, List, Optional

import anthropic


# ---------------------------------------------------------------------------
# Registro de herramientas
# ---------------------------------------------------------------------------

class ToolRegistry:
    """Guarda las funciones que el agente puede invocar y sus esquemas JSON."""

    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._schemas: List[Dict[str, Any]] = []

    def tool(self, description: str, input_schema: Dict[str, Any]):
        """Decorador para registrar una función como herramienta del agente."""

        def decorator(func: Callable):
            name = func.__name__
            self._functions[name] = func
            self._schemas.append(
                {
                    "name": name,
                    "description": description,
                    "input_schema": input_schema,
                }
            )
            return func

        return decorator

    @property
    def schemas(self) -> List[Dict[str, Any]]:
        return self._schemas

    def call(self, name: str, tool_input: Dict[str, Any]) -> str:
        if name not in self._functions:
            return f"Error: herramienta '{name}' no encontrada."
        try:
            result = self._functions[name](**tool_input)
            return str(result)
        except Exception as e:
            return f"Error ejecutando '{name}': {e}"


registry = ToolRegistry()


# ---------------------------------------------------------------------------
# Herramientas de ejemplo (reemplazá/agregá las que necesites)
# ---------------------------------------------------------------------------

@registry.tool(
    description="Realiza una operación aritmética simple entre dos números.",
    input_schema={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"},
            "operacion": {
                "type": "string",
                "enum": ["suma", "resta", "multiplicacion", "division"],
            },
        },
        "required": ["a", "b", "operacion"],
    },
)
def calculadora(a: float, b: float, operacion: str) -> float:
    ops = {
        "suma": lambda: a + b,
        "resta": lambda: a - b,
        "multiplicacion": lambda: a * b,
        "division": lambda: a / b if b != 0 else float("inf"),
    }
    return ops[operacion]()


@registry.tool(
    description="Guarda una nota de texto en un archivo local llamado notes.txt.",
    input_schema={
        "type": "object",
        "properties": {"texto": {"type": "string"}},
        "required": ["texto"],
    },
)
def guardar_nota(texto: str) -> str:
    with open("notes.txt", "a", encoding="utf-8") as f:
        f.write(texto + "\n")
    return "Nota guardada correctamente."


# ---------------------------------------------------------------------------
# Harness del agente
# ---------------------------------------------------------------------------

class AgentHarness:
    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        system_prompt: str = "Sos un asistente útil con acceso a herramientas.",
        max_tokens: int = 1024,
        max_tool_iterations: int = 10,
    ):
        self.client = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY del entorno
        self.model = model
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.max_tool_iterations = max_tool_iterations
        self.history: List[Dict[str, Any]] = []

    def _call_model(self) -> anthropic.types.Message:
        """Llama a la API con reintentos simples ante errores transitorios."""
        for intento in range(3):
            try:
                return self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    system=self.system_prompt,
                    messages=self.history,
                    tools=registry.schemas,
                )
            except anthropic.APIStatusError as e:
                if e.status_code in (429, 529) and intento < 2:
                    time.sleep(2 ** intento)
                    continue
                raise

    def step(self, user_input: str) -> str:
        """Procesa un turno del usuario, incluyendo el loop de tool calling."""
        self.history.append({"role": "user", "content": user_input})

        for _ in range(self.max_tool_iterations):
            response = self._call_model()
            self.history.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                # Respuesta final de texto
                return "".join(
                    block.text for block in response.content if block.type == "text"
                )

            # Ejecutar cada bloque tool_use y devolver los resultados
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    output = registry.call(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output,
                        }
                    )
            self.history.append({"role": "user", "content": tool_results})

        return "Se alcanzó el límite de iteraciones de herramientas sin respuesta final."

    def run_repl(self):
        """Loop interactivo simple por consola."""
        print("Agente listo. Escribí 'salir' para terminar.\n")
        while True:
            user_input = input("Vos: ").strip()
            if user_input.lower() in ("salir", "exit", "quit"):
                break
            try:
                respuesta = self.step(user_input)
                print(f"\nAgente: {respuesta}\n")
            except Exception:
                print("\n[Error inesperado]")
                traceback.print_exc()


if __name__ == "__main__":
    agente = AgentHarness()
    agente.run_repl()
