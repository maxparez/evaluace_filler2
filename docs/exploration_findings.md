# Exploration Findings - Critical Information for Implementation

**Date:** 2025-10-14
**Test Data:** `Bruntal_Pionyrska_MS_360_consolidated.json`
**Status:** ✅ Complete - Form successfully submitted

---

## Executive Summary

Successfully explored and completed entire MŠ form section using Chrome DevTools MCP in headed mode. All 12 pages documented with screenshots, Question IDs, and exact field structures. Ready for Python + Playwright implementation.

**Key Success Metrics:**
- ✅ 12 pages navigated successfully
- ✅ 12 screenshots captured
- ✅ All data from JSON correctly mapped
- ✅ Form completed: "Děkujeme Vám! Vaše odpovědi byly uloženy."
- ✅ Zero manual intervention needed after exploration start

---

## Critical Discoveries

### 1. NEW PAGE NOT IN RULES.MD! ⚠️

**Page 8: Tematická setkávání (1.I/8)**

This page was **NOT mentioned** in the original rules.md pseudocode, but appeared in the actual form flow.

**Question:** "Uveďte prosím, dle Vašeho nejlepšího odhadu, jaký počet dětí ovlivnila šablona „1.I/8 Odborně zaměřená tematická a komunitní setkávání v MŠ"."

**Solution:**
- Use random multipliers (0.30-0.50 × MS) like other non-JSON fields
- 4 school years fields
- Not in JSON, so calculate on-the-fly

**Location in workflow:** After SDP/ŽZOR counts, before OMJ

---

### 2. Stale Snapshot Problem - Real Experience

**Problem:**
After `fill()` or `click()`, UIDs from previous snapshot become invalid.

**Example that FAILED:**
```javascript
take_snapshot()  // UIDs: 1_6, 1_7
fill(uid="1_6", value="code")  // Works
click(uid="1_7")  // ERROR: stale snapshot!
```

**Solution that WORKED:**
```javascript
take_snapshot()
fill(uid="1_6", value="code")
take_snapshot()  // NEW snapshot with NEW UIDs
click(uid="2_7")  // Works!
```

**BETTER Solution - JavaScript Injection:**
```javascript
evaluate_script(`() => {
  document.querySelector('input').value = 'code';
  document.querySelector('button').click();
}`)
// No stale snapshots - single operation!
```

---

### 3. Hidden Fields Problem

**Page 5 (DVPP počty) and Page 7 (SDP/ŽZOR počty) have MORE input fields than visible:**

- **Visible fields:** 28 (7 topics × 4 years)
- **Total inputs on page:** 64!

**Why?** Form likely has:
- Hidden sections for other activities
- Pre-rendered fields for all possible topics
- Disabled/invisible inputs

**Solution:**
- Fill only first N fields that correspond to checked topics
- Use positional filling: `values[0...27]`
- Or use precise UIDs from snapshot

---

### 4. Validation Error Recovery

**Scenario:** Clicked "Další" but got error:
> "Jedna nebo více otázek nebyla zodpovězena platným způsobem."

**What happened:**
- JavaScript filled values, but some didn't persist
- Particularly "přírodovědné a technické vzdělávání" had wrong value (20 instead of 19)
- Last 3 topics were empty

**Root cause:**
- `value =` assignment without `dispatchEvent('change')`
- Browser didn't recognize the value change

**Solution that WORKED:**
```javascript
input.value = newValue;
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
```

**Recovery steps:**
1. Close error dialog (click "Zavřít")
2. Take new snapshot
3. Use `fill_form()` with precise UIDs
4. Verify all fields have correct values
5. Try "Další" again

---

### 5. Year Format Conversion

**CRITICAL:** JSON uses dash, UI uses slash!

| JSON Format | UI Format | Status |
|-------------|-----------|--------|
| `"2022-2023"` | `"2022/2023"` | ✅ Must convert |
| `"2023-2024"` | `"2023/2024"` | ✅ Must convert |
| `"2024-2025"` | `"2024/2025"` | ✅ Must convert |
| `"2025-2026"` | `"2025/2026"` | ✅ Must convert |

**Python implementation:**
```python
ui_year = json_year.replace('-', '/')
```

---

### 6. Text Normalization for Czech

**Essential for matching checkbox labels!**

