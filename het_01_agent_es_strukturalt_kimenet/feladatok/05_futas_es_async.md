# 5. feladat – Futásvizsgálat és async

**Idő:** 45 perc. **Előfeltétel:** legalább egy sikeres agentfutás.

## Feladat

1. Futtass egy üzenetet `run_sync` segítségével, és jelenítsd meg az `all_messages()` eredményét.
2. Keresd meg a felhasználói kérést, az utasításokat, a modell válaszát és – ha jelen van – a kimeneti toolhívást, valamint a visszaadott eredményt.
3. Írd ki a futás modellkéréseinek számát, a bemeneti és kimeneti tokenhasználatot.
4. Készíts `async def` függvényt ugyanarra az üzenetre `await agent.run(...)` használatával. Parancssorból `asyncio.run(...)` indítsa.
5. Hasonlítsd össze a két futás kimenetének típusát. Offline, ugyanazzal az előre megadott válasszal a mezők is megegyeznek; valódi modellnél ez nem garantált.
6. Írd le, miért nem hívnád a `run_sync` metódust egy már futó event loopon belül, például egy aszinkron webvégpontban.

## Leadandó

- Egy szinkron és egy aszinkron futtatási példa.
- Egy annotált üzenetsor és a hozzá tartozó használati adatok.
- Rövid válasz: miért nem a lista elemszáma mondja meg a modellhívások számát?
- Rövid válasz: miért jelenhet meg toolhívás saját függvénytool nélkül?

## Elkészült, ha

Mindkét futtatási mód `TicketAnalysis` kimenetet ad, és az üzenetek alapján el tudod magyarázni, mi történt egy konkrét futásban.

**Verziótipp:** az ellenőrzött Pydantic AI V2 verzióban a használat `result.usage` tulajdonság. Régi V1 példákban `result.usage()` hívást is találhatsz.
