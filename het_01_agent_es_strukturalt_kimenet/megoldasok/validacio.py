"""2. feladat: tíz kézi bemenet, konverzió és a séma korlátja."""

import json
from pathlib import Path

from pydantic import ValidationError

from .schemas import TicketAnalysis


def print_errors(error: ValidationError) -> None:
    for item in error.errors():
        location = ".".join(str(part) for part in item["loc"])
        print(f"  {location}: {item['type']} – {item['msg']}")


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "feladatok" / "validacio_bemenetek.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    accepted = 0
    rejected = 0
    for case in cases:
        try:
            analysis = TicketAnalysis.model_validate(case["adat"])
        except ValidationError as error:
            rejected += 1
            print(f"{case['id']}: ELUTASÍTVA")
            print_errors(error)
        else:
            accepted += 1
            print(f"{case['id']}: ELFOGADVA – {analysis.model_dump()}")
    print(f"\nÖsszesítés: {accepted} elfogadott, {rejected} elutasított.")

    converted_data = {**cases[0]["adat"], "needs_clarification": "false"}
    converted = TicketAnalysis.model_validate(converted_data)
    print("\nKonverzió: 'false' →", repr(converted.needs_clarification))
    try:
        TicketAnalysis.model_validate(converted_data, strict=True)
    except ValidationError as error:
        print("Ugyanez strict=True esetén:")
        print_errors(error)

    try:
        TicketAnalysis.model_validate({**cases[0]["adat"], "priority": "high"})
    except ValidationError as error:
        print("\nNem engedélyezett extra mező:")
        print_errors(error)

    wrong = TicketAnalysis.model_validate(
        {
            "category": "billing",
            "summary": "Az ügyfél a csomagja hollétéről érdeklődik.",
            "needs_clarification": True,
        }
    )
    print("\nSémailag elfogadott, de téves kategória a 'Hol van a csomagom?' üzenethez:")
    print(wrong.model_dump_json(indent=2))
    print("A séma nem vetette össze a kategóriát az eredeti üzenet jelentésével.")


if __name__ == "__main__":
    main()
