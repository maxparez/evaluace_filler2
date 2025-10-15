# LimeSurvey Automatické Vyplňování - Evidence Podpořenosti

Automatizační nástroj pro vyplňování dotazníků LimeSurvey pro výzvu "Šablony pro MŠ a ZŠ I".

**Technologie:** Python 3 + Playwright
**Status:** ✅ **PRODUCTION READY**

---

## 🎯 Účel

Automaticky vyplňuje webový dotazník na `https://evaluace.opjak.cz/index.php/262621` na základě JSON konfigurace. Podporuje vyplňování pro tři typy škol:
- **MŠ** (Mateřská škola)
- **ZŠ** (Základní škola)
- **ŠD** (Školní družina)

---

## ✨ Funkce

- ✅ Automatické přihlášení pomocí přístupového kódu
- ✅ Detekce typu stránky z question textu
- ✅ Vyplnění všech sekcí pro MŠ/ZŠ/ŠD:
  - Školní asistent (náhodné hodnoty 0.30-0.50 × base count)
  - DVPP témata (checkboxes z JSON)
  - DVPP počty (náhodné hodnoty pro zaškrtnutá témata)
  - SDP/ŽZOR témata (checkboxes z JSON)
  - SDP/ŽZOR počty (**přesné hodnoty z JSON**)
  - Tematická setkávání (náhodné hodnoty)
  - OMJ národnosti (přeskočit)
  - Vedoucí pracovníci (vyplnit 0)
  - Ukrajinští pracovníci (vyplnit 0)
- ✅ Normalizace českých diakritických znamének pro matching
- ✅ JavaScript injection pro robustní vyplňování (řeší skryté fieldy)
- ✅ Event dispatching pro správnou validaci
- ✅ Kompletní logování s emoji
- ✅ Detekce úspěšného dokončení
- ✅ Headless i headed režim

---

## 📋 Požadavky

- **Python** 3.8 nebo novější
- **pip** (Python package manager)
- **Internet connection** (pro přístup k formuláři)

---

## 🚀 Instalace

```bash
# 1. Přejděte do adresáře projektu
cd ai_evaluace_filler2

# 2. Vytvořte virtual environment
python -m venv venv

# 3. Aktivujte virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 4. Nainstalujte závislosti
pip install -r requirements.txt

# 5. Nainstalujte Chromium browser pro Playwright
playwright install chromium
```

---

## 📁 Struktura JSON Konfigurace

Vytvořte JSON soubor s následující strukturou:

```json
{
  "school_name": "Nazev_Skoly_123",
  "code": "ABC123",
  "MS": 97,
  "ZS": 0,
  "SD": 0,
  "dvpp_topics": {
    "vzdělávání_MŠ_1_I_4": [
      "pedagogická diagnostika",
      "inkluze",
      "formativní hodnocení"
    ]
  },
  "sdp_zzor": {
    "1.I/6 Inovativní vzdělávání dětí v MŠ": {
      "čtenářská pre/gramotnost": {
        "2022-2023": 0,
        "2023-2024": 19,
        "2024-2025": 0,
        "2025-2026": 0
      },
      "matematická pre/gramotnost": {
        "2022-2023": 0,
        "2023-2024": 15,
        "2024-2025": 0,
        "2025-2026": 0
      }
    }
  }
}
```

### Vysvětlení polí:

| Pole | Typ | Povinné | Popis |
|------|-----|---------|-------|
| `school_name` | string | Ne | Identifikátor školy (pro logging) |
| `code` | string | **Ano** | Přístupový kód k dotazníku |
| `MS` | integer | Ne* | Počet dětí v MŠ |
| `ZS` | integer | Ne* | Počet žáků v ZŠ |
| `SD` | integer | Ne* | Počet účastníků v ŠD |
| `dvpp_topics` | object | Ne | Témata pro vzdělávání pracovníků |
| `sdp_zzor` | object | Ne | Oblasti a počty pro inovativní vzdělávání |

\* **Poznámka:** Alespoň jeden z MS/ZS/SD musí být > 0

### Klíče pro dvpp_topics:

- `"vzdělávání_MŠ_1_I_4"` - pro MŠ sekci
- `"vzdělávání_ZŠ_1_I_5"` - pro ZŠ sekci (očekáváno)
- `"vzdělávání_ŠD_1_I_X"` - pro ŠD sekci (očekáváno)

### Klíče pro sdp_zzor:

- `"1.I/6 Inovativní vzdělávání dětí v MŠ"` - pro MŠ sekci
- `"1.I/7 Inovativní vzdělávání žáků v ZŠ"` - pro ZŠ sekci (očekáváno)
- `"1.I/9 Inovativní vzdělávání v ŠD"` - pro ŠD sekci (očekáváno)

### Formát školních roků:

V JSON **vždy použijte formát s pomlčkou**: `"2022-2023"`
Systém automaticky konvertuje na UI formát: `"2022/2023"`

---

## 🎮 Použití

### Základní příkazy

