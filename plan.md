# Implementační plán - LimeSurvey Automatické Vyplňování

## 🎯 Cíl projektu

Vytvořit automatizační nástroj v **Python + Playwright** pro vyplňování dotazníků LimeSurvey na základě JSON konfigurace.

**Status:** ✅ **MŠ PRODUCTION READY** | 🔄 ZŠ/ŠD In Progress

---

## 📊 Progress Overview

| Fáze | Status | Completion | Notes |
|------|--------|------------|-------|
| Fáze 1: Exploration | ✅ Complete | 100% | All 12 MŠ pages documented |
| Fáze 2: Python Setup | ✅ Complete | 100% | Venv, dependencies installed |
| Fáze 3: Core Modules | ✅ Complete | 100% | All 6 modules working |
| Fáze 4: MŠ Testing | ✅ Complete | 100% | Bruntal test passed |
| Fáze 5: ZŠ/ŠD Support | 🔄 In Progress | 60% | Need activity code detection |
| Fáze 6: Reliability | ⏳ Pending | 0% | Error recovery, retry logic |

---

## 📋 Fáze 1-4: HOTOVO ✅

### ✅ Fáze 1: Exploration (COMPLETE)
- Chrome DevTools MCP installed
- Form manually explored
- 12 pages documented
- Screenshots captured
- Critical findings documented

### ✅ Fáze 2: Python projekt setup (COMPLETE)
- Virtual environment created
- Playwright + pytest installed
- Project structure created
- requirements.txt generated

### ✅ Fáze 3: Core moduly (COMPLETE)
Všechny moduly implementovány:
- `config_loader.py` - JSON loading & validation
- `text_normalizer.py` - Czech text normalization + activity code extraction
- `calculator.py` - Random multipliers
- `logger_config.py` - Logging with emoji
- `question_detector.py` - Page type detection
- `form_filler.py` - Main Playwright automation

### ✅ Fáze 4: MŠ Testing (COMPLETE)
- Bruntal_Pionyrska_MS_360 test passed
- All 10 MŠ pages filled successfully
- Form completed: "Děkujeme Vám!"
- Headed and headless modes work
- Comprehensive logging verified

---

## 🔄 Fáze 5: ZŠ/ŠD Support (IN PROGRESS - 60%)

### ✅ Hotovo
1. ✅ ŠD page detection added (1.V/1, 1.V/3)
2. ✅ Activity code regex fixed (supports I, II, V, X)
3. ✅ Checkbox logic updated for ŠD codes

### ⏳ Zbývá
1. **Add ZŠ DVPP detection (1.II/7)** - CRITICAL
2. **Add ZŠ SDP/ŽZOR detection (1.II/9)** - CRITICAL
3. **Test with Kravare_Kouty (ZŠ only)**
4. **Test with Ostrava_Radvanice (ZŠ+ŠD)**
5. **Verify multi-school combinations**

### Implementation Plan for ZŠ

**File:** `src/question_detector.py`

**Add to `detect_zs_pages()` function:**

```python
def detect_zs_pages(normalized: str, activity_code: str) -> Optional[QuestionInfo]:
    """Detect ZŠ-specific pages"""

    # 1.II/7 DVPP ZŠ - Checkboxes
    if activity_code == "1.II/7" and \
       "vzdelavani pracovniku" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='ZS',
            activity_code='1.II/7',
            json_key='vzdělávání_ZŠ_1_II_7',
            description="ZŠ - DVPP témata (checkboxes)"
        )

    # 1.II/7 DVPP ZŠ - Counts
    if activity_code == "1.II/7" and \
       "vzdelavani pracovniku" in normalized and \
       ("pocet" in normalized or "s jakym poctem" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='ZS',
            activity_code='1.II/7',
            calculation='random',
            description="ZŠ - DVPP počty"
        )

    # 1.II/9 SDP/ŽZOR ZŠ - Checkboxes
    if activity_code == "1.II/9" and \
       "inovativni vzdelavani" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='ZS',
            activity_code='1.II/9',
            json_key='1.II/9 Inovativní vzdělávání žáků v ZŠ',
            description="ZŠ - SDP/ŽZOR témata (checkboxes)"
        )

    # 1.II/9 SDP/ŽZOR ZŠ - Counts
    if activity_code == "1.II/9" and \
       "inovativni vzdelavani" in normalized and \
       ("pocet" in normalized or "kolik" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='ZS',
            activity_code='1.II/9',
            calculation='from_json',
            json_key='1.II/9 Inovativní vzdělávání žáků v ZŠ',
            description="ZŠ - SDP/ŽZOR počty (exact from JSON)"
        )

    # ... rest of ZŠ detection
```

