"""
Behave environment hooks.
This module provides hooks that behave calls at various points during test execution.

Note: This file needs to be imported or the hooks registered in the main environment.py
at the test root, or steps need to import and use the World class directly.
"""

import sys
import os

# Add support directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from world import AptosWorld


def before_scenario(context, scenario):
    """Called before each scenario - create fresh world."""
    context.world = AptosWorld()


def after_scenario(context, scenario):
    """Called after each scenario - cleanup."""
    if hasattr(context, "world"):
        context.world.reset()


def before_all(context):
    """Called once before all tests."""
    # Add support directory to Python path for imports
    support_dir = os.path.join(os.path.dirname(__file__))
    if support_dir not in sys.path:
        sys.path.insert(0, support_dir)


def after_all(context):
    """Called once after all tests."""
    pass
