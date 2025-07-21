"""
docGen AI - Générateur de documentation Python intelligent avec IA.

Ce package fournit des outils avancés pour générer automatiquement
une documentation riche et intelligente pour les projets Python.
"""

__version__ = "2.0.0"
__author__ = "Genesis Company"
__email__ = "contact@genesis-company.net"

from .docgen import DocGenerator, extract_doc_info, extract_doc_info_enhanced
from .formatter import DocumentationFormatter, format_markdown
from .cli import main

__all__ = [
    "DocGenerator",
    "extract_doc_info", 
    "extract_doc_info_enhanced",
    "DocumentationFormatter",
    "format_markdown",
    "main",
    "__version__",
    "__author__",
    "__email__"
] 