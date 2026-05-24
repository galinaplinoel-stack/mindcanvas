"""MindCanvas — AI Mind Mapping

Interactive mind mapping powered by AI. Generate, visualize,
and organize ideas on an infinite canvas.
"""

__version__ = "1.0.0"
__author__ = "MindCanvas Team"

from .canvas import Canvas
from .generator import Generator
from .layout import AutoLayout
from .models import Node, Edge, MindMap
from .templates import TemplateLibrary
from .exporter import Exporter

__all__ = [
    "Canvas", "Generator", "AutoLayout",
    "Node", "Edge", "MindMap",
    "TemplateLibrary", "Exporter",
]