**Example mismatch:**
- JSON: `"umělecká gramotnost"`
- UI: `"umělecká gramotnost  "` (extra spaces)
- UI: `"Umělecká gramotnost"` (capital)

**Working normalization:**
```javascript
function normalize(text) {
  return text.toLowerCase().trim()
    .normalize("NFD")  // Decompose á → a + ́
    .replace(/[\u0300-\u036f]/g, "")  // Remove diacritics
    .replace(/\s+/g, " ");  // Collapse whitespace
}
```

**Python equivalent:**
```python
import unicodedata
import re

def normalize_czech_text(text: str) -> str:
    nfd = unicodedata.normalize('NFD', text)
    no_diacritics = nfd.encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'\s+', ' ', no_diacritics.lower().strip())
```

---

### 7. Checkbox Label Structure

**IMPORTANT:** Label is **SIBLING** of checkbox, NOT parent!

**HTML structure:**
```html
<checkbox id="chk1" />
<StaticText>Label text</StaticText>
```

**Wrong approach:**
```javascript
const label = checkbox.parentElement.querySelector('label');  // FAILS
```

**Correct approach:**
```javascript
const label = checkbox.nextElementSibling;  // WORKS
if (label && label.textContent) {
  // Use label.textContent for matching
}
```

---

### 8. DVPP vs SDP/ŽZOR Calculation Difference

**CRITICAL DISTINCTION:**

| Section | Calculation | Source |
|---------|-------------|--------|
| DVPP počty | `round(random(0.30, 0.50) × MS)` | **Random** |
| SDP/ŽZOR počty | Exact values | **From JSON** |

**Why different?**
- DVPP topics not in JSON → use random estimates
- SDP/ŽZOR has explicit counts in JSON → use exact values

**Example:**
```json
// DVPP - NO counts in JSON
"vzdělávání_MŠ_1_I_4": [
  "inkluze",  // <-- Just topic names, NO counts!
  "formativní hodnocení"
]

// SDP/ŽZOR - HAS counts in JSON
"1.I/6 Inovativní vzdělávání dětí v MŠ": {
  "inkluze včetně primární prevence": {
    "2022-2023": 22,  // <-- Explicit counts!
    "2023-2024": 0
  }
}
```

---

### 9. Skip vs Fill-Zero Pages

**Two types of "empty" pages:**

**Type A: SKIP (no filling at all)**
- Page: OMJ národnosti
- Rule: Click "Další" without filling
- Reason: Form says "Pokud jste žádné děti s OMJ nepodpořili, pokračujte na další otázku"

**Type B: FILL ZERO**
- Page: Vedoucí pracovníci, Ukrajinští pracovníci
- Rule: Fill 0 in all fields
- Reason: Form says "V případě, že nedošlo k podpoře..., vyplňte prosím nulu."

**Detection:**
```python
if "OMJ" in question_text or "národnost" in question_text:
    # Skip - just click Další
    page.click('button:has-text("Další")')
elif "vedoucích pracovníků" in question_text:
    # Fill 0
    fill_all_fields_with_zero()
elif "ukrajinskou národností" in question_text:
    # Fill 0
    fill_all_fields_with_zero()
```

---

### 10. Question ID Pattern

**All form pages have unique Question IDs:**

Format: `ls-question-text-262621X[section]X[question]`

**Examples from exploration:**
- `ls-question-text-262621X129X6098` → Školní asistent
- `ls-question-text-262621X129X6150` → DVPP témata checkboxy
- `ls-question-text-262621X129X5898` → DVPP počty
- `ls-question-text-262621X129X6215` → SDP/ŽZOR témata
- `ls-question-text-262621X129X6046` → SDP/ŽZOR počty

**Section codes:**
- `129` = MŠ section
- `131` = ZŠ section (expected, not tested)
- Unknown for ŠD

**Usage:**
```python
question_div = page.query_selector('[id^="ls-question-text-"]')
question_id = question_div.get_attribute('id')
question_text = question_div.inner_text()
```

---

### 11. Page Type Detection Strategy

**Best approach: Combination of Question ID + Text Content**

