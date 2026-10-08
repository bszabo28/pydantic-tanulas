# 4. feladat – Tíz ügyfélüzenet

**Idő:** 75 perc. **Előfeltétel:** a 3. feladat agentje.

## Feladat

Használd a [minta_uzenetek.json](minta_uzenetek.json) tíz üzenetét. Ezek egyértelmű, hiányos, vegyes és többértelmű eseteket tartalmaznak.

1. Modellhívás előtt minden esethez írd le az elvárt `category`, `order_id` és `needs_clarification` értéket, rövid indoklással.
2. Futtasd az agentet minden üzenetre külön. Egy üzenet eredménye ne váljon a következő előzményévé.
3. Az eredményt a típusos mezők alapján hasonlítsd össze az elvárásokkal. Az összefoglalót tartalmilag értékeld; több megfogalmazás is elfogadható.
4. Írd ki az eltérő mezőket. Egy sikertelen futást külön jelölj, és folytasd a többi mintával.
5. Nézd meg külön a hiányzó rendelésazonosítót, a `"00123"` érték kezdő nulláit és az üzenetben szereplő számlaszámot.
6. Válassz egy többértelmű esetet, és valódi modellnél futtasd háromszor. Rögzítsd, változott-e a kategória vagy a visszakérdezés szükségessége.

## Kísérlet

Módosíts egyetlen utasítást, például pontosítsd, mit jelent a vegyes ügy. Futtasd újra ugyanazokat a mintákat, és írd le, mely esetekben segített a módosítás.

API-kulcs nélkül az előre megadott válaszok lejátszásával a feldolgozást gyakorolhatod. Ezt jelöld offline bemutatóként; a modell osztályozási minőségét nem méri.

## Leadandó

Táblázat az üzenetazonosítóval, a három elvárt mezővel, a kapott mezőkkel és az eltérés magyarázatával. Rögzítsd a modellazonosítót, a csomagverziókat és az utasítás változatát is.

## Elkészült, ha

Mind a tíz esetnek van eredménye vagy külön jelzett futási hibája. Meg tudod mutatni, hogy az elfogadott séma mellett is szükség van tartalmi összehasonlításra.
