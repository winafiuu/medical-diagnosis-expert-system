"""
Certainty Factor (CF) calculation utilities.
This module provides functions for combining and calculating certainty factors
in the medical diagnosis expert system.
"""


def combine_cf_and(cf1, cf2):
    """
    Combine certainty factors using AND logic (minimum).
    Used when ALL conditions must be true.
    
    Args:
        cf1 (float): First certainty factor (0.0 to 1.0)
        cf2 (float): Second certainty factor (0.0 to 1.0)
        
    Returns:
        float: Combined certainty factor
        
    Example:
        >>> combine_cf_and(0.8, 0.6)
        0.6
    """
    return min(cf1, cf2)


def combine_cf_or(cf1, cf2):
    """
    Combine certainty factors using OR logic (maximum).
    Used when ANY condition being true is sufficient.
    
    Args:
        cf1 (float): First certainty factor (0.0 to 1.0)
        cf2 (float): Second certainty factor (0.0 to 1.0)
        
    Returns:
        float: Combined certainty factor
        
    Example:
        >>> combine_cf_or(0.8, 0.6)
        0.8
    """
    return max(cf1, cf2)


def combine_cf_multiple_and(*cfs):
    """
    Combine multiple certainty factors using AND logic.
    
    Args:
        *cfs: Variable number of certainty factors
        
    Returns:
        float: Combined certainty factor (minimum of all)
        
    Example:
        >>> combine_cf_multiple_and(0.8, 0.6, 0.9, 0.7)
        0.6
    """
    if not cfs:
        return 0.0
    return min(cfs)


def combine_cf_multiple_or(*cfs):
    """
    Combine multiple certainty factors using OR logic.
    
    Args:
        *cfs: Variable number of certainty factors
        
    Returns:
        float: Combined certainty factor (maximum of all)
        
    Example:
        >>> combine_cf_multiple_or(0.8, 0.6, 0.9, 0.7)
        0.9
    """
    if not cfs:
        return 0.0
    return max(cfs)


def apply_rule_confidence(evidence_cf, rule_cf):
    """
    Apply rule confidence to evidence certainty.
    Final CF = Evidence CF × Rule Reliability CF
    
    This represents how much we trust the rule itself, independent of
    the evidence certainty.
    
    Args:
        evidence_cf (float): Certainty factor from evidence (0.0 to 1.0)
        rule_cf (float): Reliability of the rule itself (0.0 to 1.0)
        
    Returns:
        float: Final certainty factor
        
    Example:
        >>> apply_rule_confidence(0.8, 0.9)
        0.72
    """
    return evidence_cf * rule_cf


def combine_parallel_evidence(cf1, cf2):
    """
    Combine certainty factors from parallel (independent) evidence.
    Uses the formula: CF1 + CF2 - (CF1 × CF2)
    
    This is used when we have multiple independent pieces of evidence
    supporting the same conclusion.
    
    Args:
        cf1 (float): First certainty factor (0.0 to 1.0)
        cf2 (float): Second certainty factor (0.0 to 1.0)
        
    Returns:
        float: Combined certainty factor
        
    Example:
        >>> combine_parallel_evidence(0.6, 0.7)
        0.88
    """
    return cf1 + cf2 - (cf1 * cf2)


def combine_conflicting_evidence(cf_positive, cf_negative):
    """
    Combine conflicting evidence (one supporting, one contradicting).
    Uses the formula: (CF_pos - CF_neg) / (1 - min(|CF_pos|, |CF_neg|))
    
    Args:
        cf_positive (float): Certainty factor supporting the hypothesis
        cf_negative (float): Certainty factor contradicting the hypothesis
        
    Returns:
        float: Combined certainty factor
        
    Example:
        >>> combine_conflicting_evidence(0.8, 0.3)
        0.714
    """
    if cf_positive == cf_negative:
        return 0.0
    
    denominator = 1 - min(abs(cf_positive), abs(cf_negative))
    if denominator == 0:
        return 0.0
    
    return (cf_positive - cf_negative) / denominator


def normalize_cf(cf):
    """
    Normalize a certainty factor to ensure it's within valid range [0.0, 1.0].
    
    Args:
        cf (float): Certainty factor to normalize
        
    Returns:
        float: Normalized certainty factor
        
    Example:
        >>> normalize_cf(1.5)
        1.0
        >>> normalize_cf(-0.2)
        0.0
    """
    return max(0.0, min(1.0, cf))


def get_cf_category(cf):
    """
    Categorize a certainty factor into a human-readable confidence level.
    
    Args:
        cf (float): Certainty factor (0.0 to 1.0)
        
    Returns:
        str: Confidence category
        
    Example:
        >>> get_cf_category(0.85)
        'Very High'
    """
    if cf >= 0.9:
        return "Very High"
    elif cf >= 0.7:
        return "High"
    elif cf >= 0.5:
        return "Moderate"
    elif cf >= 0.3:
        return "Low"
    else:
        return "Very Low"


def calculate_weighted_average_cf(cf_list, weights=None):
    """
    Calculate weighted average of multiple certainty factors.
    
    Args:
        cf_list (list): List of certainty factors
        weights (list): Optional list of weights (must sum to 1.0)
        
    Returns:
        float: Weighted average certainty factor
        
    Example:
        >>> calculate_weighted_average_cf([0.8, 0.6, 0.9], [0.5, 0.3, 0.2])
        0.75
    """
    if not cf_list:
        return 0.0
    
    if weights is None:
        # Equal weights
        return sum(cf_list) / len(cf_list)
    
    if len(cf_list) != len(weights):
        raise ValueError("cf_list and weights must have the same length")
    
    if abs(sum(weights) - 1.0) > 0.001:
        raise ValueError("Weights must sum to 1.0")
    
    return sum(cf * weight for cf, weight in zip(cf_list, weights))
