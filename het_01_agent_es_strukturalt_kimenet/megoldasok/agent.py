"""3. feladat: újrafelhasználható agentkonfiguráció."""

import os

from pydantic_ai import Agent
from pydantic_ai.models import Model
from pydantic_ai.models.test import TestModel

from .schemas import TicketAnalysis

PROMPT_VERSION = "het01-v1"
INSTRUCTIONS = """
Ügyfélüzenetet elemzel. Egy TicketAnalysis elemzést készíts.

Kategóriák:
- delivery: csomag, szállítás, kézbesítés, rendelés útjával kapcsolatos probléma.
- billing: számla, terhelés, fizetés, visszatérítés.
- other: más téma, nem eldönthető téma, vagy két egyformán hangsúlyos külön ügy.
Ha a szállítási és a számlázási panasz egyszerre, egyformán hangsúlyos,
a kategória other legyen, és needs_clarification legyen true.

A summary rövid, tényszerű magyar összefoglaló legyen, 5–160 karakterben.
Csak az üzenetben szereplő információt foglald össze. Ne ígérj megoldást,
és ne állíts ismeretlen rendelési állapotot vagy üzleti szabályt.

Az order_id kizárólag az egyértelműen rendelésazonosítóként megadott adat.
Őrizd meg szövegként a kezdő nullákat és a kötőjeleket is.
Ha nincs ilyen adat, order_id legyen null. Ne találj ki azonosítót.
A számlaszám nem rendelésazonosító.

A needs_clarification legyen true, ha a kérés többértelmű vagy vegyes,
illetve ha konkrét szállítási vagy számlázási ügyben hiányzik a rendelésazonosító.
Egy érthető általános kérdés és egy köszönet önmagában nem igényel visszakérdezést.
"""


def create_agent(model: Model | str) -> Agent[None, TicketAnalysis]:
    return Agent(
        model,
        output_type=TicketAnalysis,
        instructions=INSTRUCTIONS,
        # Egy kimenetjavítás engedélyezett; ismételt hiba lezárja a futást.
        retries={"output": 1},
    )


def resolve_model(model_name: str | None = None) -> str:
    name = (model_name if model_name is not None else os.getenv("PYDANTIC_AI_MODEL", "")).strip()
    if not name:
        raise ValueError(
            "Hiányzó modell: add meg a --model argumentumot vagy a "
            "PYDANTIC_AI_MODEL változót. API-kulcs nélküli próbához használd a --offline kapcsolót."
        )
    return name


def demo_model(*, invalid_output: bool = False) -> TestModel:
    """Rögzített válasz; az átadott ügyfélüzenetet nem elemzi."""
    output = {
        "category": "delivery",
        "summary": "Az ügyfél a 123-as rendelését keresi.",
        "order_id": "123",
        "needs_clarification": False,
    }
    if invalid_output:
        output["category"] = "invalid"
    return TestModel(custom_output_args=output)


if __name__ == "__main__":
    from pydantic_ai import models

    models.ALLOW_MODEL_REQUESTS = False
    agent = create_agent(demo_model())
    result = agent.run_sync("Hol van a 123-as rendelésem?")
    print("Offline bemutató: előre megadott válasz.")
    print("Kimeneti típus:", type(result.output).__name__)
    print("Kategória:", result.output.category)
    print("Rendelés:", result.output.order_id)
    print(result.output.model_dump_json(indent=2))
