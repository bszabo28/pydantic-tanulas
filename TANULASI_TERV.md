# Pydantic AI tanulási terv production használathoz

A cél, hogy önállóan tudj Pydantic AI alkalmazást tervezni, a futását megmagyarázni, a hibáit reprodukálni, a válaszainak minőségét mérni és a szolgáltatást üzemeltetni. A terv magabiztos Python-tudásra és heti 5–7 óra tanulásra épül. Nyolc hétre körülbelül 50 óra munkát tervezünk; a továbblépést minden héten egy működő feladat és egy megértési ellenőrzés határozza meg.

Végig egy ügyfélszolgálati asszisztenst fejlesztesz. Először egy üzenetet sorol kategóriába, később rendelési adatokat és tudásbázist kérdez le, majd egy tesztelhető API részeként fut. Az adatokat kezdetben helyi minták adják; így a keretrendszer működésére tudsz figyelni.

## A működés alapmodellje

A Pydantic AI az LLM köré szervezett, típusos futtatási keret. Egy `Agent` összekapcsolja a modellt, az utasításokat, a meghívható Python-függvényeket és az elvárt kimeneti típust. A dependency rendszer a saját szolgáltatásaidat és a kéréshez tartozó adatokat adja át ezeknek a függvényeknek. [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/), [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/).

Egy tipikus futás menete:

