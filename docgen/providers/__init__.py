"""
Providers pour docGen AI.

Ce module contient les fournisseurs de services externes
comme l'API Groq et la gestion de mémoire.
"""

from .groq_client import GroqClient
from .memory import Memory

__all__ = ["GroqClient", "Memory"] 