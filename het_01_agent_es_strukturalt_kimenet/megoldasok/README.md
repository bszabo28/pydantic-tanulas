# Megoldások – 1. hét

Először próbáld meg a [feladatokat](../README.md) saját kóddal. Itt egy lehetséges megoldást és a fontos megértési kérdések válaszát találod. A környezet telepítését a heti útmutató írja le; minden parancs a repository gyökeréből indul.

| Feladat | Megoldás | Futtatás |
| --- | --- | --- |
| 1. Séma | [schemas.py](schemas.py) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.schemas` |
| 2. Validálás | [validacio.py](validacio.py) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.validacio` |
| 3. Agent | [agent.py](agent.py) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.agent` |
| 4. Tíz üzenet | [mintak.py](mintak.py), [elvárt elemzések](elvart_elemzesek.json) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.mintak --offline` |
| 5. Futás, async | [futas_vizsgalata.py](futas_vizsgalata.py) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.futas_vizsgalata --async` |
| 6. CLI | [cli.py](cli.py) | `python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline "Hol van a 123-as rendelésem?"` |

## 1. Adatmodell

A `str | None` típus megengedi a `None` értéket, de alapértelmezés nélkül a mező továbbra is kötelező. A `default=None` teszi elhagyhatóvá. A rendelésazonosító szöveg, ezért a `"00123"` kezdő nullái megmaradnak.

A `model_dump()` Python-szótárt, a `model_dump_json()` JSON-szöveget ad vissza. A modell a megengedett formát ellenőrzi; egy ügyfélüzenet kategóriáját nem választja ki.

## 2. Kézi validálás

Az első öt bemenet helyes. Az utolsó öt hibája:

| Azonosító | Mező | Hibatípus | Ok |
| --- | --- | --- | --- |
| V06 | `category` | `literal_error` | A `refund` nem megengedett kategória. |
| V07 | `summary` | `missing` | Hiányzik a kötelező összefoglaló. |
| V08 | `summary` | `string_too_short` | Az `ok` rövidebb öt karakternél. |
| V09 | `needs_clarification` | `bool_parsing` | A `talán` nem alakítható logikai értékké. |
| V10 | `order_id` | `string_type` | Szöveg helyett egész szám érkezett. |

Normál validáláskor a `"false"` szöveg `False` értékké alakul. `strict=True` esetén ez a bemenet `bool_type` hibát ad. A `priority` extra mező `extra_forbidden` hibát okoz. Az alap séma tehát nem minden mezőnél végez ugyanazt a konverziót.

A hibás kategóriájú, de érvényes objektum azt mutatja meg, hogy a Pydantic által elfogadott érték lehet tartalmilag téves. Az osztályozáshoz az eredeti szöveget is értelmezni kell.

## 3. Agent

A `create_agent` közös utasításokat és `TicketAnalysis` kimeneti típust állít be. A `result.output` már validált Python-objektum: közvetlenül olvasható például a `category` mezője. [Agent](https://pydantic.dev/docs/ai/core-concepts/agent/).

A `demo_model` ugyanazt az előre megírt elemzést adja minden ügyfélüzenetre. A valódi modellhasználathoz válaszd ki a szolgáltatót és a modellt a `PYDANTIC_AI_MODEL` vagy a `--model` segítségével.

## 4. Tíz üzenet

Az elvárt elemzések a harmadik feladat szabályait követik. A vegyes ügy (`U07`) itt `other`, visszakérdezéssel; más alkalmazás más szabályt is választhat. `U09` számlaszáma az összefoglalóban megjelenhet, de nem lesz rendelésazonosító.

A program a kategóriát, az azonosítót és a visszakérdezést hasonlítja össze. Az összefoglaló pontos szövegegyezését nem követeli meg. Az offline eredmények előre megadott válaszok lejátszásai; minőségvizsgálathoz futtasd a `mintak` modult `--offline` nélkül.

## 5. Üzenetek és két futtatási mód

A bemutatóban a kérésben megtalálod a felhasználói szöveget és az utasításokat. A válaszban a strukturált adat kimeneti toolhívásként érkezik, majd annak visszaigazolása is szerepel az üzenetsorban. Ez a kimeneti formátum része. Saját üzleti függvénytoolt ezen a héten nem adtunk hozzá. [Strukturált kimenet](https://pydantic.dev/docs/ai/core-concepts/output/#tool-output).

A `result.usage.requests` a modellkérések száma; az `all_messages()` többféle üzenetet tartalmaz. A tesztmodell tokenadatai bemutatóadatok, valódi költségbecsléshez ne használd őket.

A `run_sync` blokkoló belépési pont. Az aszinkron példa `await agent.run(...)` segítségével fut; a CLI számára az `asyncio.run` hozza létre az event loopot. Már aszinkron környezetben közvetlenül a `run_async` függvényt vagy az `agent.run` metódust várd meg `await`-tel.

## 6. CLI és hibák

A JSON a standard kimenetre, a bemutató jelzése, a hibák és az opcionális futásvizsgálat a standard hibakimenetre kerülnek.

```bash
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline --inspect "Hol van a 123-as rendelésem?"
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline --async "Hol van a 123-as rendelésem?"
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline --simulate-invalid-output "Hol van a rendelésem?"
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline "   "
env -u PYDANTIC_AI_MODEL python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli "Hol van a rendelésem?"
```

Az első két parancs 0-val, az érvénytelen kimenet 1-gyel, az utolsó kettő 2-vel zárul. A kilépési kódot közvetlenül a parancs után `echo $?` mutatja meg. Az érvénytelen kimenet egy javítási próbát kap, majd a futás hibával lezárul; sikeresnek látszó objektum nem keletkezik. A használati limitek és az összetett retrykezelés a harmadik hét témái.

A heti magyarázatot írd meg saját szavaiddal. Egy lehetséges, öt mondatból álló minta:

1. A Pydantic modell leírja a mezőket és az elfogadható értékeket.
2. Az LLM az ügyfélüzenet jelentéséből következtet a kategóriára és a hiányzó adatokra.
3. Az Agent összekapcsolja az utasítást, a modellt, a futást és a kimenet validálását.
4. Egy `billing` kategória megengedett érték, ezért a csomagkeresés téves besorolása is lehet sémailag helyes.
5. A CLI jelzi a sikertelen futást, és az azonosító hiányát `None` értékkel kell megőrizni.
