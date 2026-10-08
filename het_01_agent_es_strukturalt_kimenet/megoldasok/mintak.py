"""4. feladat: tíz üzenet és a három tartalmi mező összehasonlítása."""

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import sys

from pydantic_ai import models
from pydantic_ai.exceptions import AgentRunError, UserError
from pydantic_ai.models.test import TestModel

from .agent import PROMPT_VERSION, create_agent, resolve_model
from .schemas import TicketAnalysis

CHECKED_FIELDS = ("category", "order_id", "needs_clarification")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tíz független ügyfélüzenet összehasonlítása.")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--model", help="Modellazonosító; egyébként PYDANTIC_AI_MODEL.")
    args = parser.parse_args(argv)
    if args.offline and args.model is not None:
        parser.error("Válassz egy futtatási módot: --offline vagy --model.")

    week = Path(__file__).resolve().parents[1]
    cases = json.loads((week / "feladatok" / "minta_uzenetek.json").read_text(encoding="utf-8"))
    expectations = json.loads(
        (week / "megoldasok" / "elvart_elemzesek.json").read_text(encoding="utf-8")
    )
    try:
        if args.offline:
            models.ALLOW_MODEL_REQUESTS = False
            agent = create_agent(TestModel())
            model_name = "TestModel (előre megadott válaszok)"
        else:
            model_name = resolve_model(args.model)
            agent = create_agent(model_name)
    except (ValueError, UserError) as error:
        print(f"Konfigurációs hiba: {error}", file=sys.stderr)
        return 2

    print(
        f"Modell: {model_name}; utasítás: {PROMPT_VERSION}; "
        f"pydantic: {version('pydantic')}; pydantic-ai-slim: {version('pydantic-ai-slim')}",
        file=sys.stderr,
    )
    if args.offline:
        print("OFFLINE: a bemutató a megadott válaszokat játssza le, nem mér szövegmegértést.", file=sys.stderr)

    matched = 0
    failed = 0
    for case in cases:
        expectation = expectations[case["id"]]
        expected = TicketAnalysis.model_validate(expectation["output"])
        try:
            if args.offline:
                with agent.override(model=TestModel(custom_output_args=expected.model_dump())):
                    result = agent.run_sync(case["uzenet"])
            else:
                result = agent.run_sync(case["uzenet"])
        except (AgentRunError, UserError, TimeoutError) as error:
            failed += 1
            print(f"{case['id']}: FUTÁSI HIBA – {type(error).__name__}")
            continue

        actual = result.output
        differences = {
            field: {"elvart": getattr(expected, field), "kapott": getattr(actual, field)}
            for field in CHECKED_FIELDS
            if getattr(expected, field) != getattr(actual, field)
        }
        if not differences:
            matched += 1
        print(f"\n{case['id']}: {'ELTÉRÉS' if differences else 'EGYEZÉS'} – {case['uzenet']}")
        print(actual.model_dump_json(indent=2))
        if differences:
            print(json.dumps(differences, ensure_ascii=False, indent=2))
        print("Indoklás:", expectation["indoklas"])
        print("Modellkérések:", result.usage.requests)

    print(f"\nÖsszesítés: {matched}/{len(cases)} egyezés, {failed} futási hiba.")
    print("Az összefoglalók tartalmi helyességét külön, kézzel ellenőrizd.")
    return 0 if matched == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