```python
def detect_page_type(page):
    question = page.query_selector('[id^="ls-question-text-"]')
    text = question.inner_text().lower()

    # Pattern matching (order matters!)
    if "1.i/1" in text and "asistent" in text:
        return "ms_skolni_asistent"
    elif "1.i/4" in text and "vzdělávání pracovníků" in text:
        if "tématu" in text:
            return "ms_dvpp_counts"
        else:
            return "ms_dvpp_checkboxes"
    elif "1.i/6" in text and "inovativní vzdělávání" in text:
        if "tématu" in text or "počet" in text:
            return "ms_sdp_zzor_counts"
        else:
            return "ms_sdp_zzor_checkboxes"
    elif "1.i/8" in text and "tematická" in text:
        return "ms_tematicka_setkavani"
    elif "omj" in text or "národnost" in text:
        return "omj_skip"
    elif "vedoucích pracovníků" in text:
        return "vedouci_pracovnici"
    elif "ukrajinskou národností" in text:
        return "ukrajinsti_pracovnici"
    else:
        return "unknown"
```

---

### 12. Completion Detection

**Final page has unique text:**

```python
if "Děkujeme Vám!" in page.inner_text() and \
   "Vaše odpovědi byly uloženy" in page.inner_text():
    return True  # Success!
```

**No Question ID** on completion page.

**Screenshot:** `12_completion.png`

---

## Technical Implementation Notes

### Chrome DevTools MCP vs Playwright

**Chrome DevTools MCP (used for exploration):**
- ✅ Perfect for interactive exploration
- ✅ Great for debugging (visible browser)
- ❌ Stale snapshot issues
- ❌ Need UIDs from snapshots
- ❌ More complex error handling

**Playwright (recommended for production):**
- ✅ More stable API
- ✅ Better selectors (CSS, XPath, text)
- ✅ Built-in waiting and retry logic
- ✅ Cleaner error handling
- ✅ No stale reference issues
- ✅ Same automation capabilities

**Conclusion:** Use Playwright for final implementation, not Chrome DevTools MCP.

---

### Recommended Playwright Selectors

**Instead of UIDs, use semantic selectors:**

```python
# Bad (Chrome DevTools MCP style)
page.fill("uid=16_46", "0")

# Good (Playwright style)
page.fill('input[description*="Školní rok 2022/2023"]', "0")

# Better (by label)
page.fill('text="Školní rok 2022/2023" >> .. >> input', "0")

# Best (by context)
page.locator('text="přírodovědné a technické vzdělávání"') \
    .locator('..') \
    .locator('text="2023/2024" >> .. >> input') \
    .fill("19")
```

---

### JavaScript Injection in Playwright

**Equivalent to Chrome DevTools MCP's `evaluate_script`:**

```python
page.evaluate("""() => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => {
        cb.checked = false;
        cb.dispatchEvent(new Event('change', { bubbles: true }));
    });
}""")
```

**Or with arguments:**

```python
topics = ["inkluze", "formativní hodnocení"]
page.evaluate("""(topics) => {
    // ... JavaScript using topics array
}""", topics)
```

---

## Data Mapping Summary

### From JSON to UI - Complete Mapping

**1. Login:**
- JSON: `config['code']`
- UI: textbox → value

**2. Školní asistent (MS):**
- JSON: `config['MS']` = 97
- UI: 4 fields → `round(random(0.30, 0.50) × 97)`

**3. DVPP témata checkboxy (MS):**
- JSON: `config['dvpp_topics']['vzdělávání_MŠ_1_I_4']` = array of topic names
- UI: Check checkboxes where label matches (normalized)

**4. DVPP počty (MS):**
- JSON: N/A (no counts)
- UI: For each checked topic × 4 years → `round(random(0.30, 0.50) × 97)`

**5. SDP/ŽZOR témata checkboxy (MS):**
- JSON: `config['sdp_zzor']['1.I/6 Inovativní vzdělávání dětí v MŠ']` = dict keys
- UI: Check checkboxes where label matches keys

**6. SDP/ŽZOR počty (MS):**
- JSON: `config['sdp_zzor']['1.I/6...']['čtenářská pre/gramotnost']['2022-2023']` = 0
- UI: Exact values from JSON (convert year format!)

**7. Tematická setkávání (MS):**
- JSON: N/A
- UI: 4 fields → `round(random(0.30, 0.50) × 97)`

**8. OMJ (MS):**
- JSON: N/A
- UI: Skip (no filling)