**Update `fill_checkboxes()` in `src/form_filler.py`:**

```python
# Add 1.II/7 and 1.II/9 to appropriate lists
if info.activity_code in ['1.I/6', '1.II/9', '1.V/3']:  # SDP/ŽZOR codes
    # ...
else:  # DVPP codes: 1.I/4, 1.II/7, 1.V/1
    # ...
```

---

## ⏳ Fáze 6: Reliability Improvements (PENDING)

### Cíl
Zvýšit spolehlivost na 99%+ pro produkční použití

### Priority 1: Error Recovery

**1. Retry Logic for Failed Pages**
```python
def process_current_page_with_retry(self, page: Page, max_retries=3) -> bool:
    """Process page with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            success = self.process_current_page(page)
            if success:
                return True

            self.logger.warning(f"Page processing failed, attempt {attempt+1}/{max_retries}")

            # Take screenshot for debugging
            page.screenshot(path=f"logs/error_attempt_{attempt}.png")

            # Wait before retry
            time.sleep(3)

        except Exception as e:
            self.logger.error(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise

    return False
```

**2. Validation Error Detection**
```python
def check_validation_errors(self, page: Page) -> bool:
    """Check if page has validation errors"""
    error_selectors = [
        'text="Jedna nebo více otázek"',
        '.alert-danger',
        '.error-message',
    ]

    for selector in error_selectors:
        if page.query_selector(selector):
            error_text = page.inner_text(selector)
            self.logger.error(f"Validation error: {error_text}")
            return True

    return False
```

**3. Automatic Error Recovery**
```python
def recover_from_validation_error(self, page: Page, info: QuestionInfo) -> bool:
    """Try to recover from validation error"""
    self.logger.info("Attempting error recovery...")

    # Close error dialog
    try:
        page.click('button:has-text("Zavřít")', timeout=2000)
    except:
        pass

    # Retake snapshot
    time.sleep(1)

    # Retry filling with different approach
    # ... implementation specific to error type

    return True
```

### Priority 2: Page Detection Improvements

**1. Fallback Detection Methods**
```python
def detect_question_type_with_fallback(self, question_text: str, page: Page) -> Optional[QuestionInfo]:
    """Detect with multiple fallback strategies"""

    # Primary: Activity code + keywords
    info = detect_question_type(question_text)
    if info:
        return info

    # Fallback 1: Check for specific elements
    if page.query_selector('input[type="checkbox"]'):
        return self._detect_checkbox_page(question_text, page)

    # Fallback 2: Count input fields
    input_count = len(page.query_selector_all('input[type="text"]'))
    if input_count == 4:
        return self._detect_simple_inputs(question_text)

    # Fallback 3: Check table structure
    if page.query_selector('table'):
        return self._detect_table_page(question_text, page)

    return None
```

**2. Smart Page Type Guessing**
```python
def guess_page_type_from_structure(self, page: Page) -> str:
    """Guess page type from DOM structure"""

    checkboxes = len(page.query_selector_all('input[type="checkbox"]'))
    text_inputs = len(page.query_selector_all('input[type="text"]'))
    tables = len(page.query_selector_all('table'))

    if checkboxes > 5:
        return 'checkboxes'
    elif text_inputs == 4 and tables == 0:
        return 'simple_inputs'
    elif text_inputs > 10 and tables > 0:
        return 'table_counts'
    else:
        return 'unknown'
```

### Priority 3: Logging & Debugging

**1. Screenshot on Every Page**
```python
def take_page_screenshot(self, page: Page, page_name: str) -> None:
    """Take screenshot for debugging"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"logs/screenshots/{timestamp}_{page_name}.png"
    page.screenshot(path=filename)
    self.logger.debug(f"Screenshot saved: {filename}")
```

**2. Detailed State Logging**
```python
def log_page_state(self, page: Page) -> None:
    """Log current page state for debugging"""
    self.logger.debug(f"URL: {page.url}")
    self.logger.debug(f"Title: {page.title()}")

    question = page.query_selector('[id^="ls-question-text-"]')
    if question:
        self.logger.debug(f"Question ID: {question.get_attribute('id')}")

    input_count = len(page.query_selector_all('input'))
    self.logger.debug(f"Input fields: {input_count}")
```

**3. Performance Metrics**
```python
class PerformanceTracker:
    """Track performance metrics"""

    def __init__(self):
        self.start_time = time.time()
        self.page_times = []

    def mark_page_start(self):
        self.page_start = time.time()

    def mark_page_end(self, page_name: str):
        duration = time.time() - self.page_start
        self.page_times.append((page_name, duration))
        return duration

    def get_summary(self):
        total = time.time() - self.start_time
        avg = sum(t for _, t in self.page_times) / len(self.page_times)
        return {
            'total': total,
            'average_per_page': avg,
            'pages': len(self.page_times)
        }
```

