# Workflow Mapping - Complete Form Structure

**Test Data:** `Bruntal_Pionyrska_MS_360_consolidated.json` (MS=97, ZS=0, SD=0)
**Access Code:** `00X2ic`
**Date:** 2025-10-14

---

## Summary

Successfully completed form with **12 pages total**:
1. Login
2. Intro page
3-11. MŠ section (9 pages)
12. Completion

**Total screenshots:** 12
**Total time:** ~15 minutes
**Result:** ✅ "Děkujeme Vám! Vaše odpovědi byly uloženy."

---

## Page-by-Page Breakdown

### Page 1: Login

**Screenshot:** `01_login.png`

**Elements:**
- Textbox for access code
- Button "Pokračovat"

**Action:**
- Fill code from JSON: `config['code']`
- Click "Pokračovat"

---

### Page 2: Intro Page

**Screenshot:** `02_intro_page.png`

**Elements:**
- H1 title: "Evidence podpořenosti u výzvy..."
- IČO verification: 60780517
- Instructions text
- Button "Další"

**Action:**
- Verify IČO matches expected value (optional)
- Click "Další"

---

### Page 3: MŠ - Školní asistent

**Screenshot:** `03_ms_skolni_asistent.png`
**Question ID:** `ls-question-text-262621X129X6098`

**Question text:**
> "Uveďte, prosím, dle Vašeho nejlepšího odhadu, jakému počtu dětí na Vaší škole poskytli podporu školní asistenti hrazení ze šablony „1.I/1 Školní asistent MŠ"."

**Page type:** `simple_inputs`
**School type:** `MS`
**Calculation:** `random_multiplier (0.30-0.50) × MS`

**Fields:** 4 textboxes for school years
- Školní rok 2022/2023
- Školní rok 2023/2024
- Školní rok 2024/2025
- Školní rok 2025/2026

**Filled values:** 33, 40, 37, 44

**Validation:** At least one field must be non-zero

---

### Page 4: MŠ - DVPP témata (checkboxy)

**Screenshot:** `04_ms_dvpp_checkboxes.png`
**Question ID:** `ls-question-text-262621X129X6150`

**Question text:**
> "V jaké oblasti jste realizovali vzdělávání pracovníků ve vzdělávání MŠ hrazené ze šablony "1.I/4 Vzdělávání pracovníků ve vzdělávání MŠ"?"

**Page type:** `checkboxes`
**School type:** `MS`
**JSON mapping:** `dvpp_topics["vzdělávání_MŠ_1_I_4"]`

**Available checkboxes:** 32 total
**Checked:** 5 (from JSON)
- pedagogická diagnostika ✓
- inkluze ✓
- zážitková pedagogika ✓
- formativní hodnocení ✓
- umělecká gramotnost ✓

**Implementation:**
- Use JavaScript injection
- Uncheck ALL checkboxes first
- Then check only required ones
- Use text normalization (lowercase, no diacritics)

---

### Page 5: MŠ - DVPP počty dětí

**Screenshot:** `05_ms_dvpp_counts.png`
**Question ID:** `ls-question-text-262621X129X5898`

**Question text:**
> "Uveďte, prosím, dle Vašeho nejlepšího odhadu, s jakým počtem dětí Vaší školy pracovali pracovníci ve vzdělávání podpoření ze šablony "1.I/4 Vzdělávání pracovníků ve vzdělávání MŠ" v tématu:"

**Page type:** `table_counts`
**School type:** `MS`
**Calculation:** `random_multiplier (0.30-0.50) × MS` for EACH field

**Structure:**
- Rows: 5 topics (those checked on previous page)
- Columns: 4 school years (2022/2023, 2023/2024, 2024/2025, 2025/2026)
- Total fields: 20 (5 × 4)

**Note:** Page had 124 total input fields (including hidden/other sections), but only first 28 needed to be filled

**Validation:** Each row must have at least one non-zero value

---

### Page 6: MŠ - SDP/ŽZOR témata (checkboxy)

**Screenshot:** `06_ms_sdp_zzor_checkboxes.png`
**Question ID:** `ls-question-text-262621X129X6215`

**Question text:**
> "V jaké oblasti jste realizovali inovativní vzdělávání dětí v MŠ hrazené ze šablony "1.I/6 Inovativní vzdělávání dětí v MŠ"?"

**Page type:** `checkboxes`
**School type:** `MS`
**JSON mapping:** `sdp_zzor["1.I/6 Inovativní vzdělávání dětí v MŠ"]`

**Available checkboxes:** 17 total
**Checked:** 7 (from JSON)
- čtenářská pre/gramotnost ✓
- matematická pre/gramotnost ✓
- umělecká gramotnost ✓
- přírodovědné a technické vzdělávání ✓
- vzdělávání s využitím nových technologií ✓
- kulturní povědomí a vyjádření ✓
- rozvoj podnikavosti a kreativity ✓

