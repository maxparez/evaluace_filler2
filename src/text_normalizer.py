"""Czech text normalization utilities for label matching"""

import unicodedata
import re


def normalize_czech_text(text: str) -> str:
    """
    Normalize Czech text for comparison
    - Remove diacritics (á → a, ž → z, ů → u)
    - Convert to lowercase
    - Collapse whitespace
    - Trim leading/trailing spaces

    Args:
        text: Input text with Czech diacritics

    Returns:
        Normalized text without diacritics

    Examples:
        >>> normalize_czech_text("Umělecká gramotnost  ")
        "umelecka gramotnost"
        >>> normalize_czech_text("Čtenářská pre/gramotnost")
        "ctenarska pre/gramotnost"
    """
    if not text:
        return ""

    # NFD normalization - decompose characters (á → a + ́)
    nfd = unicodedata.normalize('NFD', text)

    # Remove diacritics (combining characters)
    no_diacritics = ''.join(
        char for char in nfd
        if unicodedata.category(char) != 'Mn'
    )

    # Lowercase and collapse whitespace
    normalized = re.sub(r'\s+', ' ', no_diacritics.lower().strip())

    return normalized


def compare_texts(text1: str, text2: str) -> bool:
    """
    Case-insensitive, diacritics-insensitive text comparison

    Args:
        text1: First text to compare
        text2: Second text to compare

    Returns:
        True if texts match after normalization

    Examples:
        >>> compare_texts("inkluze", "Inkluze  ")
        True
        >>> compare_texts("formativní hodnocení", "formativni hodnoceni")
        True
    """
    return normalize_czech_text(text1) == normalize_czech_text(text2)


def first_word_match(json_text: str, ui_text: str) -> bool:
    """
    Match only the first word of two texts
    Used for EVVO special case matching

    Args:
        json_text: Text from JSON configuration
        ui_text: Text from UI label

    Returns:
        True if first words match

    Examples:
        >>> first_word_match("EVVO - environmentální", "EVVO")
        True
        >>> first_word_match("inkluze", "inkluze včetně...")
        True
    """
    json_words = normalize_czech_text(json_text).split()
    ui_words = normalize_czech_text(ui_text).split()

    if not json_words or not ui_words:
        return False

    return json_words[0] == ui_words[0]


def contains_normalized(haystack: str, needle: str) -> bool:
    """
    Check if normalized needle is in normalized haystack

    Args:
        haystack: Text to search in
        needle: Text to search for

    Returns:
        True if needle found in haystack (case/diacritics-insensitive)

    Examples:
        >>> contains_normalized("Školní asistent MŠ", "asistent")
        True
        >>> contains_normalized("1.I/4 Vzdělávání", "vzdelavani")
        True
    """
    return normalize_czech_text(needle) in normalize_czech_text(haystack)


def convert_year_format(json_year: str) -> str:
    """
    Convert year format from JSON (dash) to UI (slash)

    Args:
        json_year: Year string in JSON format (e.g., "2022-2023")

    Returns:
        Year string in UI format (e.g., "2022/2023")

    Examples:
        >>> convert_year_format("2022-2023")
        "2022/2023"
        >>> convert_year_format("2023-2024")
        "2023/2024"
    """
    return json_year.replace('-', '/')


def normalize_for_checkbox_matching(text: str) -> str:
    """
    Normalize text specifically for checkbox label matching
    - Remove text in parentheses (e.g., "(environmentální ... osvěta)")
    - Remove diacritics
    - Lowercase
    - Collapse whitespace

    Args:
        text: Input text with possible parentheses

    Returns:
        Normalized text without parentheses content

    Examples:
        >>> normalize_for_checkbox_matching("EVVO (environmentální vzdělávání)")
        "evvo"
        >>> normalize_for_checkbox_matching("inkluze včetně primární prevence")
        "inkluze vcetne primarni prevence"
    """
    # Remove text in parentheses
    no_parens = re.sub(r'\([^)]*\)', '', text)

    # Apply standard normalization
    return normalize_czech_text(no_parens)


def extract_activity_code(text: str) -> str:
    """
    Extract activity code from question text (e.g., "1.I/4", "1.I/6", "1.V/1")

    Args:
        text: Question text containing activity code

    Returns:
        Activity code or empty string if not found

    Examples:
        >>> extract_activity_code("šablony 1.I/4 Vzdělávání")
        "1.I/4"
        >>> extract_activity_code("1.I/6 Inovativní vzdělávání")
        "1.I/6"
        >>> extract_activity_code("1.V/1 Vzdělávání pracovníků")
        "1.V/1"
        >>> extract_activity_code("1.II/9 Inovativní")
        "1.II/9"
    """
    # Pattern: digit.Roman/digit (e.g., 1.I/4, 1.II/9, 1.V/1)
    # Roman numerals: I, II, III, IV, V, VI, VII, VIII, IX, X
    pattern = r'\d+\.[IVX]+/\d+'
    match = re.search(pattern, text)

    return match.group(0) if match else ""
