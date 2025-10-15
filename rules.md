# Automatické vyplnění dotazníku (LimeSurvey) – Evidence podpořenosti u výzvy „Šablony pro MŠ a ZŠ I“

Tento návod popisuje, jak **automaticky** vyplnit webový dotazník v systému LimeSurvey: `https://evaluace.opjak.cz/index.php/262621`.

---

## 1) Vstupní konfigurace

Konfigurace je předávána jako JSON (ukázka níže). Agent ji načte před zahájením vyplňování.

```json
{
  "school_name": "Otice_ZS_MS_733",
  "code": "00XcmS",
  "MS": 83,
  "ZS": 70,
  "SD": 52,
  "dvpp_topics": {
    "vzdělávání_MŠ_1_I_4": [
      "cizí jazyky/komunikace v cizím jazyce",
      "inkluze",
      "formativní hodnocení",
      "řízení organizace, leadership a řízení pedagogického procesu"
    ],
    "vzdělávání_ZŠ_1_II_7": [
      "formativní hodnocení"
    ],
    "vzdělávání_ŠD_ŠK_1_V_1": [
      "inkluze"
    ]
  },
  "sdp_zzor": {
    "1.V/3 Inovativní vzdělávání účastníků zájmového vzdělávání v ŠD/ŠK": {
      "čtenářská pre/gramotnost": {
        "2022-2023": 9,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "umělecká gramotnost": {
        "2022-2023": 5,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      }
    },
    "1.II/9 Inovativní vzdělávání žáků v ZŠ": {
      "čtenářská pre/gramotnost": {
        "2022-2023": 9,
        "2023-2024": 19,
        "2024-2025": 15,
        "2025-2026": 0
      },
      "umělecká gramotnost": {
        "2022-2023": 9,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "vzdělávání s využitím nových technologií": {
        "2022-2023": 9,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "kulturní povědomí a vyjádření": {
        "2022-2023": 9,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      }
    },
    "1.I/6 Inovativní vzdělávání dětí v MŠ": {
      "čtenářská pre/gramotnost": {
        "2022-2023": 25,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "matematická pre/gramotnost": {
        "2022-2023": 25,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "inkluze včetně primární prevence": {
        "2022-2023": 22,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "přírodovědné a technické vzdělávání": {
        "2022-2023": 19,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "evvo a vzdělávání pro udržitelný rozvoj": {
        "2022-2023": 25,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "vzdělávání s využitím nových technologií": {
        "2022-2023": 17,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "kulturní povědomí a vyjádření": {
        "2022-2023": 24,
        "2023-2024": 0,
        "2024-2025": 0,
        "2025-2026": 0
      }
    }
  }
}
```

---

## 2) Globální pravidla vyplňování

* **Vždy pokračuj tlačítkem „Další“** po dokončení stránky.
* Úvodní titulek stránky je:

  ```html
  <h1 class="survey-name text-center">
    Evidence podpořenosti u výzvy "Šablony pro MŠ a ZŠ I" (číslo výzvy 02_22_002)
  </h1>
  ```
* Sekce pro typ školy jsou odděleny nadpisy:

  ```html
  <div class="group-title text-center h3 space-col">MŠ</div>
  <div class="group-title text-center h3 space-col">ZŠ</div>
  <div class="group-title text-center h3 space-col">ŠD</div>
  ```
* **Školní roky** používané v dotazníku: `2022/2023`, `2023/2024`, `2024/2025` (případně `2025/2026`, pokud je v položkách JSON uveden).
* Pokud není v JSON uvedeno jinak, **počty** vyplňuj jako **podíl 0.30–0.50** z počtu dětí pro daný typ školy. **Pro každé pole použij náhodný multiplikátor** z tohoto rozsahu (např. 0.33, 0.35, 0.38, 0.42, 0.45), aby nebyla všechna čísla stejná. Na konci **zaokrouhli na celé číslo** (nejbližší celé číslo).

  * Příklad: `MS = 83`
    - První pole: `round(0.35 * 83) = 29`
    - Druhé pole: `round(0.42 * 83) = 35`
    - Třetí pole: `round(0.38 * 83) = 32`

---

## 3) Přihlášení

1. Otevři URL dotazníku.
2. Přihlas se pomocí hodnoty `code` z JSON.
3. Potvrď a pokračuj na první stránku dotazníku.

---

## 4) Rozpoznání a rozsah vyplňování podle typu školy

Na základě přítomnosti hodnot v JSON vyplňuj jen odpovídající sekce:

* **MŠ** – pokud JSON obsahuje klíč `MS` (>0), vyplňuj část označenou nadpisem `MŠ`.
* **ZŠ** – pokud JSON obsahuje klíč `ZS` (>0), vyplňuj část `ZŠ`.
* **ŠD/ŠK** – pokud JSON obsahuje klíč `SD` (>0), vyplňuj část `ŠD` (případně `ŠK`, je‑li přítomna).