**Implementation:** Same as DVPP checkboxes (JavaScript, uncheck all first, normalize text)

---

### Page 7: MŠ - SDP/ŽZOR počty

**Screenshot:** `07_ms_sdp_zzor_counts.png`
**Question ID:** `ls-question-text-262621X129X6046`

**Question text:**
> "Uveďte prosím, dle Vašeho nejlepšího odhadu, kolik dětí Vaší školy bylo podpořeno šablonou "1.I/6 Inovativní vzdělávání dětí v MŠ" v tématu:"

**Page type:** `table_counts`
**School type:** `MS`
**Calculation:** **EXACT values from JSON** (not random!)

**Structure:**
- Rows: 7 topics (those checked on previous page)
- Columns: 4 school years
- Total fields visible: 28 (7 × 4)
- Total inputs on page: 64 (includes hidden/other sections)

**Data from JSON:**
```json
"čtenářská pre/gramotnost": {"2022-2023": 0, "2023-2024": 19, "2024-2025": 0, "2025-2026": 0}
"matematická pre/gramotnost": {"2022-2023": 0, "2023-2024": 15, ...}
"umělecká gramotnost": {"2022-2023": 0, "2023-2024": 15, ...}
"přírodovědné a technické vzdělávání": {"2022-2023": 0, "2023-2024": 19, ...}
"vzdělávání s využitím nových technologií": {"2022-2023": 0, "2023-2024": 18, ...}
"kulturní povědomí a vyjádření": {"2022-2023": 0, "2023-2024": 19, ...}
"rozvoj podnikavosti a kreativity": {"2022-2023": 0, "2023-2024": 20, ...}
```

**Filled values:** [0,19,0,0, 0,15,0,0, 0,15,0,0, 0,19,0,0, 0,18,0,0, 0,19,0,0, 0,20,0,0]

**Implementation:**
- Map JSON year format: `"2022-2023"` → UI format: `"2022/2023"`
- Fill by sequential order (first 28 fields)
- Use `fill_form` with precise UIDs after validation errors

**Validation:** Each row must have at least one non-zero value

---

### Page 8: MŠ - Tematická setkávání

**Screenshot:** `08_ms_tematicka_setkavani.png`
**Question ID:** Not captured

**Question text:**
> "Uveďte prosím, dle Vašeho nejlepšího odhadu, jaký počet dětí ovlivnila šablona „1.I/8 Odborně zaměřená tematická a komunitní setkávání v MŠ"."

