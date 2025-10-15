# Chrome DevTools MCP - Exploration Workflow

## 🎯 Cíl exploration

Projít formulář manuálně pomocí Chrome DevTools MCP v **headed mode** (viditelný browser) a zdokumentovat:

1. Přesné pořadí stránek
2. `ls-question-text-*` ID pro každou otázku
3. Strukturu formulářových prvků (checkboxy, textboxy, tabulky)
4. Mapování JSON dat → UI elementy
5. Speciální případy a edge cases

---

## 📦 Testovací data

**Soubor:** `data/Bruntal_Pionyrska_MS_360_consolidated.json`

```json
{
  "school_name": "Bruntal_Pionyrska_MS_360",
  "code": "00X2ic",
  "MS": 97,
  "ZS": 0,
  "SD": 0,
  "dvpp_topics": {
    "vzdělávání_MŠ_1_I_4": [
      "pedagogická diagnostika",
      "inkluze",
      "zážitková pedagogika",
      "formativní hodnocení",
      "umělecká gramotnost"
    ]
  },
  "sdp_zzor": {
    "1.I/6 Inovativní vzdělávání dětí v MŠ": {
      "čtenářská pre/gramotnost": {"2022-2023": 0, "2023-2024": 19, ...},
      "matematická pre/gramotnost": {"2022-2023": 0, "2023-2024": 15, ...},
      "umělecká gramotnost": {"2022-2023": 0, "2023-2024": 15, ...},
      "přírodovědné a technické vzdělávání": {"2022-2023": 0, "2023-2024": 19, ...},
      "vzdělávání s využitím nových technologií": {"2022-2023": 0, "2023-2024": 18, ...},
      "kulturní povědomí a vyjádření": {"2022-2023": 0, "2023-2024": 19, ...},
      "rozvoj podnikavosti a kreativity": {"2022-2023": 0, "2023-2024": 20, ...}
    }
  }
}
```

**Poznámka:** Pouze MŠ sekce (ZS=0, SD=0), takže očekáváme pouze stránky pro mateřskou školu.

---

## 🔧 Chrome DevTools MCP nástroje

### Dostupné tools (teorie z chrome-devtools-usage.md):

1. **`new_page(url)`** - Otevře novou stránku
2. **`take_snapshot()`** - Vezme snapshot DOM s UID pro elementy
3. **`click(uid)`** - Klikne na element podle UID
4. **`fill(uid, value)`** - Vyplní textové pole
5. **`fill_form(elements[])`** - Hromadné vyplnění polí
6. **`evaluate_script(function)`** - JavaScript injection (DOPORUČENO pro checkboxy)
7. **`screenshot()`** - Screenshot stránky

### Workflow pattern:

```
1. take_snapshot() → získat UIDs
2. fill/click pomocí UIDs
3. DŮLEŽITÉ: Po každém click/fill vzít NOVÝ snapshot (staré UIDs se stanou stale)
4. Nebo použít evaluate_script() pro hromadné operace (lepší!)
```

---

## 📋 Exploration checklist

### ✅ Stránka 1: Login
- [ ] Screenshot
- [ ] Identifikovat input pole pro kód
- [ ] Identifikovat tlačítko "Pokračovat"
- [ ] Vyplnit kód: `00X2ic`
- [ ] Kliknout Pokračovat

### ✅ Stránka 2: Úvodní stránka
- [ ] Screenshot
- [ ] Ověřit titulek: "Evidence podpořenosti..."
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 1: Školní asistent
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zkopírovat přesný text otázky
- [ ] Identifikovat textová pole pro školní roky:
  - 2022/2023
  - 2023/2024
  - 2024/2025
  - 2025/2026?
- [ ] Vyplnit hodnoty: `round(random(0.30, 0.50) * 97)`
  - Např: 34, 41, 38, 32
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 2: DVPP témata (checkboxy)
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zkontrolovat text obsahuje: "1.I/4" a "vzdělávání pracovníků"
- [ ] Zjistit strukturu checkboxů:
  - HTML selektor
  - Label selektor
  - Relationship checkbox ↔ label
