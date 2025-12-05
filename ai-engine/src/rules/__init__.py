"""
Rule definitions for disease diagnosis.
This package contains rule modules for different categories of diseases.
"""

from .viral_rules import InfluenzaRules, Covid19Rules, CommonColdRules
from .bacterial_rules import StrepThroatRules, PneumoniaRules, BronchitisRules

__all__ = [
    'InfluenzaRules', 'Covid19Rules', 'CommonColdRules',
    'StrepThroatRules', 'PneumoniaRules', 'BronchitisRules'
]

# Rules will be organized into separate modules:
# - viral_rules.py - Rules for viral diseases (Influenza, COVID-19, Common Cold)
# - bacterial_rules.py - Rules for bacterial diseases (Strep Throat, Pneumonia, Bronchitis)

