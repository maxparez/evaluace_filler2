"""Configuration loader and validator for JSON input files"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


def load_config(filepath: str) -> Dict[str, Any]:
    """
    Load and validate JSON configuration file

    Args:
        filepath: Path to JSON configuration file

    Returns:
        Validated configuration dictionary

    Raises:
        ConfigValidationError: If validation fails
        FileNotFoundError: If file doesn't exist
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    with open(path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Validate required fields
    _validate_config(config)

    return config


def _validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration structure

    Args:
        config: Configuration dictionary to validate

    Raises:
        ConfigValidationError: If validation fails
    """
    # Required: access code
    if 'code' not in config or not config['code']:
        raise ConfigValidationError("Missing required field: 'code'")

    # Required: at least one school type with count > 0
    school_types = ['MS', 'ZS', 'SD']
    has_school = False

    for school_type in school_types:
        if school_type in config:
            if not isinstance(config[school_type], int):
                raise ConfigValidationError(f"Field '{school_type}' must be an integer")
            if config[school_type] > 0:
                has_school = True

    if not has_school:
        raise ConfigValidationError(
            "At least one school type (MS, ZS, SD) must have a count > 0"
        )

    # Optional: dvpp_topics validation
    if 'dvpp_topics' in config:
        if not isinstance(config['dvpp_topics'], dict):
            raise ConfigValidationError("Field 'dvpp_topics' must be a dictionary")

        for key, topics in config['dvpp_topics'].items():
            if not isinstance(topics, list):
                raise ConfigValidationError(
                    f"dvpp_topics['{key}'] must be a list of strings"
                )

    # Optional: sdp_zzor validation
    if 'sdp_zzor' in config:
        if not isinstance(config['sdp_zzor'], dict):
            raise ConfigValidationError("Field 'sdp_zzor' must be a dictionary")

        for activity, topics in config['sdp_zzor'].items():
            if not isinstance(topics, dict):
                raise ConfigValidationError(
                    f"sdp_zzor['{activity}'] must be a dictionary"
                )

            for topic, years in topics.items():
                if not isinstance(years, dict):
                    raise ConfigValidationError(
                        f"sdp_zzor['{activity}']['{topic}'] must be a dictionary"
                    )


def get_school_types(config: Dict[str, Any]) -> list[str]:
    """
    Get list of school types that need to be processed (count > 0)

    Args:
        config: Configuration dictionary

    Returns:
        List of school type codes (e.g., ['MS', 'ZS'])
    """
    school_types = []

    for school_type in ['MS', 'ZS', 'SD']:
        if config.get(school_type, 0) > 0:
            school_types.append(school_type)

    return school_types


def get_base_count(config: Dict[str, Any], school_type: str) -> int:
    """
    Get base student/child count for a school type

    Args:
        config: Configuration dictionary
        school_type: School type code (MS, ZS, SD)

    Returns:
        Base count for the school type
    """
    return config.get(school_type, 0)


def get_dvpp_topics(config: Dict[str, Any], activity_key: str) -> list[str]:
    """
    Get DVPP topics for an activity

    Args:
        config: Configuration dictionary
        activity_key: Activity key (e.g., 'vzdělávání_MŠ_1_I_4')

    Returns:
        List of topic names, or empty list if not found
    """
    dvpp_topics = config.get('dvpp_topics', {})
    return dvpp_topics.get(activity_key, [])


def get_sdp_zzor_topics(config: Dict[str, Any], activity_key: str) -> Dict[str, Dict[str, int]]:
    """
    Get SDP/ŽZOR topics with counts for an activity

    Args:
        config: Configuration dictionary
        activity_key: Activity key (e.g., '1.I/6 Inovativní vzdělávání dětí v MŠ')

    Returns:
        Dictionary of topics with year counts, or empty dict if not found
    """
    sdp_zzor = config.get('sdp_zzor', {})
    return sdp_zzor.get(activity_key, {})