**Page type:** `simple_inputs`
**School type:** `MS`
**Calculation:** `random_multiplier (0.30-0.50) × MS`
**JSON mapping:** NONE (not in JSON - this activity wasn't in test data)

**Fields:** 4 textboxes for school years

**Filled values:** 34, 41, 38, 45

**⚠️ Important:** This page was NOT mentioned in rules.md pseudocode! Discovered during exploration.

---

### Page 9: MŠ - OMJ národnosti

**Screenshot:** `09_ms_omj.png`
**Question ID:** Not captured

**Question text:**
> "Uveďte prosím, dle Vašeho nejlepšího odhadu, jaký počet dětí s OMJ ovlivnil projekt za celou dobu realizace, jejichž národnost je:"

**Page type:** `skip`
**School type:** `MS`
**Rule:** **DO NOT FILL - just click "Další"**

**Fields:** 15 textboxes for different nationalities (romská, ukrajinská, slovenská, polská, německá, maďarská, ruská, bulharská, rumunská, vietnamská, mongolská, řecká, chorvatská, srbská, jiná)

**Action:** Click "Další" without filling anything

**Note:** Form says: "Pokud jste žádné děti s OMJ nepodpořili, pokračujte na další otázku"

---

### Page 10: MŠ - Vedoucí pracovníci

**Screenshot:** `10_ms_vedouci_pracovnici.png`
**Question ID:** Not captured

**Question text:**
> "Uveďte prosím, kolik vedoucích pracovníků ve vzdělávání (vyjma ostatních pracovníků ve vzdělávání) se za celou dobu realizace účastnilo aktivity:"

**Page type:** `fixed_value`
**School type:** `MS`
**Rule:** **Always fill 0**

**Fields:** 1 textbox
- 1.I/4 Vzdělávání pracovníků MŠ

**Filled value:** 0

**Note:** Form says: "V případě, že nedošlo k podpoře žádného vedoucího pracovníka, vyplňte prosím nulu."

---

### Page 11: MŠ - Ukrajinští pracovníci

**Screenshot:** `11_ms_ukrajinsti_pracovnici.png`
**Question ID:** Not captured

**Question text:**
> "Uveďte prosím, kolik pracovníků ve vzdělávání s ukrajinskou národností bylo v jednotlivých letech realizace financováno prostřednictvím šablony:"

**Page type:** `fixed_value`
**School type:** `MS`
**Rule:** **Always fill 0 for all years**

**Fields:** 4 textboxes
- 1.I/1 Školní asistent MŠ
  - Školní rok 2022/2023
  - Školní rok 2023/2024
  - Školní rok 2024/2025
  - Školní rok 2025/2026

**Filled values:** 0, 0, 0, 0

---

### Page 12: Completion

**Screenshot:** `12_completion.png`

**Text:**
> **"Děkujeme Vám!"**
> **"Vaše odpovědi byly uloženy."**

**Elements:**
- Link: "Vytisknout své odpovědi."

**Action:** Done! No further action needed.

---

## Key Learnings

### 1. Page Detection Strategy

✅ **Use `ls-question-text-*` ID and question text content**

Examples:
- `ls-question-text-262621X129X6150` contains "1.I/4" → DVPP MŠ
- `ls-question-text-262621X129X6215` contains "1.I/6" → SDP/ŽZOR MŠ
- Text contains "OMJ" → OMJ page (skip)
- Text contains "vedoucích pracovníků" → Vedoucí pracovníci (fill 0)
- Text contains "ukrajinskou národností" → Ukrajinští pracovníci (fill 0)

### 2. Checkbox Handling

✅ **Use JavaScript injection** (fastest, most reliable)

```javascript
// 1. Uncheck ALL first
const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
allCheckboxes.forEach(cb => {
  cb.checked = false;
  cb.dispatchEvent(new Event('change', { bubbles: true }));
});

// 2. Check only required ones
// Use text normalization for matching
```

❌ **Don't use individual click() calls** - causes stale snapshots

### 3. Text Normalization

**Critical for Czech text matching:**

```javascript
function normalize(text) {
  return text.toLowerCase().trim()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")  // Remove diacritics
    .replace(/\s+/g, " ");
}
```

### 4. Table Filling

**Two approaches:**

A) **By position** (simpler, works if order is predictable):
```javascript
const values = [0, 19, 0, 0, 0, 15, 0, 0, ...];
inputs.forEach((inp, idx) => inp.value = values[idx]);
```

B) **By UID** (more reliable after validation errors):
```javascript
fill_form([
  {"uid": "16_39", "value": "19"},
  {"uid": "16_48", "value": "18"},
  ...
])
```

### 5. Year Format Mapping

**JSON:** `"2022-2023"` (dash)
**UI:** `"2022/2023"` (slash)

Always convert when filling!

### 6. Stale Snapshot Problem

**Problem:** After `fill()` or `click()`, UIDs become stale

**Solution:**
- Use JavaScript injection for bulk operations
- Or take new `snapshot()` after each action

### 7. Hidden Fields

**Watch out:** Some pages have more input fields than visible (e.g., 64 total but only 28 visible)

**Solution:** Fill only the first N fields that correspond to checked topics

### 8. Validation Errors

When form shows: "Jedna nebo více otázek nebyla zodpovězena platným způsobem"

**Steps:**
1. Close error dialog
2. Take new snapshot
3. Use `fill_form()` with precise UIDs
4. Verify all required fields are filled

---

## Page Type Classification

### Simple Inputs
- Školní asistent
- Tematická setkávání
- **Calculation:** Random multiplier

### Checkboxes
- DVPP témata
- SDP/ŽZOR témata
- **Method:** JavaScript injection, normalize text

### Table Counts
- DVPP počty
- SDP/ŽZOR počty
- **DVPP:** Random multiplier
- **SDP/ŽZOR:** Exact from JSON

### Skip Pages
- OMJ národnosti
- **Action:** Just click "Další"

### Fixed Value Pages
- Vedoucí pracovníci (fill 0)
- Ukrajinští pracovníci (fill 0)
- **Action:** Always 0

---

## Implementation Priority

### High Priority (Core Functionality)
1. ✅ Page detection by question text
2. ✅ JavaScript checkbox handling
3. ✅ Text normalization
4. ✅ Year format conversion (dash → slash)
5. ✅ Random multiplier calculation
6. ✅ Exact value filling from JSON

### Medium Priority (Robustness)
1. ⚠️ Validation error handling
2. ⚠️ Hidden field detection
3. ⚠️ Stale snapshot recovery

### Low Priority (Nice to Have)
1. ⏸️ Screenshot before/after each page
2. ⏸️ Detailed logging of all changes
3. ⏸️ Progress tracking

---

**End of Workflow Mapping**