**9. Vedoucí pracovníci (MS):**
- JSON: N/A
- UI: Fill 0

**10. Ukrajinští pracovníci (MS):**
- JSON: N/A
- UI: Fill all 0

---

## Error Scenarios Encountered

### Error 1: Validation Failed on SDP/ŽZOR Counts

**Symptom:**
> "Jedna nebo více otázek nebyla zodpovězena platným způsobem."

**Cause:**
- JavaScript `input.value = X` without `dispatchEvent`
- Some fields didn't persist values

**Fix:**
```javascript
input.value = newValue;
input.dispatchEvent(new Event('input', { bubbles: true }));
input.dispatchEvent(new Event('change', { bubbles: true }));
```

### Error 2: Stale Snapshot

**Symptom:**
> "This uid is coming from a stale snapshot."

**Cause:**
- Used UID from old snapshot after page change

**Fix:**
- Take new snapshot after every `fill()` or `click()`
- Or use JavaScript injection for bulk operations

---

## Files Created During Exploration

```
ai_evaluace_filler2/
├── plan.md                           # Overall implementation plan
├── README.md                          # Updated for Python + Playwright
├── .gitignore                         # Python-specific ignores
├── docs/
│   ├── exploration_workflow.md        # Pre-exploration checklist
│   ├── workflow_mapping.md            # Page-by-page detailed mapping
│   └── exploration_findings.md        # This file
└── screenshots/
    ├── 01_login.png
    ├── 02_intro_page.png
    ├── 03_ms_skolni_asistent.png
    ├── 04_ms_dvpp_checkboxes.png
    ├── 05_ms_dvpp_counts.png
    ├── 06_ms_sdp_zzor_checkboxes.png
    ├── 07_ms_sdp_zzor_counts.png
    ├── 08_ms_tematicka_setkavani.png  # NEW - not in rules.md!
    ├── 09_ms_omj.png
    ├── 10_ms_vedouci_pracovnici.png
    ├── 11_ms_ukrajinsti_pracovnici.png
    └── 12_completion.png
```

---

## Next Steps for Implementation

### Phase 2: Python + Playwright Setup

**Priority 1: Environment Setup**
```bash
python -m venv venv
source venv/bin/activate
pip install playwright pytest
playwright install chromium
```

**Priority 2: Core Modules (in order)**
1. `src/config_loader.py` - Load & validate JSON
2. `src/text_normalizer.py` - Czech text normalization
3. `src/calculator.py` - Random multipliers
4. `src/question_detector.py` - Page type detection
5. `src/form_filler.py` - Main Playwright automation
6. `main.py` - CLI entry point

**Priority 3: Testing**
- Use `Bruntal_Pionyrska_MS_360_consolidated.json` for first test
- Verify against screenshots from exploration
- Then test with other JSON files (ZŠ, ŠD combinations)

---

## Questions for Future Sessions

### Answered ✅
- ✅ What's the exact page order? → 12 pages documented
- ✅ Are all DVPP fields random? → Yes, no counts in JSON
- ✅ Are all SDP/ŽZOR fields from JSON? → Yes, exact values
- ✅ Do we skip or fill OMJ? → Skip (no filling)
- ✅ Is there a Tematická setkávání page? → YES! (newly discovered)

### Still Unknown ⚠️
- ❓ What happens if MS=0 but ZS>0? (only ZŠ section shows?)
- ❓ What if all MS, ZS, SD > 0? (all 3 sections?)
- ❓ Are ZŠ and ŠD workflows similar to MŠ? (expect yes)
- ❓ Do ZŠ/ŠD also have Tematická setkávání pages?
- ❓ Do ZŠ/ŠD also have Ukrajinští pracovníci pages? (rules.md says only MŠ)

---

## Success Criteria for Phase 2

- [ ] Python modules created and tested
- [ ] Successfully fills form with test JSON
- [ ] Completion message detected
- [ ] Screenshots match exploration screenshots
- [ ] Works with headed and headless modes
- [ ] Handles all page types correctly
- [ ] Text normalization works for Czech
- [ ] Year format conversion works
- [ ] Random multipliers generate reasonable values
- [ ] Error handling for validation failures

---

**End of Exploration Findings**

**Status:** Ready for implementation 🚀