> Pozn.: V LimeSurvey je každá část vizuálně oddělena, hledej element s třídou `group-title` obsahující název příslušné sekce.

---

## 5) Vzdělávání pracovníků ve vzdělávání (DVPP)

* Tato část je **vždy** řízena JSON klíčem `dvpp_topics`.
* Pro každou klíčovou větev `vzdělávání_MŠ_1_I_4`, `vzdělávání_ZŠ_1_II_7`, `vzdělávání_ŠD_ŠK_1_V_1`:

  1. Najdi sekci odpovídající typu školy (MŠ/ZŠ/ŠD) a aktivitě.
  2. Zaškrtni příslušná témata **v přesném znění** ze seznamu.
  3. Pokud téma v dotazníku neexistuje, **ponech prázdné** (nepřidávej vlastní texty).
* Po dokončení stránky klikni **„Další“**.

---

## 6) Inovativní vzdělávání (sdp_zzor)

* Řízeno JSON klíčem `sdp_zzor`.
* Pro každý **název aktivity** (např. `1.I/6 Inovativní vzdělávání dětí v MŠ`, `1.II/9 ...`, `1.V/3 ...`):

  1. Najdi odpovídající podsekci pro daný typ školy.
  2. V rámci aktivity iteruj všechny **oblasti** (např. „čtenářská pre/gramotnost“, „umělecká gramotnost“, …).
  3. Zaškrtni příslušnou oblast inovativního vzdělávání - checkbox a label je v <li>..</li> bloku, text labelu odpovídá oblasti v JSON, pokud nenalezneš přesný text v labelu, zkontoruj jen 1. slovo oblasti vs. 1. slovo labelu např.:
  "evvo a vzdělávání pro udržitelný rozvoj" vs "EVVO (environmentální vzdělávání, výchova a osvěta) a vzdělávání pro udržitelný rozvoj" -> 1. slova jsou stejná - Zaškrtni příslušný checkbox 
  
  4. Pro **každý školní rok** z klíčů (typicky `2022-2023`, `2023-2024`, `2024-2025`, `2025-2026`) vyplň přesný počet z JSON.
  5. Není-li hodnota v JSON, **vyplň 0**.
* Po dokončení stránky klikni **„Další“**.

---

## 7) Počty dětí/žáků podle typu školy (obecné pole počtu)

Pokud dotazník vyžaduje obecné počty pro MŠ/ZŠ/ŠD za **každý školní rok** a nejsou v JSON explicitně uvedeny:

1. Urči **základní počet** z JSON (`MS`, `ZS`, `SD`).
2. Spočti hodnotu jako `round(0.35 * základní_počet)` (pokud není jinak instruováno – viz kapitola 2).
3. Zapiš stejné pravidlo pro roky `2022/2023`, `2023/2024`, `2024/2025` (příp. `2025/2026`).
4. Po dokončení stránky klikni **„Další“**.

---

## 8) Specifické otázky a jejich pevná pravidla

1. **OMJ – Uveďte prosím, dle Vašeho nejlepšího odhadu, jaký počet dětí s OMJ ovlivnil projekt za celou dobu realizace, jejichž národnost je:**

   * **Nevyplňuj žádná čísla** – pokračuj pouze **tlačítkem „Další“**.

2. **Vedoucí pracovníci ve vzdělávání** – *„Uveďte prosím, kolik vedoucích pracovníků ve vzdělávání (vyjma ostatních pracovníků ve vzdělávání) se za celou dobu realizace účastnilo aktivity:“*

   * **Vždy vyplň 0** pro všechny položky.

3. **Pracovníci ve vzdělávání s ukrajinskou národností** – *„Uveďte prosím, kolik pracovníků ve vzdělávání s ukrajinskou národností bylo v jednotlivých letech realizace financováno prostřednictvím šablony:“*

   * **Všude vyplň 0** pro všechny školní roky.

Po každé této stránce klikni **„Další“**.

---

## 9) Ukončení dotazníku

Dotazník končí stránkou s textem:

```
Děkujeme Vám!

Vaše odpovědi byly uloženy.

Vytisknout své odpovědi.
```

Po zobrazení této stránky je proces **hotový**.

---

## 10) Technické tipy (doporučený postup pro agenta)

### A) Použití Chrome DevTools MCP

* **Základní workflow**:
  1. Použij `take_snapshot` pro získání struktury stránky s UID prvků
  2. Použij `fill`, `fill_form` nebo `click` s UID z snapshotu
  3. Po každé akci vezmi nový snapshot pro nové UID (staré UID přestanou fungovat)