```bash
# Aktivovat virtual environment
source venv/bin/activate

# Základní spuštění (headless mode)
python main.py data/config.json

# Debug mode (viditelný browser)
python main.py data/config.json --headed

# Přepsat přístupový kód z JSON
python main.py data/config.json --code XYZ789

# Verbose logging (detailní výpis)
python main.py data/config.json --verbose

# Kombinace všech parametrů
python main.py data/config.json --headed --code ABC123 --verbose
```

### Příklady s testovacími daty

```bash
# MŠ pouze
python main.py data/Bruntal_Pionyrska_MS_360_consolidated.json --headed

# ZŠ pouze
python main.py data/Kravare_Kouty_ZS_4620_consolidated.json --headed

# MŠ + ZŠ kombinace
python main.py data/Ostrava_Radvanice_Vrchlickeho_ZS_6660_consolidated.json --headed
```

### Nápověda

```bash
python main.py --help
```

---

## 🔄 Workflow

### Co se stane při spuštění:

1. **Validace** - Kontrola JSON konfigurace
2. **Login** - Přihlášení pomocí přístupového kódu
3. **Intro stránka** - Přeskočení úvodní stránky
4. **Pro každý typ školy (MŠ/ZŠ/ŠD):**
   - **Školní asistent** - Vyplnění 4 polí (školní roky) náhodnými hodnotami
   - **DVPP témata** - Zaškrtnutí checkboxů z JSON
   - **DVPP počty** - Vyplnění tabulky náhodnými hodnotami
   - **SDP/ŽZOR témata** - Zaškrtnutí checkboxů z JSON
   - **SDP/ŽZOR počty** - Vyplnění tabulky **přesnými hodnotami z JSON**
   - **Tematická setkávání** - Vyplnění náhodnými hodnotami
   - **OMJ národnosti** - Přeskočení (bez vyplňování)
   - **Vedoucí pracovníci** - Vyplnění 0
   - **Ukrajinští pracovníci** - Vyplnění 0
5. **Verifikace** - Kontrola zprávy "Děkujeme Vám! Vaše odpovědi byly uloženy."
6. **Dokončení** - Zavření prohlížeče

---

## 📊 Logování

### Formát logů

Skript vytváří dva výstupy:
1. **Console** - Kompaktní výpis s emoji
2. **Log file** - Detailní log v `logs/form_filler_YYYYMMDD_HHMMSS.log`

### Příklad console výstupu

```
20:40:06 | 📁 Log file: logs/form_filler_20251014_204006.log
20:40:06 |
20:40:06 | ============================================================
20:40:06 |   LimeSurvey Form Filler Started
20:40:06 | ============================================================
20:40:06 | School: Bruntal_Pionyrska_MS_360
20:40:06 | Code: 00X2ic
20:40:06 | School types: MS
20:40:06 |
20:40:06 | 📄 Page 1: Introduction page
20:40:10 | 📄 Page 2: MŠ - Školní asistent
20:40:10 |   ✏️  Školní rok 2022/2023: 34
20:40:10 |   ✏️  Školní rok 2023/2024: 41
20:40:14 | 📄 Page 3: MŠ - DVPP témata (checkboxes)
20:40:14 | Checking 5 checkboxes
20:40:14 |   ✓ pedagogická diagnostika
20:40:14 |   ✓ inkluze
20:40:18 | 📄 Page 4: MŠ - DVPP počty
20:40:18 | Filling 20 fields (5 topics × 4 years)
20:40:18 |   📊 pedagogická diagnostika | 2022/2023: 34
20:40:22 | ✅ Form completed successfully!
```

### Emoji legenda

| Emoji | Význam |
|-------|--------|
| 📁 | Log file path |
| 📄 | Nová stránka |
| ✏️ | Vyplnění textového pole |
| ✓ | Zaškrtnutý checkbox |
| 📊 | Vyplnění tabulky |
| ⏭️ | Přeskočená stránka |
| ⚠️ | Varování |
| ❌ | Chyba |
| ✅ | Úspěch |

---

## ⚙️ Výpočty a Business Logika

### Náhodné multiplikátory

**Použití:** Školní asistent, DVPP počty, Tematická setkávání

Pro každé pole se vygeneruje náhodný multiplikátor **0.30 - 0.50**:

```python
count = round(random.uniform(0.30, 0.50) × base_count)
```

**Příklad pro MS=97:**
```
Školní rok 2022/2023: round(0.36 × 97) = 35
Školní rok 2023/2024: round(0.43 × 97) = 42
Školní rok 2024/2025: round(0.31 × 97) = 30
Školní rok 2025/2026: round(0.48 × 97) = 47
```

### Přesné hodnoty z JSON

**Použití:** SDP/ŽZOR počty

Hodnoty se berou **přesně** z JSON bez jakékoli modifikace:

```json
"čtenářská pre/gramotnost": {
  "2022-2023": 0,    → vyplní 0
  "2023-2024": 19,   → vyplní 19
  "2024-2025": 0,    → vyplní 0
  "2025-2026": 0     → vyplní 0
}
```

