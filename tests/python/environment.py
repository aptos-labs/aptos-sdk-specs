"""
Behave environment hooks.
This file is automatically loaded by behave from the test root directory.
"""

import sys
import os

# Add support directory to Python path for imports
support_dir = os.path.join(os.path.dirname(__file__), "support")
if support_dir not in sys.path:
    sys.path.insert(0, support_dir)

# Add current directory for steps imports
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from support.world import AptosWorld


def before_all(context):
    """Called once before all tests."""
    pass


def before_scenario(context, scenario):
    """Called before each scenario - create fresh world."""
    context.world = AptosWorld()


def after_scenario(context, scenario):
    """Called after each scenario - cleanup."""
    if hasattr(context, "world"):
        context.world.reset()


def after_all(context):
    """Called once after all tests."""
    pass
