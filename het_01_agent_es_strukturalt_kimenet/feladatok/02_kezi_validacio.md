# 2. feladat – Öt helyes és öt hibás bemenet

**Idő:** 60 perc. **Előfeltétel:** az 1. feladat sémája.

## Feladat

A [validacio_bemenetek.json](validacio_bemenetek.json) tíz kézi adatot tartalmaz. Az első ötnek át kell mennie, az utolsó ötnek hibát kell adnia az első feladat sémájával.

1. Olvasd be a fájlt, és minden `adat` objektumra hívd meg a `TicketAnalysis.model_validate(...)` metódust.
2. Siker esetén írd ki az azonosítót és a validált adatot.
3. `ValidationError` esetén a többi bemenet feldolgozása folytatódjon. A `errors()` alapján írd ki a `loc`, `type` és `msg` értéket.
4. Készíts összesítést: elfogadott és elutasított bemenetek száma.
5. Írd le előre, majd ellenőrizd, mi történik, ha a `needs_clarification` mező értéke `"false"`. Ugyanazt az adatot validáld `strict=True` paraméterrel is.
6. Adj egy helyes bemenethez `priority="high"` mezőt, és nézd meg az `extra="forbid"` hatását.
7. Készíts egy sémailag helyes `billing` elemzést a „Hol van a csomagom?” üzenethez. Magyarázd el, miért fogadja el a Pydantic ezt a téves kategóriát.

## Leadandó

- Futtatható validálási program, modellhívás nélkül.
- Öt hibát leíró táblázat: bemenetazonosító, hibás mező, hiba oka.
- Két-három mondat a típuskonverzió és a szigorú validálás különbségéről.

## Elkészült, ha

Az összesítés 5 elfogadott és 5 elutasított bemenet, egy hiba nem szakítja meg a feldolgozást, és bemutatod, hogy a validálás nem ellenőrzi az eredeti üzenet jelentését.

**Tipp:** a `model_validate` megkapja az adatot, de ebben a feladatban nem kapja meg az ügyfélüzenetet.
