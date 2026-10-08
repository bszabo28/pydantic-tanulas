# 1. feladat – TicketAnalysis séma

**Idő:** 45 perc. **Előfeltétel:** magabiztos Python; most még nem kell LLM vagy API-kulcs.

## Feladat

Írj egy `TicketAnalysis` nevű Pydantic `BaseModel` osztályt az alábbi szerződéssel.

| Mező | Típus és szabály | Kötelező? |
| --- | --- | --- |
| `category` | `Literal["delivery", "billing", "other"]` | Igen |
| `summary` | Szöveg, legalább 5 és legfeljebb 160 karakter | Igen |
| `order_id` | Szöveg vagy `None`; alapértelmezése `None` | Nem |
| `needs_clarification` | Logikai érték | Igen |

1. Minden mezőhöz adj magyar `Field(description=...)` leírást.
2. Tiltsd a fel nem sorolt mezőket `extra="forbid"` konfigurációval.
3. Készíts objektumot ebből a kézi adatból:

   ```python
   {
       "category": "delivery",
       "summary": "Az ügyfél a késő csomagjáról érdeklődik.",
       "needs_clarification": True,
   }
   ```

4. Írd ki a `category` és az `order_id` mezőt, a `model_dump()` eredményét, valamint a `model_dump_json(indent=2)` eredményét.
5. Próbáld ki külön a kihagyott `order_id` mezőt, az explicit `None`-t és a `"00123"` értéket. Az utolsó maradjon szöveg, a kezdő nullákkal együtt.
6. Nézd meg a `model_json_schema()` eredményét. Keresd meg a kötelező mezőket és a kategóriák felsorolását.

## Leadandó

- Az adatmodell és egy rövid, futtatható bemutató.
- Saját válasz: miért nem ugyanaz a `str | None` és a `str | None = None`?
- Saját válasz: a séma önmagában eldönti-e, hogy egy ügyfélüzenet `delivery` kategóriájú?

## Elkészült, ha

A kihagyott rendelésazonosító `None`, a hibás kategória elutasítást kap, és a Python-objektumot külön tudod választani a belőle készített JSON-szövegtől.

**Tipp:** `BaseModel`, `Field`, `ConfigDict`, `Literal`. A tartalmi osztályozási szabályokkal a harmadik feladatban foglalkozol.
