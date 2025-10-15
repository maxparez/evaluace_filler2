"""Page type detection based on question text patterns"""

from typing import Optional, Dict, Literal
from src.text_normalizer import normalize_czech_text, contains_normalized, extract_activity_code


PageType = Literal[
    'simple_inputs',      # Simple year inputs with random values
    'checkboxes',         # Topic checkboxes from JSON
    'table_counts',       # Table with topic × year counts
    'skip',              # Skip page (no filling)
    'fixed_zero',        # Fill all fields with 0
    'intro',             # Introduction page (just click Next)
    'completion'         # Completion page (done!)
]

SchoolType = Literal['MS', 'ZS', 'SD']


class QuestionInfo:
    """Information about detected question/page"""

    def __init__(
        self,
        page_type: PageType,
        school_type: Optional[SchoolType] = None,
        activity_code: Optional[str] = None,
        calculation: Optional[str] = None,
        json_key: Optional[str] = None,
        description: str = ""
    ):
        self.page_type = page_type
        self.school_type = school_type
        self.activity_code = activity_code
        self.calculation = calculation  # 'random', 'from_json', or None
        self.json_key = json_key
        self.description = description

    def __repr__(self) -> str:
        return f"QuestionInfo(type={self.page_type}, school={self.school_type}, desc={self.description})"


def detect_question_type(question_text: str) -> Optional[QuestionInfo]:
    """
    Detect question/page type from question text

    Args:
        question_text: Text from ls-question-text-* element

    Returns:
        QuestionInfo object with detected page type, or None if unknown

    Detection logic based on docs/workflow_mapping.md and docs/exploration_findings.md
    """
    if not question_text:
        return None

    normalized = normalize_czech_text(question_text)

    # Special pages (order matters!)

    # Completion page
    if "dekujeme vam" in normalized and "odpovedi byly ulozeny" in normalized:
        return QuestionInfo(
            page_type='completion',
            description="Completion page"
        )

    # OMJ page (skip)
    if ("omj" in normalized or "narodnosti" in normalized) and \
       ("deti s omj" in normalized or "deti s omj ovlivnil" in normalized):
        return QuestionInfo(
            page_type='skip',
            description="OMJ národnosti (skip)"
        )

    # Vedoucí pracovníci (fill 0)
    if "vedoucich pracovniku" in normalized and "ve vzdelavani" in normalized:
        return QuestionInfo(
            page_type='fixed_zero',
            description="Vedoucí pracovníci (fill 0)"
        )

    # Ukrajinští pracovníci (fill 0)
    if "ukrajinskou narodnosti" in normalized or \
       ("pracovniku ve vzdelavani" in normalized and "ukrajin" in normalized):
        return QuestionInfo(
            page_type='fixed_zero',
            description="Ukrajinští pracovníci (fill 0)"
        )

    # Introduction page (IČO verification)
    if "evidence podporenosti" in normalized and "ico" in normalized:
        return QuestionInfo(
            page_type='intro',
            description="Introduction page"
        )

    # Extract activity code for further detection
    activity_code = extract_activity_code(question_text)

    # MŠ pages
    if detect_ms_pages(normalized, activity_code):
        return detect_ms_pages(normalized, activity_code)

    # ZŠ pages
    if detect_zs_pages(normalized, activity_code):
        return detect_zs_pages(normalized, activity_code)

    # ŠD pages
    if detect_sd_pages(normalized, activity_code):
        return detect_sd_pages(normalized, activity_code)

    return None


