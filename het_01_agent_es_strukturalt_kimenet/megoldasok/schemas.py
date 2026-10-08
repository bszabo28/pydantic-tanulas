"""1. feladat: a kimeneti szerződés, LLM nélkül."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketAnalysis(BaseModel):
    """Egy ügyfélüzenet kategóriája, összefoglalója és ismert azonosítója."""

    model_config = ConfigDict(extra="forbid")

    category: Literal["delivery", "billing", "other"] = Field(
        description="Szállítás: delivery; számlázás: billing; egyéb vagy vegyes ügy: other."
    )
    summary: str = Field(
        min_length=5,
        max_length=160,
        description="Rövid magyar összefoglaló az ügyfél üzenetéről, kitalált tény nélkül.",
    )
    order_id: str | None = Field(
        default=None,
        description="Az üzenetben megadott rendelésazonosító szövegként; hiány esetén None.",
    )
    needs_clarification: bool = Field(
        description="Szükséges-e további adat vagy a kérés pontosítása?"
    )


def main() -> None:
    import json

    data = {
        "category": "delivery",
        "summary": "Az ügyfél a késő csomagjáról érdeklődik.",
        "needs_clarification": True,
    }
    analysis = TicketAnalysis.model_validate(data)
    print("Kategória:", analysis.category)
    print("Kihagyott azonosító:", analysis.order_id)
    print("Python dict:", analysis.model_dump())
    print("JSON:", analysis.model_dump_json(indent=2))
    for order_id in (None, "00123"):
        example = TicketAnalysis.model_validate({**data, "order_id": order_id})
        print("Explicit azonosító:", repr(example.order_id))
    print("JSON-séma:")
    print(json.dumps(TicketAnalysis.model_json_schema(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
