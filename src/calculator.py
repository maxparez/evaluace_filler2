"""Calculation utilities for random multipliers and count generation"""

import random
from typing import List, Optional


def random_multiplier(min_val: float = 0.30, max_val: float = 0.50) -> float:
    """
    Generate random multiplier between min and max values

    Args:
        min_val: Minimum multiplier value (default: 0.30)
        max_val: Maximum multiplier value (default: 0.50)

    Returns:
        Random float between min_val and max_val

    Examples:
        >>> multiplier = random_multiplier()
        >>> 0.30 <= multiplier <= 0.50
        True
    """
    return random.uniform(min_val, max_val)


def calculate_count(base_count: int, multiplier: Optional[float] = None) -> int:
    """
    Calculate count with multiplier and round to nearest integer

    Args:
        base_count: Base student/child count (MS, ZS, or SD)
        multiplier: Optional specific multiplier (if None, generates random)

    Returns:
        Rounded count (integer)

    Examples:
        >>> calculate_count(97, 0.35)
        34
        >>> calculate_count(100, 0.40)
        40
    """
    if multiplier is None:
        multiplier = random_multiplier()

    return round(base_count * multiplier)


def generate_counts_for_years(base_count: int, num_years: int = 4) -> List[int]:
    """
    Generate random counts for multiple school years

    Each year gets a different random multiplier for variation

    Args:
        base_count: Base student/child count
        num_years: Number of years to generate (default: 4)

    Returns:
        List of calculated counts for each year

    Examples:
        >>> counts = generate_counts_for_years(97, 4)
        >>> len(counts)
        4
        >>> all(29 <= c <= 49 for c in counts)  # 0.30*97 to 0.50*97
        True
    """
    return [calculate_count(base_count) for _ in range(num_years)]


def generate_counts_for_topics(
    base_count: int,
    num_topics: int,
    num_years: int = 4
) -> List[int]:
    """
    Generate random counts for multiple topics and years

    Used for DVPP table filling where we have N topics × 4 years

    Args:
        base_count: Base student/child count
        num_topics: Number of topics (rows)
        num_years: Number of years (columns, default: 4)

    Returns:
        Flat list of counts in row-major order (topic1_year1, topic1_year2, ...)

    Examples:
        >>> counts = generate_counts_for_topics(97, 5, 4)
        >>> len(counts)
        20
    """
    counts = []

    for _ in range(num_topics):
        for _ in range(num_years):
            counts.append(calculate_count(base_count))

    return counts


def validate_at_least_one_nonzero(counts: List[int]) -> bool:
    """
    Validate that at least one count is non-zero

    Used for form validation - each row must have at least one non-zero value

    Args:
        counts: List of counts to validate

    Returns:
        True if at least one count is non-zero

    Examples:
        >>> validate_at_least_one_nonzero([0, 0, 0, 5])
        True
        >>> validate_at_least_one_nonzero([0, 0, 0, 0])
        False
    """
    return any(count > 0 for count in counts)


def get_year_list() -> List[str]:
    """
    Get list of school years in UI format (with slashes)

    Returns:
        List of 4 school year strings

    Examples:
        >>> get_year_list()
        ['2022/2023', '2023/2024', '2024/2025', '2025/2026']
    """
    return [
        "2022/2023",
        "2023/2024",
        "2024/2025",
        "2025/2026"
    ]