- [ ] **Použít JavaScript injection** pro zaškrtnutí:
  ```javascript
  // Odškrtnout všechny
  // Zaškrtnout: pedagogická diagnostika, inkluze, zážitková pedagogika,
  //             formativní hodnocení, umělecká gramotnost
  ```
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 3: DVPP počty dětí
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zjistit strukturu tabulky:
  - Řádky = témata (z předchozí stránky)
  - Sloupce = školní roky
  - Input fields selektory
- [ ] Vyplnit hodnoty: `round(random(0.30, 0.50) * 97)` pro každé pole
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 4: SDP/ŽZOR témata (checkboxy)
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zkontrolovat text obsahuje: "1.I/6" a "inovativní vzdělávání"
- [ ] **Použít JavaScript injection** pro zaškrtnutí oblastí:
  - čtenářská pre/gramotnost
  - matematická pre/gramotnost
  - umělecká gramotnost
  - přírodovědné a technické vzdělávání
  - vzdělávání s využitím nových technologií
  - kulturní povědomí a vyjádření
  - rozvoj podnikavosti a kreativity
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 5: SDP/ŽZOR počty
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zjistit strukturu tabulky:
  - Řádky = oblasti (z předchozí stránky)
  - Sloupce = školní roky (2022/2023, 2023/2024, ...)
- [ ] Vyplnit **EXACT hodnoty z JSON**:
  - čtenářská pre/gramotnost: 2023/2024 = 19
  - matematická pre/gramotnost: 2023/2024 = 15
  - atd...
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 6: Tematická setkávání (?)
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Zjistit co vyplnit
- [ ] Vyplnit hodnoty
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 7: OMJ národnosti
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Ověřit text obsahuje: "OMJ" nebo "národnost"
- [ ] **NEVYPLŇOVAT NIČEHO**
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 8: Vedoucí pracovníci
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Ověřit text obsahuje: "vedoucí pracovníci"
- [ ] Vyplnit **všechny položky = 0**
- [ ] Kliknout "Další"

### ✅ MŠ Stránka 9: Ukrajinští pracovníci
- [ ] Screenshot
- [ ] Identifikovat `ls-question-text-*` ID
- [ ] Ověřit text obsahuje: "ukrajin"
- [ ] Vyplnit **všechny školní roky = 0**
- [ ] Kliknout "Další"

### ✅ Stránka konec: Poděkování
- [ ] Screenshot
- [ ] Ověřit text: "Děkujeme Vám! Vaše odpovědi byly uloženy."
- [ ] ✅ HOTOVO

---

## 📊 Output - Co dokumentovat

Pro každou stránku vytvořit v `docs/workflow_mapping.md`:

```markdown
## Stránka X: Název

**Question ID:** `ls-question-text-262621X...`

**Question text:**
```
Přesný text otázky...
```

**Page type:** `checkboxes` | `table_counts` | `simple_inputs`

**School type:** `MS` | `ZS` | `SD`

**JSON mapping:**
- JSON key: `vzdělávání_MŠ_1_I_4` nebo `1.I/6 Inovativní vzdělávání dětí v MŠ`
- Calculation: `random_multiplier` nebo `from_json` nebo `fixed_value`

**Element selectors:**
- Checkboxes: `input[type="checkbox"]`
- Labels: `label[for="..."]`
- Text inputs: `input[type="text"]`
- Table structure: ...

**Screenshot:** `screenshots/0X_page_name.png`

**Notes:**
- Special cases
- Edge cases
- Normalizace requirements
```

---

## 🚀 Začínáme

**Status:** Ready to start
**Next step:** Otevřít formulář pomocí Chrome DevTools MCP

```
# Spustit exploration
[User potvrdí → začít s new_page()]
```

---

*Tento dokument bude aktualizován během exploration.*