def detect_ms_pages(normalized: str, activity_code: str) -> Optional[QuestionInfo]:
    """Detect MŠ-specific pages"""

    # 1.I/1 Školní asistent MŠ
    if activity_code == "1.I/1" or \
       ("skolni asistent" in normalized and "ms" in normalized):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='MS',
            activity_code='1.I/1',
            calculation='random',
            description="MŠ - Školní asistent"
        )

    # 1.I/4 DVPP MŠ - Checkboxes
    if activity_code == "1.I/4" and \
       "vzdelavani pracovniku" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='MS',
            activity_code='1.I/4',
            json_key='vzdělávání_MŠ_1_I_4',
            description="MŠ - DVPP témata (checkboxes)"
        )

    # 1.I/4 DVPP MŠ - Counts
    if activity_code == "1.I/4" and \
       "vzdelavani pracovniku" in normalized and \
       ("pocet deti" in normalized or "s jakym poctem" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='MS',
            activity_code='1.I/4',
            calculation='random',
            description="MŠ - DVPP počty"
        )

    # 1.I/6 SDP/ŽZOR MŠ - Checkboxes
    if activity_code == "1.I/6" and \
       "inovativni vzdelavani" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='MS',
            activity_code='1.I/6',
            json_key='1.I/6 Inovativní vzdělávání dětí v MŠ',
            description="MŠ - SDP/ŽZOR témata (checkboxes)"
        )

    # 1.I/6 SDP/ŽZOR MŠ - Counts
    if activity_code == "1.I/6" and \
       "inovativni vzdelavani" in normalized and \
       ("pocet deti" in normalized or "kolik deti" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='MS',
            activity_code='1.I/6',
            calculation='from_json',
            json_key='1.I/6 Inovativní vzdělávání dětí v MŠ',
            description="MŠ - SDP/ŽZOR počty (exact from JSON)"
        )

    # 1.I/8 Tematická setkávání MŠ (NEW! Not in rules.md)
    if activity_code == "1.I/8" or \
       ("tematicka" in normalized and "komunitni setkavani" in normalized and "ms" in normalized):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='MS',
            activity_code='1.I/8',
            calculation='random',
            description="MŠ - Tematická setkávání"
        )

    return None


def detect_zs_pages(normalized: str, activity_code: str) -> Optional[QuestionInfo]:
    """Detect ZŠ-specific pages"""

    # Similar structure to MŠ but with ZŠ identifiers
    # To be implemented when testing with ZŠ data

    # 1.II/1 Školní asistent ZŠ (PRIMARY CODE!)
    if activity_code == "1.II/1" or \
       ("jakemu poctu zaku" in normalized and "poskytli podporu" in normalized):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='ZS',
            activity_code='1.II/1',
            calculation='random',
            description="ZŠ - Školní asistent"
        )

    # 1.I/2 Školní asistent ZŠ (fallback/alternative code)
    if ("skolni asistent" in normalized and "zs" in normalized) or \
       (activity_code == "1.I/2"):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='ZS',
            activity_code='1.I/2',
            calculation='random',
            description="ZŠ - Školní asistent"
        )

    # 1.II/7 DVPP ZŠ - Checkboxes (PRIMARY ZŠ DVPP CODE!)
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

    # 1.II/9 SDP/ŽZOR ZŠ - Checkboxes (PRIMARY ZŠ SDP/ŽZOR CODE!)
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
       ("pocet" in normalized or "kolik" in normalized or "s jakym" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='ZS',
            activity_code='1.II/9',
            calculation='from_json',
            json_key='1.II/9 Inovativní vzdělávání žáků v ZŠ',
            description="ZŠ - SDP/ŽZOR počty (exact from JSON)"
        )

    # 1.II/11 Tematická setkávání ZŠ (similar to MŠ 1.I/8)
    if activity_code == "1.II/11" or \
       ("tematicka" in normalized and "komunitni setkavani" in normalized and ("zs" in normalized or "zaku" in normalized)):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='ZS',
            activity_code='1.II/11',
            calculation='random',
            description="ZŠ - Tematická setkávání"
        )

    # 1.I/5 DVPP ZŠ - Alternative code (fallback)
    if activity_code == "1.I/5" and "vzdelavani pracovniku" in normalized:
        if "v jake oblasti" in normalized:
            return QuestionInfo(
                page_type='checkboxes',
                school_type='ZS',
                activity_code='1.I/5',
                json_key='vzdělávání_ZŠ_1_I_5',
                description="ZŠ - DVPP témata (checkboxes)"
            )
        else:
            return QuestionInfo(
                page_type='table_counts',
                school_type='ZS',
                activity_code='1.I/5',
                calculation='random',
                description="ZŠ - DVPP počty"
            )

    # 1.I/7 SDP/ŽZOR ZŠ - Alternative code (fallback)
    if activity_code == "1.I/7" and "inovativni vzdelavani" in normalized:
        if "v jake oblasti" in normalized:
            return QuestionInfo(
                page_type='checkboxes',
                school_type='ZS',
                activity_code='1.I/7',
                json_key='1.I/7 Inovativní vzdělávání žáků v ZŠ',
                description="ZŠ - SDP/ŽZOR témata (checkboxes)"
            )
        else:
            return QuestionInfo(
                page_type='table_counts',
                school_type='ZS',
                activity_code='1.I/7',
                calculation='from_json',
                json_key='1.I/7 Inovativní vzdělávání žáků v ZŠ',
                description="ZŠ - SDP/ŽZOR počty (exact from JSON)"
            )

    return None