* **Vyplňování checkboxů pomocí JavaScriptu** (DOPORUČENO):
  ```javascript
  // 1. Najdi checkboxy pomocí document.querySelectorAll('input[type="checkbox"]')
  // 2. Najdi label pomocí document.querySelector(`label[for="${checkbox.id}"]`)
  // 3. VŽDY NEJDŘÍV odškrtni VŠECHNY checkboxy
  // 4. Pak zaškrtni pouze požadované
  // 5. Používej normalizaci textu (bez diakritiky, lowercase) pro porovnání
  ```

* **JavaScript normalizační funkce**:
  ```javascript
  function normalize(text) {
    return text.toLowerCase().trim()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ");
  }
  ```

### B) Struktura HTML formuláře

* **Checkboxy**:
  - Label je sourozenec (sibling) checkboxu, ne rodič
  - Používej `document.querySelector(\`label[for="${checkbox.id}"]\`)` pro hledání labelu

* **Textová pole v tabulkách**:
  - Téma je v `<th>` buňce řádku (`row.querySelector('th')`)
  - Rok je v předchozím elementu textboxu (`box.previousElementSibling`)

### C) Vyhledávání prvků

* **Titul dotazníku**: `h1.survey-name`
* **Nadpisy skupin** (sekce škol): `div.group-title`
* **Tlačítko pokračování**: tlačítko s viditelným textem **„Další"** (může být `button[type=submit]` nebo `input[value="Další"]`)

### D) Robustnost

* Po každém odeslání stránky ověř, že došlo k **přechodu na novou stránku** (změna adresy, přítomnost nové skupiny otázek nebo potvrzovacího textu)
* Pokud se objeví validační chyba, zkontroluj, zda některé povinné pole není prázdné – doplň podle pravidel výše
* Použij `wait_for` pro čekání na konkrétní text po přechodu na novou stránku

### E) Zaokrouhlování

* Použij `round()` (nejbližší celé číslo). Pokud systém vyžaduje celé číslo bez zaokrouhlování, použij `floor()`
* Pro MŠ (MS=83): `round(0.35 * 83) = 29`
* Pro ZŠ (ZS=70): `round(0.35 * 70) = 25`
* Pro ŠD (SD=52): `round(0.35 * 52) = 18`

### F) Konzistence roků

* Dodržuj přesné formáty **„2022-2023"** v JSON vs. **„2022/2023"** v UI – mapuj je 1:1 dle roku

---

## 11) Pseudokód workflow

```
load JSON cfg
open survey URL (via new_page)
take_snapshot
login with cfg.code (via fill + click)
click "Další"

// === MŠ SEKCE ===
if cfg.MS > 0:

  // Stránka: Školní asistent MŠ - počty dětí
  take_snapshot
  fill_form: školní roky 2022/2023, 2023/2024, 2024/2025 = round(0.35 * MS)
  click "Další"

  // Stránka: DVPP témata MŠ (checkboxy)
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni pouze témata z dvpp_topics["vzdělávání_MŠ_1_I_4"]
    - používej normalizaci textu
  click "Další"

  // Stránka: DVPP počty dětí podle tématu
  take_snapshot
  fill_form: pro každé zaškrtnuté téma = round(0.35 * MS) pro roky
  click "Další"

  // Stránka: SDP/ŽZOR témata MŠ (checkboxy)
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni témata z sdp_zzor["1.I/6 Inovativní vzdělávání dětí v MŠ"]
  click "Další"

  // Stránka: SDP/ŽZOR počty podle tématu a roku
  take_snapshot
  evaluate_script:
    - vyplň hodnoty z JSON podle tématu a roku (2022-2023 → 2022/2023)
  click "Další"

  // Stránka: Odborně zaměřená tematická setkávání
  take_snapshot
  fill_form: roky = round(0.35 * MS)
  click "Další"

  // Stránka: OMJ národnosti MŠ
  take_snapshot
  click "Další" (BEZ vyplňování!)

  // Stránka: Vedoucí pracovníci MŠ
  take_snapshot
  fill = 0
  click "Další"

  // Stránka: Ukrajinští pracovníci MŠ
  take_snapshot
  fill all = 0
  click "Další"

// === ZŠ SEKCE ===
if cfg.ZS > 0:

  // Stránka: DVPP témata ZŠ
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni témata z dvpp_topics["vzdělávání_ZŠ_1_II_7"]
  click "Další"

  // Stránka: DVPP počty žáků
  take_snapshot
  fill_form: round(0.35 * ZS) pro roky
  click "Další"

  // Stránka: SDP/ŽZOR témata ZŠ
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni témata z sdp_zzor["1.II/9 Inovativní vzdělávání žáků v ZŠ"]
  click "Další"

  // Stránka: SDP/ŽZOR počty
  take_snapshot
  evaluate_script:
    - vyplň hodnoty z JSON
  click "Další"

  // Stránka: OMJ ZŠ
  take_snapshot
  click "Další" (BEZ vyplňování!)

  // Stránka: Vedoucí pracovníci ZŠ
  take_snapshot
  fill = 0
  click "Další"

// === ŠD SEKCE ===
if cfg.SD > 0:

  // Stránka: DVPP témata ŠD
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni témata z dvpp_topics["vzdělávání_ŠD_ŠK_1_V_1"]
  click "Další"

  // Stránka: DVPP počty účastníků
  take_snapshot
  fill_form: round(0.35 * SD) pro roky
  click "Další"

  // Stránka: SDP/ŽZOR témata ŠD
  take_snapshot
  evaluate_script:
    - odškrtni VŠE
    - zaškrtni témata z sdp_zzor["1.V/3 Inovativní vzdělávání účastníků..."]
  click "Další"

  // Stránka: SDP/ŽZOR počty
  take_snapshot
  evaluate_script:
    - vyplň hodnoty z JSON
  click "Další"

  // Stránka: OMJ ŠD
  take_snapshot
  click "Další" (BEZ vyplňování!)

  // Stránka: Vedoucí pracovníci ŠD
  take_snapshot
  fill = 0
  click "Další"

// Konec
take_snapshot
wait for text "Děkujeme Vám! Vaše odpovědi byly uloženy."
process done ✅
```