### Priority 4: Configuration Validation

**1. Pre-flight Checks**
```python
def validate_config_completeness(config: Dict) -> List[str]:
    """Validate config has all required data for school types"""
    warnings = []

    for school_type in get_school_types(config):
        # Check DVPP topics
        dvpp_key = f"vzdělávání_{school_type}_..."
        if dvpp_key not in config.get('dvpp_topics', {}):
            warnings.append(f"Missing DVPP topics for {school_type}")

        # Check SDP/ŽZOR data
        # ... similar checks

    return warnings
```

**2. JSON Schema Validation**
```python
import jsonschema

SCHEMA = {
    "type": "object",
    "required": ["code"],
    "properties": {
        "code": {"type": "string", "minLength": 1},
        "MS": {"type": "integer", "minimum": 0},
        "ZS": {"type": "integer", "minimum": 0},
        "SD": {"type": "integer", "minimum": 0},
        # ... more schema
    }
}

def validate_json_schema(config: Dict) -> None:
    """Validate against JSON schema"""
    jsonschema.validate(instance=config, schema=SCHEMA)
```

---

## 🎯 Roadmap pro Dosažení Vysoké Spolehlivosti

### Milestone 1: Complete ZŠ/ŠD Support (1-2 hodiny)
- [ ] Add 1.II/7 detection
- [ ] Add 1.II/9 detection
- [ ] Test all 5 JSON files
- [ ] Verify all pass

### Milestone 2: Error Recovery (2-3 hodiny)
- [ ] Add retry logic
- [ ] Add validation error detection
- [ ] Add automatic recovery
- [ ] Test with intentional errors

### Milestone 3: Advanced Detection (1-2 hodiny)
- [ ] Add fallback detection methods
- [ ] Add structure-based guessing
- [ ] Test edge cases

### Milestone 4: Production Hardening (2-3 hodiny)
- [ ] Add screenshot on error
- [ ] Add performance tracking
- [ ] Add detailed state logging
- [ ] Add pre-flight validation

### Milestone 5: Testing & Validation (2-3 hodiny)
- [ ] Unit tests for all modules
- [ ] Integration tests
- [ ] Stress testing (100+ runs)
- [ ] Edge case testing

---

## 📊 Success Criteria

### Phase 5 Complete (ZŠ/ŠD)
- [ ] All 5 test files pass
- [ ] ZŠ pages detected correctly
- [ ] ŠD pages detected correctly
- [ ] Multi-school combinations work

### Phase 6 Complete (Reliability)
- [ ] 99%+ success rate on repeated runs
- [ ] Automatic error recovery works
- [ ] Clear error messages for failures
- [ ] Performance < 3 minutes per form
- [ ] No manual intervention needed

---

## 🔧 Technical Debt & Future Improvements

### Code Quality
- [ ] Add type hints everywhere
- [ ] Add comprehensive docstrings
- [ ] Refactor large functions
- [ ] Extract magic constants

### Testing
- [ ] Unit tests for utilities
- [ ] Integration tests for workflows
- [ ] Mock tests for external dependencies
- [ ] Performance benchmarks

### Features
- [ ] Resume from failed page
- [ ] Batch processing multiple JSONs
- [ ] Dry-run mode (validate only)
- [ ] Export filled form as PDF

### DevOps
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Docker container
- [ ] Monitoring & alerting

---

## 📝 Notes

### Activity Code Reference
```
MŠ:  1.I/4 (DVPP)    1.I/6 (SDP/ŽZOR)    1.I/8 (Tematická)
ZŠ:  1.II/7 (DVPP)   1.II/9 (SDP/ŽZOR)   [unknown Tematická]
ŠD:  1.V/1 (DVPP)    1.V/3 (SDP/ŽZOR)    [unknown Tematická]
```

### JSON Key Reference
```
DVPP:
- vzdělávání_MŠ_1_I_4
- vzdělávání_ZŠ_1_II_7
- vzdělávání_ŠD_ŠK_1_V_1

SDP/ŽZOR:
- 1.I/6 Inovativní vzdělávání dětí v MŠ
- 1.II/9 Inovativní vzdělávání žáků v ZŠ
- 1.V/3 Inovativní vzdělávání účastníků zájmového vzdělávání v ŠD/ŠK
```

---

**Last Updated:** 2025-10-14 21:00
**Status:** MŠ ✅ Production Ready | ZŠ/ŠD 🔄 60% Complete
**Next Milestone:** Complete ZŠ detection → Test all files → Add reliability improvements
