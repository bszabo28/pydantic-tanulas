# 1. hét – Agent és strukturált kimenet

**Cél:** készíts egy ügyfélüzenetet osztályozó programot, amely `TicketAnalysis` objektumot ad vissza. A hét végén el tudod különíteni az adatvalidálást, a modell következtetését és az agent futtatását.

Ez a [tanulási terv](../TANULASI_TERV.md) első hetének gyakorlati anyaga, körülbelül **6 órára**. Az ügyfélszolgálati asszisztens ezen a héten szöveget elemez; rendelési adatforrást a második héten kap.

## Mappák és munkamód

- `feladatok/`: feladatleírások és bemenetek. Ezekkel kezdd.
- `megoldasok/`: futtatható Python-kód, elvárt elemzések és magyarázatok. Saját próbálkozás után nézd meg.

A saját kódodat például egy `sajat/` mappában készítsd el. A feladatok sorrendben egymásra épülnek; a megoldások közös sémát és agentet használnak.

| Sorrend | Feladat | Idő | Elkészülő eredmény |
| --- | --- | --- | --- |
| 1 | [TicketAnalysis séma](feladatok/01_ticket_analysis_sema.md) | 45 perc | Típusos adatmodell |
| 2 | [Öt helyes és öt hibás bemenet](feladatok/02_kezi_validacio.md) | 60 perc | Validálási riport és konverziós kísérlet |
| 3 | [Az első Agent](feladatok/03_elso_agent.md) | 60 perc | Strukturált kimenetű agent |
| 4 | [Tíz ügyfélüzenet](feladatok/04_tiz_uzenet.md) | 75 perc | Összehasonlítás saját elvárásokkal |
| 5 | [Futásvizsgálat és async](feladatok/05_futas_es_async.md) | 45 perc | Üzenetsor, használati adatok, két futtatási mód |
| 6 | [CLI és heti ellenőrzés](feladatok/06_cli_es_ellenorzes.md) | 75 perc | Parancssori program és saját magyarázat |

## Környezet

A parancsokat a repository gyökeréből futtasd. Ajánlott Python: **3.12**. A kód Python 3.12, Pydantic 2.14.0 és Pydantic AI 2.54.0 mellett lett ellenőrizve.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r het_01_agent_es_strukturalt_kimenet/requirements.txt -c het_01_agent_es_strukturalt_kimenet/requirements.lock
```

A `requirements.lock` az ellenőrzéshez telepített függőségek pontos verzióit rögzíti. Más operációs rendszeren a csomagkezelő az adott platformhoz illő csomagfájlokat választja.

Az OpenAI szolgáltatóhoz szükséges extra települ. Más szolgáltató használatakor a hozzá tartozó extrát és konfigurációt add hozzá a [telepítési útmutató](https://pydantic.dev/docs/ai/overview/install/#slim-install) szerint.

## Gyors próba a megoldásokkal

API-kulcs nélkül:

```bash
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.validacio
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli --offline "Hol van a 123-as rendelésem?"
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.mintak --offline
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.futas_vizsgalata
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.futas_vizsgalata --async
```

**Az offline mód előre megadott választ játszik le `TestModel` segítségével.** Az agent futását és a validálást lehet vele megfigyelni; a szövegmegértés minőségét valódi modellel vizsgáld. A CLI offline válasza minden bemenetre ugyanaz, a tíz mintás bemutató az adott mintához előre megírt választ használ. [TestModel](https://pydantic.dev/docs/ai/guides/testing/#unit-testing-with-testmodel).

Valódi modellhez állítsd be a `PYDANTIC_AI_MODEL` környezeti változót egy hozzáférhető `szolgáltató:modell` azonosítóra, vagy add át a `--model` argumentumot. A szolgáltató API-kulcsát a saját környezeti változójába tedd; OpenAI esetén ez `OPENAI_API_KEY`. Az érték nélküli `.env.example` minta nem töltődik be automatikusan.

```bash
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.cli "Hol van a 123-as rendelésem?"
python -m het_01_agent_es_strukturalt_kimenet.megoldasok.mintak
```

A tíz mintás futtatás mintánként külön futást indít. Az élő hívások a szolgáltatód használatát fogyasztják. A megoldásokhoz tartozó további parancsok a [megoldások útmutatójában](megoldasok/README.md) találhatók.

## A hét teljesítésének feltételei

- [ ] A tíz kézi bemenetből öt sikeres, öt hibás; meg tudod mutatni a hibás mezőt.
- [ ] Elmagyarázod a hiányzó mező, a `None` és az alapértelmezett érték különbségét.
- [ ] Az agent `TicketAnalysis` objektumot ad vissza, amelynek a mezőivel dolgozol.
- [ ] Összevetetted tíz ügyfélüzenet eredményét az előre leírt elvárásaiddal.
- [ ] Meg tudod különböztetni az üzenetsort, a modellkérések számát és a tokenhasználatot.
- [ ] A CLI sikeres futása 0-val, sikertelen futása nem nulla kóddal zárul.
- [ ] Be tudsz mutatni egy sémailag helyes, tartalmilag téves osztályozást.
- [ ] Öt mondatban összefoglaltad, melyik döntést a modell hozta, és mit ellenőrzött a Python-kód.

## Hivatalos olvasnivaló

- [Pydantic adatmodellek](https://pydantic.dev/docs/validation/latest/concepts/models/)
- [Agent és futtatás](https://pydantic.dev/docs/ai/core-concepts/agent/)
- [Strukturált kimenet](https://pydantic.dev/docs/ai/core-concepts/output/)
- [Futási eredmény API](https://pydantic.dev/docs/ai/api/pydantic-ai/run/)