---

## 12) Kontrolní seznam před odesláním

* [ ] Přihlášení proběhlo pomocí `code` z JSON.
* [ ] Vyplněny pouze relevantní sekce (MŠ/ZŠ/ŠD) dle JSON.
* [ ] DVPP témata označena přesně podle `dvpp_topics` (pokud existují v UI).
* [ ] Inovativní vzdělávání vyplněno podle `sdp_zzor` včetně všech roků.
* [ ] Obecné roční počty dopočteny `round(0.35 * count)` tam, kde nejsou explicitně v JSON.
* [ ] Stránka s OMJ přeskočena tlačítkem **„Další“** bez vyplňování.
* [ ] Vedoucí pracovníci = **0** (vše).
* [ ] Ukrajinští pracovníci = **0** (všechny roky).
* [ ] Zobrazen finální text **„Děkujeme Vám! Vaše odpovědi byly uloženy.“**

---

### Poznámky

* Pokud se názvy položek v UI mírně liší (diakritika/mezery), porovnávej **bez ohledu na diakritiku** a **case-insensitive**.
* Nejsou-li některé sekce v konkrétním dotazníku přítomny, agent je prostě přeskočí tlačítkem **„Další"**.

---

## 13) Praktické zkušenosti z testování

### Pořadí stránek (skutečné flow):

1. **Login** stránka → vyplnit kód
2. **Úvodní stránka** s instrukcemi → kliknout Další
3. **Pro každý typ školy (MŠ/ZŠ/ŠD) v tomto pořadí:**
   - Stránka s počty pro školní asistenty/základní aktivity
   - DVPP témata (checkboxy)
   - DVPP počty dětí/žáků podle vybraných témat
   - SDP/ŽZOR témata (checkboxy)
   - SDP/ŽZOR počty podle témat a roků
   - Případně další specifické aktivity (např. tematická setkávání)
   - OMJ národnosti (PŘESKOČIT)
   - Vedoucí pracovníci (vyplnit 0)
   - (pouze MŠ) Ukrajinští pracovníci (vyplnit 0)
4. **Závěrečná stránka** s poděkováním

### Klíčové poznatky:

* **JavaScript je preferovaný způsob** pro práci s checkboxy - rychlejší a spolehlivější než klikání na jednotlivé UID
* **Vždy odškrtni VŠECHNY checkboxy** před zaškrtáváním požadovaných - formulář má často předvyplněné hodnoty
* **UID z snapshotu jsou valid pouze do další akce** - vždy vezmi nový snapshot po každém `click` nebo `fill`
* **Normalizace textu je kritická** - české texty s diakritikou vyžadují NFD normalizaci a odstranění diakritiky
* **EVVO téma** v JSON je jako "evvo a vzdělávání pro udržitelný rozvoj", ale v UI je "EVVO (environmentální vzdělávání...)" - normalizace řeší
* **Rok formát**: JSON má `2022-2023` (s pomlčkou), UI má `2022/2023` (s lomítkem) - při vyplňování převádět
* **Label struktura**: Label je SIBLING checkboxu (ne parent) - najdi přes `document.querySelector(\`label[for="${checkbox.id}"]\`)`
* **Tabulková pole**: Téma je v `<th>`, rok je v `previousElementSibling` textboxu
* **Console logging** v JavaScriptu je velmi užitečný pro debugging - používej emoji pro přehlednost (🔄 ✅ ❌ 🎯)
