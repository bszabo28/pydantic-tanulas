# 6. feladat – CLI és heti ellenőrzés

**Idő:** 75 perc. **Előfeltétel:** az előző öt feladat.

## Feladat

Készíts parancssorból futtatható programot a korábbi adatmodell és agent felhasználásával.

1. Az ügyfélüzenet pozicionális argumentum legyen; az üres vagy csak szóközt tartalmazó üzenetet utasítsd el.
2. Támogasd a `--model` argumentumot, alapértelmezése a `PYDANTIC_AI_MODEL` környezeti változó. Hiányzó konfiguráció esetén adj érthető hibát a modellhívás előtt.
3. Legyen `--offline` kapcsoló API-kulcs nélküli bemutatóhoz. Világosan írd ki, hogy előre megadott válasz fut.
4. A sikeres kimenetet a `result.output.model_dump_json(...)` segítségével írd a standard kimenetre.
5. `--inspect` esetén írd az üzenetsort és a használati adatokat a standard hibakimenetre, így a JSON külön feldolgozható marad.
6. Támogasd a `--async` kapcsolót `await agent.run(...)` alapú futáshoz.
7. Hibás konfiguráció esetén 2, sikertelen agentfutás esetén 1, siker esetén 0 legyen a kilépési kód. Hibánál ne készíts sikeresnek látszó `TicketAnalysis` objektumot.
8. A használati hibát, a szolgáltatói hibát és az érvénytelen modellválaszt felismerhető szöveggel jelezd. Ellenőrizd a hibautat offline úgy, hogy a tesztmodell rendre hibás kategóriát adjon vissza.

## Kipróbálandó helyzetek

- Egy azonosítót tartalmazó szállítási kérdés.
- Hiányos kérdés és vegyes ügy.
- Üres üzenet és hiányzó modellkonfiguráció.
- Ismételten érvénytelen modellválasz: a program hibakóddal álljon le.
- Szinkron és aszinkron offline futás.

## Leadandó

A CLI, rövid futtatási útmutató és a hibautak kipróbálásának eredménye. Írj öt saját mondatot az alábbiakról:

1. Mit ír le a Pydantic adatmodell?
2. Mit dönt el az LLM?
3. Mit szervez az Agent?
4. Miért nem garantál helyes kategóriát a strukturált kimenet?
5. Milyen hibát jelez a program, és milyen adatot nem találhat ki?

## Elkészült, ha

A program parancssorból fut, típusos eredményt használ, a hibás futás hibakóddal zárul, és saját példával elmagyarázod a séma és a jelentés különbségét.
