"""Main form filler automation using Playwright"""

import time
from typing import Dict, List, Any
from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError

from src.config_loader import (
    load_config,
    get_school_types,
    get_base_count,
    get_dvpp_topics,
    get_sdp_zzor_topics
)
from src.question_detector import detect_question_type, is_completion_page, QuestionInfo
from src.calculator import generate_counts_for_years, generate_counts_for_topics
from src.text_normalizer import normalize_czech_text, normalize_for_checkbox_matching, compare_texts, convert_year_format
from src.logger_config import (
    setup_logger,
    log_section,
    log_page,
    log_checkbox_change,
    log_field_fill,
    log_table_fill,
    log_success,
    log_error,
    log_warning,
    log_skip
)


class FormFiller:
    """Main form filler class"""

    FORM_URL = "https://evaluace.opjak.cz/index.php/262621"
    SCHOOL_YEARS = ["2022/2023", "2023/2024", "2024/2025"]  # 2025/2026 always stays empty!

    def __init__(
        self,
        config_path: str,
        headless: bool = True,
        verbose: bool = False,
        code_override: str = None
    ):
        """
        Initialize form filler

        Args:
            config_path: Path to JSON configuration file
            headless: Run browser in headless mode
            verbose: Enable verbose logging
            code_override: Override access code from JSON
        """
        self.config = load_config(config_path)
        self.headless = headless
        self.verbose = verbose
        self.logger = setup_logger(verbose=verbose)

        # Override code if provided
        if code_override:
            self.config['code'] = code_override

        self.page_counter = 0

        # Track checked topics for subsequent count pages
        self.last_checked_topics = []

    def run(self) -> bool:
        """
        Main execution method

        Returns:
            True if form completed successfully, False otherwise
        """
        log_section(self.logger, "LimeSurvey Form Filler Started")
        self.logger.info(f"School: {self.config.get('school_name', 'Unknown')}")
        self.logger.info(f"Code: {self.config['code']}")
        self.logger.info(f"School types: {', '.join(get_school_types(self.config))}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            try:
                # Login
                self.login(page)

                # Process pages until completion
                max_pages = 50  # Safety limit
                page_count = 0

                while page_count < max_pages:
                    page_count += 1

                    # Check if completion page
                    if self.is_completion_page_check(page):
                        log_success(self.logger, "Form completed successfully!")
                        log_section(self.logger, "✅ DONE")
                        return True

                    # Process current page
                    success = self.process_current_page(page)

                    if not success:
                        log_warning(self.logger, "Page processing failed, but continuing...")

                    # Click "Další" button
                    self.click_next(page)

                    # Wait for page transition
                    time.sleep(2)

                log_error(self.logger, f"Max pages ({max_pages}) reached without completion")
                return False

            except Exception as e:
                log_error(self.logger, "Fatal error during form filling", e)
                return False

            finally:
                if not self.headless:
                    self.logger.info("Browser will close in 10 seconds...")
                    time.sleep(10)
                browser.close()

    def login(self, page: Page) -> None:
        """Login to survey with access code"""
        log_section(self.logger, "Login")
        self.logger.info(f"Navigating to {self.FORM_URL}")

        page.goto(self.FORM_URL, timeout=60000)
        page.wait_for_load_state('networkidle', timeout=60000)

        # Wait for page to be ready
        time.sleep(2)

        # Fill access code - try multiple selectors
        selectors = [
            'input[type="text"]',
            'input[name="token"]',
            '#token',
            'input.form-control',
        ]

        filled = False
        for selector in selectors:
            try:
                if page.query_selector(selector):
                    page.fill(selector, self.config['code'], timeout=5000)
                    log_field_fill(self.logger, "Access code", self.config['code'])
                    filled = True
                    break
            except:
                continue

        if not filled:
            raise Exception("Could not find access code input field")

        # Click submit - try multiple selectors
        submit_selectors = [
            'button:has-text("Pokračovat")',
            'button[type="submit"]',
            'input[type="submit"]',
            '.btn-primary',
        ]

        clicked = False
        for selector in submit_selectors:
            try:
                if page.query_selector(selector):
                    page.click(selector, timeout=5000)
                    clicked = True
                    break
            except:
                continue

        if not clicked:
            raise Exception("Could not find submit button")

        page.wait_for_load_state('networkidle', timeout=60000)

        log_success(self.logger, "Logged in")

    def is_completion_page_check(self, page: Page) -> bool:
        """Check if current page is completion page"""
        try:
            page_text = page.inner_text('body')
            return is_completion_page(page_text)
        except:
            return False

    def process_current_page(self, page: Page) -> bool:
        """
        Process current page based on detected type

        Returns:
            True if page processed successfully
        """
        try:
            # Get question text
            question_text = self.get_question_text(page)

            if not question_text:
                log_warning(self.logger, "No question text found, might be intro page")
                return True

            # Detect page type
            question_info = detect_question_type(question_text)

            if not question_info:
                log_warning(self.logger, f"Unknown page type: {question_text[:200]}...")
                self.logger.debug(f"Full question text: {question_text}")
                return False

            self.page_counter += 1
            log_page(self.logger, question_info.description, self.page_counter)

            # Dispatch to appropriate handler
            if question_info.page_type == 'intro':
                return True  # Just click next

            elif question_info.page_type == 'skip':
                log_skip(self.logger, question_info.description, "Per business rules")
                return True  # Just click next

            elif question_info.page_type == 'fixed_zero':
                return self.fill_fixed_zero(page, question_info)

            elif question_info.page_type == 'simple_inputs':
                return self.fill_simple_inputs(page, question_info)

            elif question_info.page_type == 'checkboxes':
                return self.fill_checkboxes(page, question_info)

            elif question_info.page_type == 'table_counts':
                return self.fill_table_counts(page, question_info)

            else:
                log_warning(self.logger, f"Unhandled page type: {question_info.page_type}")
                return False

        except Exception as e:
            log_error(self.logger, "Error processing page", e)
            return False

    def get_question_text(self, page: Page) -> str:
        """Get question text from page"""
        try:
            # Try to find ls-question-text-* element
            question_elem = page.query_selector('[id^="ls-question-text-"]')
            if question_elem:
                return question_elem.inner_text()

            # Fallback: get entire page text
            return page.inner_text('body')

        except Exception as e:
            self.logger.debug(f"Could not get question text: {e}")
            return ""

    def click_next(self, page: Page) -> None:
        """Click 'Další' (Next) button"""
        try:
            # Wait a bit before clicking
            time.sleep(1)

            # Try different selectors for "Další" button
            selectors = [
                'button:has-text("Další")',
                'input[type="submit"][value*="Další"]',
                '.ls-move-forward',
            ]

            for selector in selectors:
                try:
                    page.click(selector, timeout=2000)
                    page.wait_for_load_state('networkidle', timeout=10000)
                    return
                except:
                    continue

            log_warning(self.logger, "Could not find 'Další' button")

        except Exception as e:
            log_error(self.logger, "Error clicking Next button", e)

    def fill_fixed_zero(self, page: Page, info: QuestionInfo) -> bool:
        """Fill all fields with 0"""
        try:
            # Use JavaScript to fill all text inputs with 0 (handles hidden fields)
            filled_count = page.evaluate("""() => {
                const inputs = document.querySelectorAll('input[type="text"]');
                let count = 0;
                inputs.forEach(inp => {
                    inp.value = '0';
                    inp.dispatchEvent(new Event('input', {bubbles: true}));
                    inp.dispatchEvent(new Event('change', {bubbles: true}));
                    count++;
                });
                return count;
            }""")

            self.logger.info(f"Filled {filled_count} fields with 0")
            return True

        except Exception as e:
            log_error(self.logger, "Error filling fixed zeros", e)
            return False

    def fill_simple_inputs(self, page: Page, info: QuestionInfo) -> bool:
        """Fill simple year inputs with random values (only first 3 years, 2025/2026 stays empty)"""
        try:
            base_count = get_base_count(self.config, info.school_type)
            counts = generate_counts_for_years(base_count, num_years=3)

            inputs = page.query_selector_all('input[type="text"]')

            if len(inputs) < 3:
                log_warning(self.logger, f"Expected at least 3 inputs, found {len(inputs)}")
                return False

            # Fill only first 3 years, leave 4th (2025/2026) empty
            for i, (year, count) in enumerate(zip(self.SCHOOL_YEARS, counts)):
                inputs[i].fill(str(count))
                # Dispatch events for validation
                inputs[i].evaluate('el => el.dispatchEvent(new Event("input", {bubbles: true}))')
                inputs[i].evaluate('el => el.dispatchEvent(new Event("change", {bubbles: true}))')
                log_field_fill(self.logger, f"Školní rok {year}", count)

            # Log that 4th year is intentionally left empty
            if len(inputs) >= 4:
                self.logger.info(f"Školní rok 2025/2026: (left empty per business rules)")

            return True

        except Exception as e:
            log_error(self.logger, "Error filling simple inputs", e)
            return False

    def fill_checkboxes(self, page: Page, info: QuestionInfo) -> bool:
        """Fill checkboxes based on JSON topics"""
        try:
            # Get topics from JSON
            # Check if this is SDP/ŽZOR or DVPP based on activity code
            # SDP/ŽZOR codes: 1.I/6 (MŠ), 1.I/7 (ZŠ - old), 1.II/9 (ZŠ - primary), 1.V/3 (ŠD)
            # DVPP codes: 1.I/4 (MŠ), 1.I/5 (ZŠ - old), 1.II/7 (ZŠ - primary), 1.V/1 (ŠD)
            if info.activity_code in ['1.I/6', '1.I/7', '1.II/9', '1.V/3']:  # SDP/ŽZOR codes
                # SDP/ŽZOR - topics are dict keys
                topics_data = get_sdp_zzor_topics(self.config, info.json_key)
                topics = list(topics_data.keys())
            else:
                # DVPP - topics are list items (includes 1.I/4, 1.I/5, 1.II/7, 1.V/1)
                topics = get_dvpp_topics(self.config, info.json_key)

            if not topics:
                log_warning(self.logger, f"No topics found for {info.json_key}")
                log_warning(self.logger, f"Available keys: {list(self.config.get('sdp_zzor', {}).keys())}")
                return False

            self.logger.info(f"Checking {len(topics)} checkboxes")

            # Store topics for next page (counts page)
            self.last_checked_topics = topics

            # Use JavaScript to handle checkboxes (fastest and most reliable)
            # First, uncheck all
            page.evaluate("""() => {
                const checkboxes = document.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach(cb => {
                    cb.checked = false;
                    cb.dispatchEvent(new Event('change', {bubbles: true}));
                });
            }""")

            # Then check only required ones
            for topic in topics:
                # Use enhanced normalization that removes parentheses
                normalized_topic = normalize_for_checkbox_matching(topic)

                # Find checkbox by label match
                checked = page.evaluate(f"""(topicNorm) => {{
                    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
                    for (const cb of checkboxes) {{
                        const label = cb.nextElementSibling;
                        if (label && label.textContent) {{
                            // Remove text in parentheses, then normalize
                            let labelText = label.textContent.replace(/\\([^)]*\\)/g, '');
                            const labelNorm = labelText.toLowerCase()
                                .normalize("NFD")
                                .replace(/[\u0300-\u036f]/g, "")
                                .replace(/\\s+/g, " ")
                                .trim();
                            if (labelNorm === topicNorm) {{
                                cb.checked = true;
                                cb.dispatchEvent(new Event('change', {{bubbles: true}}));
                                return true;
                            }}
                        }}
                    }}
                    return false;
                }}""", normalized_topic)

                if checked:
                    log_checkbox_change(self.logger, topic, True)
                else:
                    log_warning(self.logger, f"Could not find checkbox for: {topic}")

            return True

        except Exception as e:
            log_error(self.logger, "Error filling checkboxes", e)
            return False

    def fill_table_counts(self, page: Page, info: QuestionInfo) -> bool:
        """Fill table with topic × year counts (only 3 years, 2025/2026 stays empty)"""
        try:
            base_count = get_base_count(self.config, info.school_type)

            # Get topics and determine values
            if info.calculation == 'from_json':
                # SDP/ŽZOR - exact values from JSON
                topics_data = get_sdp_zzor_topics(self.config, info.json_key)
                topics = list(topics_data.keys())

                # Build flat list of values - only 3 years, then 0 for 2025/2026
                values = []
                for topic in topics:
                    years_data = topics_data[topic]
                    for year_json in ["2022-2023", "2023-2024", "2024-2025"]:
                        values.append(years_data.get(year_json, 0))
                    # Add 0 for 2025/2026 (4th year always empty)
                    values.append(0)

            else:
                # DVPP - random values
                # Try to get topics from JSON first
                dvpp_topics = get_dvpp_topics(self.config, info.json_key)

                # If not in JSON, use topics from previous checkbox page
                if not dvpp_topics and self.last_checked_topics:
                    self.logger.info("Using topics from previous checkbox page")
                    dvpp_topics = self.last_checked_topics

                topics = dvpp_topics
                num_topics = len(topics)
                # Generate only 3 years of random values
                random_values = generate_counts_for_topics(base_count, num_topics, num_years=3)

                # Add 0 for every 4th value (2025/2026)
                values = []
                for i in range(num_topics):
                    # Add 3 random values
                    values.extend(random_values[i*3:(i+1)*3])
                    # Add 0 for 2025/2026
                    values.append(0)

            # Fill inputs using JavaScript (handles hidden fields)
            num_fields = len(topics) * 4
            self.logger.info(f"Filling {num_fields} fields ({len(topics)} topics × 4 years, last year empty)")

            # Use JavaScript to fill fields (only visible rows, skip ls-hidden)
            filled_count = page.evaluate("""(values) => {
                // Find all text inputs that are NOT in ls-hidden rows
                const allInputs = document.querySelectorAll('input[type="text"]');
                const visibleInputs = Array.from(allInputs).filter(input => {
                    // Check if parent row has ls-hidden class
                    const row = input.closest('tr');
                    if (row && row.classList.contains('ls-hidden')) {
                        return false;
                    }
                    return true;
                });

                let count = 0;
                for (let i = 0; i < Math.min(values.length, visibleInputs.length); i++) {
                    visibleInputs[i].value = String(values[i]);
                    visibleInputs[i].dispatchEvent(new Event('input', {bubbles: true}));
                    visibleInputs[i].dispatchEvent(new Event('change', {bubbles: true}));
                    count++;
                }
                return count;
            }""", values)

            self.logger.info(f"Filled {filled_count} fields")

            # Log values for debugging
            all_years = self.SCHOOL_YEARS + ["2025/2026"]  # Include 4th year for logging
            for i in range(min(num_fields, len(values))):
                topic_idx = i // 4
                year_idx = i % 4
                if topic_idx < len(topics):
                    year_label = all_years[year_idx] if year_idx < len(all_years) else f"Year {year_idx}"
                    log_table_fill(self.logger, topics[topic_idx], year_label, values[i])

            return True

        except Exception as e:
            log_error(self.logger, "Error filling table counts", e)
            return False