### Speciální pravidla

| Stránka | Pravidlo |
|---------|----------|
| OMJ národnosti | **Přeskočit** - žádné vyplňování |
| Vedoucí pracovníci | **Vyplnit 0** do všech polí |
| Ukrajinští pracovníci | **Vyplnit 0** do všech polí |

---

## 🛠️ Technické detaily

### Architektura

```
src/
├── config_loader.py       # Načítání a validace JSON
├── text_normalizer.py     # Normalizace českého textu
├── calculator.py          # Náhodné multiplikátory
├── logger_config.py       # Logging setup
├── question_detector.py   # Detekce typu stránky
└── form_filler.py         # Hlavní automatizace
```

### Klíčové funkce

#### Text normalizace
```python
"Umělecká gramotnost" → "umelecka gramotnost"
```
- Odstranění diakritiky
- Lowercase
- Collapse whitespace

#### JavaScript injection
```javascript
// Řeší problém se skrytými fieldy
inputs[i].value = 'value';
inputs[i].dispatchEvent(new Event('input', {bubbles: true}));
inputs[i].dispatchEvent(new Event('change', {bubbles: true}));
```

#### Detekce stránky
- Hledá `ls-question-text-*` element
- Parsuje activity code (1.I/4, 1.I/6, atd.)
- Detekuje klíčová slova v textu

---

## 🧪 Testování

### Testovací data

V adresáři `data/` jsou připravena testovací data:

| Soubor | Škola | MS | ZS | SD | Popis |
|--------|-------|----|----|----|----|
| `Bruntal_Pionyrska_MS_360_consolidated.json` | Bruntál Pionýrská | 97 | 0 | 0 | ✅ Otestováno |
| `Krnov_Jiraskova_MS_742_consolidated.json` | Krnov Jiráskova | 80 | 0 | 0 | MŠ pouze |
| `Kravare_Kouty_ZS_4620_consolidated.json` | Kravaře Kouty | 0 | 73 | 0 | ZŠ pouze |
| `Ostrava_Radvanice_Vrchlickeho_ZS_6660_consolidated.json` | Ostrava Radvanice | 73 | 89 | 0 | MŠ + ZŠ |
| `Ostrava_soukroma_specialni_sro_ZS_5515_consolidated.json` | Ostrava soukromá | 0 | 72 | 41 | ZŠ + ŠD |

### Manuální test

```bash
# Test v headed mode (doporučeno pro první spuštění)
python main.py data/Bruntal_Pionyrska_MS_360_consolidated.json --headed --verbose

# Sledujte:
# - Správné přihlášení
# - Vyplnění všech stránek
# - Finální zprávu: "Děkujeme Vám! Vaše odpovědi byly uloženy."
```

---

## 🐛 Troubleshooting

### Problém: "Configuration file not found"
**Řešení:** Zkontrolujte cestu k JSON souboru

### Problém: "Missing required field: 'code'"
**Řešení:** Přidejte `"code": "ABC123"` do JSON nebo použijte `--code` parametr

### Problém: "At least one school type must have count > 0"
**Řešení:** Nastavte alespoň jeden z MS/ZS/SD > 0

### Problém: Timeout při vyplňování
**Řešení:**
- Zkontrolujte internetové připojení
- Spusťte v headed mode (`--headed`) pro debug
- Zkontrolujte logy v `logs/` adresáři

### Problém: Validační chyba ve formuláři
**Řešení:**
- Zkontrolujte, že JSON klíče odpovídají očekávaným hodnotám
- Ověřte formát školních roků (2022-2023, ne 2022/2023)

---

## 📝 Poznámky

### Důležité!

1. **Kód je single-use** - Po úspěšném dokončení je kód spotřebován
2. **JSON formát roků** - Vždy `"2022-2023"` (s pomlčkou)
3. **Case-insensitive matching** - Témata se matchují bez ohledu na velikost písmen
4. **Nová stránka!** - "Tematická setkávání" není v původním rules.md, ale existuje
5. **Skryté fieldy** - Systém používá JavaScript pro vyplnění skrytých polí

### Limitace

- Podporuje pouze Chrome/Chromium (přes Playwright)
- Vyžaduje internetové připojení
- Formulář musí být dostupný na uvedené URL

---

## 📚 Další dokumentace

- **`plan.md`** - Implementační plán a fáze
- **`rules.md`** - Business pravidla (původní specifikace)
- **`SESSION_CONTEXT.md`** - Aktuální status a quick start guide
- **`docs/workflow_mapping.md`** - Detailní mapování stránek
- **`docs/exploration_findings.md`** - Technické poznatky z explorace

---

## 🤝 Kontakt & Podpora

Pro otázky a podporu kontaktujte správce projektu.

---

## 📜 Licence

Interní projekt - všechna práva vyhrazena.

---

**Status:** ✅ Production Ready
**Last Updated:** 2025-10-14
**Tested:** MŠ section fully tested and working