1. Az alkalmazás átadja a felhasználói kérést, az utasításokat és a rendelkezésre álló toolok leírását a modellnek.
2. A modell választ ad vagy egy tool meghívását kéri, annak argumentumaival együtt.
3. A keretrendszer ellenőrzi az argumentumokat, és a saját Python-kódod végrehajtja a toolt.
4. A tool eredménye visszakerül a modellhez. Ez a ciklus többször ismétlődhet.
5. A végső kimenet az előírt típus és a hozzáadott validátorok ellenőrzésén megy át. Javítható hiba esetén újabb modellpróba következhet; az újrapróbálkozások és használati limitek kimerülése hibával lezárhatja a futást. [Function Tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/), [Output](https://pydantic.dev/docs/ai/core-concepts/output/).

A modell javasolja a toolhívást; a jogosultságot és az üzleti szabályok betartását a saját kódodnak kell biztosítania. A sémának megfelelő válasz továbbra is tartalmazhat téves állítást. Ezért a production cél három külön feladatot jelent: helyes program, megfelelő modellviselkedés és ellenőrizhető üzemeltetés.

| Fogalom | Mit jelent a gyakorlóprojektben? |
| --- | --- |
| Modell | A szövegből következtető, válaszokat és toolhívásokat javasló LLM. |
| Agent | A konfiguráció és a modell–tool ciklus kerete. |
| Instructions | A kategorizálás, visszakérdezés és válaszadás szabályai. |
| Tool | Például egy rendelést lekérdező Python-függvény. |
| Dependencies | A hitelesített ügyfél azonosítója, repository és szolgáltatáskliensek. |
| Output | Az alkalmazás által feldolgozható, validált eredmény. |
| Run | Egy konkrét kérés feldolgozása; több modellhívást is tartalmazhat. |
| Conversation | Több futás összekapcsolt üzenettörténete. |

## Időbeosztás és tanulási módszer

Minden héten tarts három alkalmat: körülbelül egy óra dokumentáció és saját jegyzet, három óra implementáció, majd két óra kísérletezés, ellenőrzés és hibakeresés. A két hosszabb alkalom szükség esetén szétbontható.

A hét végén írj öt mondatot arról, hogyan működik az új rész. Egy konkrét hiba bemutatásával magyarázd el, hol születik a döntés, hol történik az ellenőrzés és milyen adat kerül vissza a modellhez. Amit csak egy bemásolt példa segítségével tudsz elmagyarázni, azt ismételd meg kisebb feladaton.

| Hét | Fókusz | Elkészülő eredmény | Tervezett idő |
| --- | --- | --- | --- |
| 1 | Agent és strukturált kimenet | Típusos üzenetosztályozó | 6 óra |
| 2 | Toolok és dependencies | Rendelési adatokat használó asszisztens | 6 óra |
| 3 | Validáció és hibakezelés | Korlátozott és ellenőrzött futás | 6 óra |
| 4 | Előzmények és tudásbázis | Többfordulós, forrásokra támaszkodó válaszadás | 6 óra |
| 5 | Determinisztikus tesztelés | Offline tesztcsomag hibaforgatókönyvekkel | 6 óra |
| 6 | Evals és modellválasztás | Mérhető minőség és összehasonlítható változatok | 7 óra |
| 7 | Async API és megfigyelhetőség | Nyomon követhető, terhelhető szolgáltatás | 6 óra |
| 8 | Biztonság és kiadás | Staging kiadás és üzemeltetési leírás | 7 óra |

## Verziók és környezet

A tanulási út a 2026. október 8-án elérhető Pydantic AI V2 dokumentációjához igazodik. A Pydantic adatvalidáló könyvtár és a Pydantic AI külön csomag, önálló verziózással. Régi oktatóanyag használatakor ellenőrizd, hogy a benne szereplő API és alapértelmezett működés megegyezik-e a telepített verzióddal. [Upgrade Guide](https://pydantic.dev/docs/ai/project/changelog/).

Kezdéskor hozz létre projektkörnyezetet, és rögzítsd a feloldott függőségeket lockfile-ban. Új projekthez Python 3.12 megfelelő kiindulás; a dokumentált minimum Python 3.10. Az első hetekben elég a `pydantic-ai`, egy választott szolgáltató és a fejlesztői ellenőrzésekhez szükséges eszközök. A szolgáltatóspecifikus extrákat az installációs útmutató alapján válaszd. [Installation](https://pydantic.dev/docs/ai/overview/install/).

A modell azonosítója konfigurációból érkezzen. Az API-kulcs környezeti változóba kerüljön, a repositoryba pedig kizárólag érték nélküli konfigurációs minta. Minden mérés mellé jegyezd fel a modellazonosítót, a prompt verzióját és a csomagverziókat. Így egy későbbi változás eredetét is meg tudod vizsgálni.

## 1 hét Agent és strukturált kimenet

**Megértési cél:** el tudd különíteni a Pydantic adatmodelljét, az LLM-et és az agent futtatását.

Először ismételd át a `BaseModel`, `Field`, `Literal`, opcionális mezők, `model_validate` és `model_dump` működését. Külön figyeld meg, mikor történik típuskonverzió, és mikor szeretnél szigorú validációt. Ezután tanuld meg az `Agent`, `instructions`, `output_type`, `run`, `run_sync` és `result.output` szerepét. [Pydantic Models](https://pydantic.dev/docs/validation/latest/concepts/models/), [Agents](https://pydantic.dev/docs/ai/core-concepts/agent/).

**Gyakorlat, ebben a sorrendben:**

1. Írj `TicketAnalysis` sémát a következő adatokkal: kategória, rövid összefoglaló, opcionális rendelésazonosító és szükséges-e visszakérdezés. A kategóriát korlátozd például `delivery`, `billing`, `other` értékekre.
2. Validálj kézzel öt helyes és öt hibás bemenetet, modellhívás nélkül. Figyeld meg a hiba helyét és okát.
3. Készíts egy toolok nélküli agentet, amely ügyfélüzenetből ezt a típust állítja elő.
4. Próbáld ki egyértelmű, hiányos és többértelmű üzenettel. A hiányzó rendelésazonosító maradjon hiányzó adat.
5. Vizsgáld meg egy futás üzeneteit és használati adatait. Írd le, miért különbözik a `run_sync` használata az aszinkron `run` hívásától.

**Elkészül:** parancssorból futtatható üzenetosztályozó és tíz mintabemenet.

**Továbblépési feltétel:** el tudod magyarázni, hogyan lehet egy válasz sémailag helyes, miközben a kategorizálása téves. A program a típusos eredmény mezőivel dolgozik, és kezeli a sikertelen futást.

## 2 hét Toolok és dependencies

**Megértési cél:** tudd követni, hogyan jut el a modell által javasolt függvényhívás a saját Python-kódodig.

Tanuld meg a `@agent.tool`, `@agent.tool_plain`, `RunContext[Deps]`, `deps_type` és futáskor átadott `deps` kapcsolatát. A tool neve, paraméterei és docstringje segítik a modellt a megfelelő hívás kiválasztásában. A dependencies objektumot a saját alkalmazásod adja át; a modell azt nem kapja meg automatikusan teljes egészében. [Function Tools](https://pydantic.dev/docs/ai/tools-toolsets/tools/), [Dependencies](https://pydantic.dev/docs/ai/core-concepts/dependencies/).

**Gyakorlat:**

1. Készíts memóriában tárolt rendelési repositoryt három rendeléssel és két ügyféllel.
2. Hozz létre `Deps` dataclass-t a repositoryval és a hitelesített ügyfél azonosítójával.
3. Írj egy `get_order_status` toolt. Az azonosító a modell argumentuma lehet, a hozzáférést azonban a repository az átadott ügyfél alapján ellenőrizze.
4. Külön kezeld a nem található rendelést és a tiltott hozzáférést. A modellnek csak a válaszadáshoz szükséges adatokat add vissza.
5. Nézd végig a kérés → toolhívás → tooleredmény → végső válasz üzenetsort. Próbáld ki tool nélküli kérdéssel is.

**Elkészül:** asszisztens, amely saját adatforrásból válaszol egy rendelés állapotára.

**Továbblépési feltétel:** másik ügyfél rendelésadata a tool közvetlen meghívásával sem kérdezhető le. El tudod magyarázni, miért különböző a `deps_type=Deps` és a `deps=deps_instance` szerepe.

## 3 hét Validáció és hibakezelés

**Megértési cél:** külön tudd kezelni a modell javítható tévedését, az üzleti elutasítást és a külső szolgáltatás hibáját.

Tanuld meg a Pydantic validátorokat, az agent `output_validator` lehetőségét és a `ModelRetry` szerepét. Ismerd meg a strukturált kimenet tool, native és prompted változatát; választáskor vizsgáld meg a modell támogatását. A `ModelRetry` visszajelzést adhat a modellnek, a hálózati retry és a teljes futás időkorlátja külön felelősség. [Validators](https://pydantic.dev/docs/validation/latest/concepts/validators/), [Output](https://pydantic.dev/docs/ai/core-concepts/output/), [Retries](https://pydantic.dev/docs/ai/core-concepts/retries/), [Timeouts](https://pydantic.dev/docs/ai/core-concepts/timeouts/).

**Gyakorlat:**

1. Tervezd meg a sikeres válasz, a visszakérdezés és az emberhez továbbítás külön kimeneti eseteit.
2. Ellenőrizd, hogy a válaszban megadott rendelésazonosító és állapot összhangban van-e a repository adatával. A szabályokat külön, tesztelhető Python-függvényekben írd meg.
3. Határozd meg a modellkérések és toolhívások felső korlátját, valamint a teljes futás és a külső I/O időkorlátját.
4. Szimulálj hibás toolargumentumot, ismétlődő rossz kimenetet, 429 választ, szolgáltatói kiesést és időtúllépést. Először ellenőrzött tesztdublákkal vizsgáld ezeket.
5. Döntsd el esetenként, mikor javítson a modell, mikor ismétlődjön a hálózati kérés és mikor álljon le a folyamat.

**Elkészül:** dokumentált hibakezelési táblázat és véges, korlátozott agentfutás.

**Továbblépési feltétel:** nincs végtelen retry, és a hibát a program nem alakítja sikeresnek látszó válasszá. Jogosultsági elutasításra nem indul modelljavítási ciklus.

A `UsageLimits` a modellkérések és toolhívások számát is korlátozhatja. A költségbecslésre épülő limitet egészítsd ki szolgáltatói és alkalmazásszintű kerettel; a dokumentáció szerint a költséglimit nem kemény számlázási garancia. [Usage Limits](https://pydantic.dev/docs/ai/core-concepts/agent/#usage-limits).

## 4 hét Előzmények és tudásbázis

**Megértési cél:** tudd, mi marad meg két futás között, és milyen bizonyíték támasztja alá a választ.

Tanuld meg a `message_history`, `all_messages`, `new_messages` és az üzenetek mentésének kapcsolatát. A beszélgetéshez tartozó adatot az alkalmazásod tárolja és jogosultsághoz köti. A Pydantic AI üzenettípusai és adaptere segítenek az előzmény szerializálásában. [Messages and chat history](https://pydantic.dev/docs/ai/core-concepts/message-history/).

**Gyakorlat:**

1. Folytass kétlépéses beszélgetést: „Hol a rendelésem?” → „A 123-asra gondolok.”
2. Mentsd és töltsd vissza az előzményt; ellenőrizd, hogy másik ügyfél nem fér hozzá.
3. Írj öt rövid, azonosítóval ellátott tudásbázis-bejegyzést, például a szállítás és a számlázás szabályairól.
4. Készíts `search_knowledge_base` toolt egyszerű kereséssel. A válasz kimenetében szerepeljenek a felhasznált bejegyzések azonosítói.
5. Próbálj olyan kérdést, amelyre nincs forrás. A rendszer kérdezzen vissza vagy továbbítsa az ügyet, ahelyett hogy kitalálna egy szabályt.
6. Mérd meg, hogyan nő az előzmény hossza és a tokenhasználat. Válassz kezdeti kontextuskorlátot, és őrizd meg a toolhívásokhoz tartozó eredmények összetartozását.

**Elkészül:** többfordulós asszisztens menthető előzménnyel és visszakereshető forrásokkal.

**Továbblépési feltétel:** el tudod különíteni a beszélgetési előzményt, a hiteles adatforrást és a modell saját következtetését. Egy forrásazonosító puszta létezésén túl azt is ellenőrzöd, hogy a forrás alátámasztja-e az állítást.

Embeddinget és vektoradatbázist akkor adj hozzá, ha az egyszerű keresés korlátait konkrét példákkal már meg tudod mutatni.

## 5 hét Determinisztikus tesztelés

**Megértési cél:** a program helyességét internet és valódi modell nélkül is ellenőrizni tudd.

Használj `pytest`-et, `TestModel`-t, `FunctionModel`-t és `agent.override`-ot. A tesztekben állítsd a `pydantic_ai.models.ALLOW_MODEL_REQUESTS` értékét hamisra. A `TestModel` séma alapján generál tesztadatot; a valódi modell megértését és toolválasztását nem méri. A `FunctionModel` segítségével meghatározott válaszokat és toolhívásokat tudsz lejátszani. [Unit testing](https://pydantic.dev/docs/ai/guides/testing/).

**Gyakorlat:**

1. Teszteld közvetlenül a repository jogosultságait és az üzleti szabályokat.
2. Írj tesztet sikeres toolhívásra, hibás argumentumra, nem található rendelésre és tiltott hozzáférésre.
3. Játssz le egy hibás végső választ, majd javítást; külön teszteld a retry keret kimerülését.
4. Ellenőrizd az időtúllépés, a megszakítás és a használati limit kezelését.
5. Kapcsold be a lintet és a statikus típusellenőrzést. A CI futtassa ezeket és az offline teszteket.

**Elkészül:** gyors tesztcsomag, amely a működési és hibautakat ellenőrzi.

**Továbblépési feltétel:** a tesztek API-kulcs nélkül futnak, és egy hozzáférési vagy retry-kezelési hiba bevezetése ténylegesen megbuktatja a megfelelő tesztet. Nem egy változékony szabad szöveg teljes egyezése az egyetlen ellenőrzés.

## 6 hét Evals és modellválasztás

**Megértési cél:** adatok alapján meg tudd állapítani, javított-e egy prompt-, modell- vagy toolváltoztatás.

A Pydantic Evals `Case`, `Dataset` és evaluator fogalmaival feladateseteket és értékelési szabályokat állíthatsz össze. Kezdd programmal ellenőrizhető feltételekkel, majd a szöveg tartalmi minőségéhez adj emberi értékelést vagy kalibrált LLM-bírálót. [Pydantic Evals](https://pydantic.dev/docs/ai/evals/evals/).

**Gyakorlat:**

1. Készíts 60 esetet: 12 hétköznapi kérés, 12 hiányos vagy többértelmű kérés, 12 hiányzó adatú eset, 12 jogosulatlan adatkérés és 12 prompt injection kísérlet.
2. Minden csoportból nyolc eset kerüljön a fejlesztési, négy egy elkülönített ellenőrző adathalmazba. Így 40 eseten fejlesztesz, 20 eseten ellenőrzöd az eredményt.
3. Mérd a helyes kategóriát, a megfelelő visszakérdezést, a források helyességét, a jogosulatlan műveleteket, a késleltetést, a tokenhasználatot és a becsült költséget.
4. Hasonlíts össze két promptváltozatot. Utána próbálj másik modellt, ugyanazokon az eseteken. Egyszerre egy tényezőt módosíts.
5. Ismételd meg a bizonytalan eseteket, és nézz át kézzel minden kritikus hibát. Az LLM-bíráló döntéseit vesd össze saját értékeléseddel.

**Elkészül:** kiinduló mérési eredmény és rövid összehasonlítás minőség, késleltetés és költség szerint.

**Továbblépési feltétel:** egy változat elfogadását mérés indokolja. A kritikus hozzáférési és műveletvégrehajtási hibák blokkolják a kiadást. A 60 eset tanulási kiindulás; az éles forgalom jellegéhez további eseteket és elfogadási küszöböket kell meghatároznod.

Az offline tesztek minden kódváltozásnál fussanak. A valódi modellel végzett eval külön, költségkerettel rendelkező folyamat legyen. Az ellenőrző adathalmaz ismételt felhasználása után új, érintetlen esetekre is szükséged lesz.

## 7 hét Async API és megfigyelhetőség

**Megértési cél:** egy futás hibáját és költségét a felhasználói kéréstől az adatforrásig vissza tudd követni.

Építs FastAPI végpontot `await agent.run(...)` használatával. A hálózati kliensek élettartamát az alkalmazás indítása és leállítása kezelje. A kéréshez tartozó dependency példány hordozza a hitelesített ügyfél adatait. A Pydantic AI példái között találsz FastAPI chatalkalmazást. A tracing OpenTelemetryre épül, ezért Logfire vagy más OTel backend is használható. [Chat App with FastAPI](https://pydantic.dev/docs/ai/examples/conversational-agents/chat-app/), [Observability](https://pydantic.dev/docs/ai/integrations/logfire/).

**Gyakorlat:**

1. Készíts `POST /support` végpontot típusos be- és kimenettel. Az ügyfél azonosságát a hitelesítési réteg adja, ne a promptból olvasd ki.
2. Adj minden kéréshez azonosítót. Kösd össze a végpont, az agent, a toolok és a külső hívások trace-eit.
3. Rögzítsd a késleltetést, a modell- és toolhívások számát, a retry-kat és a hibakategóriákat. Érzékeny adatot és kulcsot ne naplózz.
4. Szimulálj párhuzamos kéréseket. Állíts be korlátot a futások számára, és kezeld a szolgáltatói kvóták elérését.
5. Mérj medián és p95 válaszidőt, vagyis a tipikus és a lassabb kérésekre jellemző időt. Különítsd el a modell és a saját I/O idejét.
6. Ha streaminget adsz hozzá, teszteld a kliens bontását és a futás megszakítását is. Üzleti műveletet csak végleges, ellenőrzött adat alapján indíts.

**Elkészül:** API, amelynél egy lassú vagy hibás kérés oka trace alapján megállapítható.

**Továbblépési feltétel:** az async végpont nem hív blokkoló `run_sync`-ot, a párhuzamos kérések ügyféladatai nem keverednek, és a megszakadt kérések erőforrásai felszabadulnak.

## 8 hét Biztonság és kiadás

**Megértési cél:** pontosan tudd, milyen műveletekre jogosult az agent, és hogyan működik a szolgáltatás hibás vagy támadó bemenet mellett.

Most adj hozzá egy rendelést módosító műveletet, például lemondási kérelmet. Használj külön jóváhagyási állapotot és szerveroldali jogosultságellenőrzést. A Pydantic AI deferred tool mechanizmusa segít a később jóváhagyott vagy külső folyamatban végrehajtott hívások kezelésében. A jóváhagyás konkrét művelethez, paraméterekhez és hitelesített személyhez tartozzon. [Deferred Tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/).

**Gyakorlat:**

1. Kezeld a felhasználói szöveget és a tudásbázisból visszakapott tartalmat nem megbízható bemenetként. Próbálj olyan szöveget, amely jogosultságokat vagy üzleti szabályokat akar felülírni.
2. Teszteld, hogy jóváhagyás nélkül nem történik módosítás, és a jóváhagyott paraméterek utólagos változtatása új ellenőrzést igényel.
3. Adj idempotenciakulcsot az író művelethez. A tárolási réteg akadályozza meg ugyanannak a műveletnek a megismétlését retry vagy párhuzamos kérés esetén.
4. Válassz kezdeti kérés-, token-, idő- és költségkereteket a 6–7. hét mérései alapján. Határozd meg, mi történik a keret elérésekor.
5. Készíts reprodukálható buildet és staging kiadást. Ellenőrizd az indítást, leállítást, konfigurációt és a readiness végpontot. A health check ne fogyasszon minden alkalommal LLM-hívást.
6. Dokumentáld a kiadást, visszaállítást és incidenskezelést. Próbálj ki szolgáltatói kiesést, adatforráshibát és költségriasztást.

**Elkészül:** staging környezetben működő szolgáltatás, mérési beszámoló és rövid üzemeltetési leírás.

**Továbblépési feltétel:** be tudod mutatni a sikeres kérés, a visszakérdezés, a megtagadott hozzáférés, a jóváhagyott módosítás és a szolgáltatói hiba teljes útját. Az ismételt író kérés nem okoz újabb üzleti módosítást, és egy kiadás visszaállítását is végrehajtottad.

## A gyakorlóprojekt tervezett szerkezete

Ezt a szerkezetet a funkciók elkészülésével fokozatosan alakítsd ki:

```text
src/support_assistant/
    schemas.py          # típusos bemenetek és kimenetek
    domain.py           # üzleti szabályok és hozzáférés
    dependencies.py     # a futásnak átadott szolgáltatások
    repositories.py     # adatforrások és tesztdubláik
    tools.py            # az agent által meghívható függvények
    agent.py            # agentkonfiguráció és utasítások
    service.py          # futtatás, limitek és hibák kezelése
    api.py              # HTTP és hitelesítési határ
    settings.py         # környezeti konfiguráció
tests/                  # offline tesztek
evals/                  # esetek, evaluátorok és mérési riportok
```

Az üzleti szabályokat az agent nélkül is lehessen meghívni és tesztelni. A prompt verziózott alkalmazásrész legyen. Az agentből érkező kimenet feldolgozásakor az alkalmazás ellenőrizze, hogy valóban végrehajtható-e a kért művelet.

## A production készség ellenőrzése

A nyolcadik hét végén minden ponthoz mutass be kódot, tesztet vagy mérési eredményt:

- [ ] El tudom magyarázni a modell–tool ciklust és egy futás üzeneteit.
- [ ] Típusos kimenetekkel és ellenőrizhető üzleti szabályokkal dolgozom.
- [ ] A jogosultságot szerveroldali kód ellenőrzi, több ügyfél adatainak elkülönítésével.
- [ ] A futások, retry-k, párhuzamosság és külső I/O korlátozottak.
- [ ] Az offline tesztek lefedik a fontos hiba- és hozzáférési eseteket.
- [ ] A modellviselkedést reprezentatív eseteken mérem, és ismerem a kritikus hibákat.
- [ ] Kérésenként visszakövethető a késleltetés, használat és hiba, érzékeny adatok kiszivárgása nélkül.
- [ ] Az író műveletek jóváhagyása és idempotenciája ellenőrzött.
- [ ] Reprodukálható a telepítés, és kipróbált a visszaállítás.
- [ ] Meg tudom indokolni, mely eseteket kezeli az agent, és melyeket továbbítja embernek.

## Haladó témák a nyolc hét után

**Capabilities és hooks:** tanuld meg közös utasítások, toolok és futási viselkedés újrafelhasználható összeállítását. Akkor bontsd ki külön modulba, amikor több agentben ismétlődik ugyanaz a viselkedés. A V2-ben a capabilities központi bővítési lehetőség. [Upgrade Guide](https://pydantic.dev/docs/ai/project/changelog/).

**Durable execution:** akkor vizsgáld meg a Temporal, DBOS vagy más támogatott motor használatát, ha a futásnak folyamatleálláson át is folytathatónak kell lennie. Gyakorlatként szakíts meg és indíts újra egy hosszabb feladatot. A beszélgetés tárolása és egy futás összeomlás utáni folytatása külön probléma. [Durable Execution](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/).

**Több agent és gráf:** egy mérhetően hasznos feladatfelosztásból indulj ki. Először hagyományos Python-vezérléssel készítsd el a folyamatot, majd mérd meg, mit ad hozzá egy újabb agent vagy explicit gráf.

**MCP és külső integrációk:** akkor bővíts, amikor már átlátod a tool jogosultságait, adathozzáférését, időkorlátját és tesztelését. Minden integrációhoz írj saját hibaforgatókönyveket.

## Az első tanulási alkalom

Az első 60–90 perc célja a kimeneti szerződés és egy egyszerű futás megértése.

1. Írd le, mit vársz ettől az üzenettől: „Tegnapra ígértétek a csomagomat, de még nem érkezett meg.”
2. Tervezd meg a `TicketAnalysis` adatmodellt. A rendelésazonosító legyen opcionális, hiszen az üzenet nem tartalmazza.
3. Adj öt kézi adatpéldát a sémának, köztük hibás kategóriát és hiányzó kötelező mezőt.
4. Olvasd el az Agents útmutató első példáit, majd írj egy saját, tool nélküli agentet ezzel a kimeneti típussal.
5. Futass három eltérő üzenetet, és vizsgáld meg a típusos kimenetet, valamint egy futás üzenettörténetét.
6. Fogalmazd meg saját szavaiddal: mit ellenőrzött a Pydantic, és mihez kellett a modell következtetése?

Az alkalom akkor teljes, ha ezt az utolsó különbséget egy helyes és egy téves válaszon is be tudod mutatni.
