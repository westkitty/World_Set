"""WORLD KIT - a concept-driven modular environment generation system.

The pipeline is driven entirely by :mod:`world_kit.dna`.  Nothing downstream
(geometry, materials, showcase, exports) hard-codes a dimension, a colour or a
name: it all reads the WORLD DNA spec, so the kit can be re-targeted at another
concept by editing one module.
"""

__all__ = ["__version__", "KIT_ROOT"]

import os

__version__ = "1.0.0"

KIT_ROOT = os.path.dirname(os.path.abspath(__file__))