def detect_sd_pages(normalized: str, activity_code: str) -> Optional[QuestionInfo]:
    """Detect ŠD-specific pages"""

    # 1.V/1 DVPP ŠD/ŠK - Checkboxes
    if activity_code == "1.V/1" and \
       "vzdelavani pracovniku" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='SD',
            activity_code='1.V/1',
            json_key='vzdělávání_ŠD_ŠK_1_V_1',
            description="ŠD - DVPP témata (checkboxes)"
        )

    # 1.V/1 DVPP ŠD/ŠK - Counts
    if activity_code == "1.V/1" and \
       "vzdelavani pracovniku" in normalized and \
       ("pocet" in normalized or "s jakym poctem" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='SD',
            activity_code='1.V/1',
            calculation='random',
            description="ŠD - DVPP počty"
        )

    # 1.V/3 SDP/ŽZOR ŠD/ŠK - Checkboxes
    if activity_code == "1.V/3" and \
       "inovativni vzdelavani" in normalized and \
       "v jake oblasti" in normalized:
        return QuestionInfo(
            page_type='checkboxes',
            school_type='SD',
            activity_code='1.V/3',
            json_key='1.V/3 Inovativní vzdělávání účastníků zájmového vzdělávání v ŠD/ŠK',
            description="ŠD - SDP/ŽZOR témata (checkboxes)"
        )

    # 1.V/3 SDP/ŽZOR ŠD/ŠK - Counts
    if activity_code == "1.V/3" and \
       "inovativni vzdelavani" in normalized and \
       ("pocet" in normalized or "kolik" in normalized or "s jakym" in normalized):
        return QuestionInfo(
            page_type='table_counts',
            school_type='SD',
            activity_code='1.V/3',
            calculation='from_json',
            json_key='1.V/3 Inovativní vzdělávání účastníků zájmového vzdělávání v ŠD/ŠK',
            description="ŠD - SDP/ŽZOR počty (exact from JSON)"
        )

    # 1.I/3 Školní asistent ŠD (if needed)
    if ("skolni asistent" in normalized and ("sd" in normalized or "sk" in normalized)) or \
       (activity_code == "1.I/3"):
        return QuestionInfo(
            page_type='simple_inputs',
            school_type='SD',
            activity_code='1.I/3',
            calculation='random',
            description="ŠD - Školní asistent"
        )

    return None


def is_completion_page(page_text: str) -> bool:
    """
    Quick check if current page is the completion page

    Args:
        page_text: Full page text content

    Returns:
        True if this is the completion page
    """
    normalized = normalize_czech_text(page_text)
    return "dekujeme vam" in normalized and "odpovedi byly ulozeny" in normalized
