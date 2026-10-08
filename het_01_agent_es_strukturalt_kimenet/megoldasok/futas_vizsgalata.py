"""5. feladat: szinkron és aszinkron futás, üzenetek és használat."""

import argparse
import asyncio
import json
import sys
from typing import TextIO

from pydantic_ai import Agent, models
from pydantic_ai.run import AgentRunResult

from .agent import create_agent, demo_model
from .schemas import TicketAnalysis


async def run_async(
    agent: Agent[None, TicketAnalysis], message: str
) -> AgentRunResult[TicketAnalysis]:
    return await agent.run(message)


def run_analysis(
    agent: Agent[None, TicketAnalysis], message: str, *, asynchronous: bool = False
) -> AgentRunResult[TicketAnalysis]:
    """CLI-belépés: saját event loopot csak aszinkron módban indítunk."""
    if asynchronous:
        return asyncio.run(run_async(agent, message))
    return agent.run_sync(message)


def inspect_run(result: AgentRunResult[TicketAnalysis], *, stream: TextIO = sys.stderr) -> None:
    usage = result.usage  # V2: tulajdonság, nem usage() metódus.
    print("\nHasználati adatok:", file=stream)
    print(f"Modellkérések: {usage.requests}", file=stream)
    print(f"Bemeneti tokenek: {usage.input_tokens}", file=stream)
    print(f"Kimeneti tokenek: {usage.output_tokens}", file=stream)
    print(f"Üzenetek: {len(result.all_messages())}", file=stream)
    print("Üzenetsor:", file=stream)
    messages = json.loads(result.all_messages_json())
    print(json.dumps(messages, ensure_ascii=False, indent=2), file=stream)


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline futásvizsgálat.")
    parser.add_argument("--async", dest="asynchronous", action="store_true")
    args = parser.parse_args()
    models.ALLOW_MODEL_REQUESTS = False
    agent = create_agent(demo_model())
    result = run_analysis(
        agent, "Hol van a 123-as rendelésem?", asynchronous=args.asynchronous
    )
    print("Offline bemutató; a tokenadatok tesztmodellből származnak.", file=sys.stderr)
    print(result.output.model_dump_json(indent=2))
    inspect_run(result)


if __name__ == "__main__":
    main()
