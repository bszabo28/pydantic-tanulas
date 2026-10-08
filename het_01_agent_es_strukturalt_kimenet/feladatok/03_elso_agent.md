# 3. feladat – Az első Agent

**Idő:** 60 perc. **Előfeltétel:** működő séma és kézi validálás.

## Feladat

Készíts egy `create_agent(model)` függvényt, amely `TicketAnalysis` kimenetű agentet hoz létre. A modell argumentumból érkezzen, az utasításokat te írd meg. Ezen a héten nem kell saját függvénytool vagy dependency.

Az osztályozás gyakorlóprojektbeli szabályai:

- `delivery`: csomag, szállítás, kézbesítés, rendelés útjával kapcsolatos probléma.
- `billing`: számla, terhelés, fizetés vagy visszatérítés.
- `other`: más téma, illetve nem eldönthető vagy két külön problémát egyformán hangsúlyozó üzenet.
- A `summary` rövid magyar összefoglaló legyen. Ne ígérjen megoldást, és ne állítson ismeretlen rendelési állapotot.
- Az `order_id` kizárólag a szövegben egyértelműen rendelésazonosítóként megadott adat legyen. Hiány esetén `None`; számlaszámot ne kezelj rendelésazonosítóként.
- Konkrét szállítási vagy számlázási ügy azonosító nélkül visszakérdezést igényel. Többértelmű és vegyes ügy szintén. Egy érthető általános kérdés vagy köszönet nem igényel visszakérdezést.

1. Állítsd be az `instructions` és az `output_type` paramétert.
2. Adj át a függvénynek modellobjektumot is: offline próbához használhatsz `TestModel(custom_output_args=...)` példányt egy kézzel megadott helyes elemzéssel.
3. `run_sync` segítségével futtasd: „Hol van a 123-as rendelésem?”
4. Ellenőrizd a `result.output` típusát, és a mezőit közvetlenül használd.
5. Valódi modell használatakor a modellazonosító környezeti változóból vagy argumentumból jöjjön. Az API-kulcs a szolgáltató környezeti változójában legyen.

## Leadandó

- Agentet létrehozó függvény és egy futtatási példa.
- Saját magyarázat az `instructions`, `output_type` és `result.output` szerepéről.
- Egy mondat arról, mit bizonyít a `TestModel` próba, és mit kell valódi modellel ellenőrizni.

## Elkészült, ha

A kimenet `TicketAnalysis` példány, a saját kódod mezőket olvas belőle, és a hiányzó rendelésazonosító pótlását az utasítás nem engedi meg.

**Tipp:** a strukturált kimenet az üzenetsorban megjelenhet kimeneti toolhívásként akkor is, ha nem regisztráltál saját Python-függvénytoolt.
