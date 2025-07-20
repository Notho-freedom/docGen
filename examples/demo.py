#!/usr/bin/env python3
"""
Module de démonstration pour docGen AI.

Ce module illustre les capacités avancées du générateur de documentation
intelligent avec des exemples concrets de fonctions et classes bien documentées.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import json
import time
from functools import wraps

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QualityLevel(Enum):
    """Niveaux de qualité pour l'évaluation du code."""
    EXCELLENT = "A"
    GOOD = "B"
    AVERAGE = "C"
    POOR = "D"
    CRITICAL = "E"

@dataclass
class CodeMetrics:
    """Métriques de qualité du code."""
    complexity: float
    lines_of_code: int
    documentation_coverage: float
    quality_grade: QualityLevel
    
    def __post_init__(self):
        """Validation des métriques après initialisation."""
        if self.complexity < 0:
            raise ValueError("La complexité ne peut pas être négative")
        if self.documentation_coverage < 0 or self.documentation_coverage > 100:
            raise ValueError("La couverture doit être entre 0 et 100%")

def performance_monitor(func):
    """
    Décorateur pour surveiller les performances des fonctions.
    
    Args:
        func: La fonction à décorer
        
    Returns:
        La fonction décorée avec surveillance des performances
        
    Example:
        >>> @performance_monitor
        >>> def slow_function():
        >>>     time.sleep(1)
        >>>     return "Done"
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"Fonction {func.__name__} exécutée en {end_time - start_time:.4f} secondes")
        return result
    return wrapper

class DocumentationAnalyzer:
    """
    Analyseur de documentation intelligent.
    
    Cette classe fournit des outils avancés pour analyser et améliorer
    la documentation de code Python. Elle utilise des algorithmes
    d'analyse statique et peut intégrer des suggestions d'IA.
    
    Attributes:
        config (Dict[str, Any]): Configuration de l'analyseur
        cache (Dict[str, Any]): Cache pour les résultats d'analyse
        
    Example:
        >>> analyzer = DocumentationAnalyzer()
        >>> metrics = analyzer.analyze_file("mon_fichier.py")
        >>> print(f"Qualité: {metrics.quality_grade}")
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialise l'analyseur de documentation.
        
        Args:
            config: Configuration optionnelle pour l'analyseur
            
        Raises:
            ValueError: Si la configuration est invalide
        """
        self.config = config or {}
        self.cache = {}
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Valide la configuration de l'analyseur."""
        required_keys = ["max_complexity", "min_coverage"]
        for key in required_keys:
            if key not in self.config:
                self.config[key] = self._get_default_config()[key]
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retourne la configuration par défaut."""
        return {
            "max_complexity": 10,
            "min_coverage": 80.0,
            "enable_cache": True,
            "ai_enhancement": False
        }
    
    @performance_monitor
    def analyze_file(self, file_path: Union[str, Path]) -> CodeMetrics:
        """
        Analyse un fichier Python et retourne ses métriques.
        
        Cette méthode effectue une analyse complète du fichier en calculant
        la complexité cyclomatique, la couverture de documentation et
        d'autres métriques de qualité importantes.
        
        Args:
            file_path: Chemin vers le fichier Python à analyser
            
        Returns:
            CodeMetrics: Métriques calculées pour le fichier
            
        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            SyntaxError: Si le fichier contient des erreurs de syntaxe
            
        Example:
            >>> analyzer = DocumentationAnalyzer()
            >>> metrics = analyzer.analyze_file("src/main.py")
            >>> if metrics.quality_grade == QualityLevel.EXCELLENT:
            >>>     print("Code de qualité excellente!")
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
        # Vérifier le cache
        cache_key = str(file_path.absolute())
        if self.config.get("enable_cache") and cache_key in self.cache:
            logger.info(f"Résultats récupérés du cache pour {file_path}")
            return self.cache[cache_key]
        
        # Analyse du fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calcul des métriques
        complexity = self._calculate_complexity(content)
        lines_of_code = len(content.split('\n'))
        documentation_coverage = self._calculate_documentation_coverage(content)
        quality_grade = self._determine_quality_grade(complexity, documentation_coverage)
        
        metrics = CodeMetrics(
            complexity=complexity,
            lines_of_code=lines_of_code,
            documentation_coverage=documentation_coverage,
            quality_grade=quality_grade
        )
        
        # Mise en cache
        if self.config.get("enable_cache"):
            self.cache[cache_key] = metrics
        
        return metrics
    
    def _calculate_complexity(self, content: str) -> float:
        """
        Calcule la complexité cyclomatique du code.
        
        Args:
            content: Contenu du fichier Python
            
        Returns:
            float: Complexité cyclomatique moyenne
        """
        # Implémentation simplifiée pour la démo
        complexity_indicators = ['if ', 'elif ', 'else:', 'for ', 'while ', 'except', 'with ']
        total_complexity = 1  # Base complexity
        
        for indicator in complexity_indicators:
            total_complexity += content.count(indicator)
        
        lines = content.split('\n')
        return total_complexity / max(len(lines), 1)
    
    def _calculate_documentation_coverage(self, content: str) -> float:
        """
        Calcule la couverture de documentation.
        
        Args:
            content: Contenu du fichier Python
            
        Returns:
            float: Pourcentage de couverture (0-100)
        """
        lines = content.split('\n')
        documented_lines = 0
        total_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('class '):
                total_lines += 1
                # Vérifier s'il y a une docstring dans les 3 lignes suivantes
                line_index = lines.index(line)
                for i in range(1, 4):
                    if line_index + i < len(lines):
                        next_line = lines[line_index + i].strip()
                        if next_line.startswith('"""') or next_line.startswith("'''"):
                            documented_lines += 1
                            break
        
        return (documented_lines / max(total_lines, 1)) * 100
    
    def _determine_quality_grade(self, complexity: float, coverage: float) -> QualityLevel:
        """
        Détermine la note de qualité basée sur les métriques.
        
        Args:
            complexity: Complexité cyclomatique
            coverage: Couverture de documentation
            
        Returns:
            QualityLevel: Note de qualité déterminée
        """
        score = 0
        
        # Score basé sur la complexité
        if complexity <= 3:
            score += 40
        elif complexity <= 7:
            score += 30
        elif complexity <= 10:
            score += 20
        else:
            score += 10
        
        # Score basé sur la couverture
        if coverage >= 90:
            score += 40
        elif coverage >= 70:
            score += 30
        elif coverage >= 50:
            score += 20
        else:
            score += 10
        
        # Score basé sur la structure
        score += 20
        
        # Détermination de la note
        if score >= 90:
            return QualityLevel.EXCELLENT
        elif score >= 80:
            return QualityLevel.GOOD
        elif score >= 70:
            return QualityLevel.AVERAGE
        elif score >= 60:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL
    
    async def enhance_with_ai(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Améliore la documentation avec l'intelligence artificielle.
        
        Cette méthode utilise l'IA pour générer des suggestions d'amélioration
        et enrichir la documentation existante avec des exemples et des
        explications plus détaillées.
        
        Args:
            file_path: Chemin vers le fichier à améliorer
            
        Returns:
            Dict[str, Any]: Suggestions et améliorations générées par l'IA
            
        Example:
            >>> analyzer = DocumentationAnalyzer()
            >>> suggestions = await analyzer.enhance_with_ai("mon_fichier.py")
            >>> print(suggestions['improvements'])
        """
        if not self.config.get("ai_enhancement"):
            logger.warning("L'amélioration IA n'est pas activée")
            return {"error": "AI enhancement not enabled"}
        
        # Simulation d'amélioration IA
        await asyncio.sleep(0.1)  # Simulation d'appel API
        
        return {
            "improvements": [
                "Ajouter des exemples d'utilisation",
                "Améliorer la documentation des paramètres",
                "Inclure des cas d'erreur",
                "Ajouter des tests unitaires"
            ],
            "enhanced_doc": "Documentation enrichie par IA...",
            "examples": "Exemples générés automatiquement...",
            "best_practices": "Suggestions de bonnes pratiques..."
        }
    
    def generate_report(self, file_path: Union[str, Path], format: str = "markdown") -> str:
        """
        Génère un rapport détaillé d'analyse.
        
        Args:
            file_path: Chemin vers le fichier analysé
            format: Format du rapport ("markdown", "html", "json")
            
        Returns:
            str: Rapport généré dans le format spécifié
        """
        metrics = self.analyze_file(file_path)
        
        if format == "json":
            return json.dumps({
                "file_path": str(file_path),
                "metrics": {
                    "complexity": metrics.complexity,
                    "lines_of_code": metrics.lines_of_code,
                    "documentation_coverage": metrics.documentation_coverage,
                    "quality_grade": metrics.quality_grade.value
                },
                "recommendations": self._generate_recommendations(metrics)
            }, indent=2)
        
        elif format == "html":
            return self._generate_html_report(file_path, metrics)
        
        else:  # markdown
            return self._generate_markdown_report(file_path, metrics)
    
    def _generate_recommendations(self, metrics: CodeMetrics) -> List[str]:
        """Génère des recommandations basées sur les métriques."""
        recommendations = []
        
        if metrics.complexity > self.config.get("max_complexity", 10):
            recommendations.append("Réduire la complexité cyclomatique")
        
        if metrics.documentation_coverage < self.config.get("min_coverage", 80):
            recommendations.append("Améliorer la couverture de documentation")
        
        if metrics.quality_grade in [QualityLevel.POOR, QualityLevel.CRITICAL]:
            recommendations.append("Refactoriser le code pour améliorer la qualité")
        
        return recommendations
    
    def _generate_markdown_report(self, file_path: Union[str, Path], metrics: CodeMetrics) -> str:
        """Génère un rapport au format Markdown."""
        return f"""# Rapport d'Analyse - {Path(file_path).name}

## 📊 Métriques de Qualité

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Complexité** | {metrics.complexity:.2f} | {'🟢' if metrics.complexity <= 5 else '🟡' if metrics.complexity <= 10 else '🔴'} |
| **Lignes de code** | {metrics.lines_of_code} | 📊 |
| **Couverture doc** | {metrics.documentation_coverage:.1f}% | {'🟢' if metrics.documentation_coverage >= 90 else '🟡' if metrics.documentation_coverage >= 70 else '🔴'} |
| **Note globale** | {metrics.quality_grade.value} | {'🟢' if metrics.quality_grade in [QualityLevel.EXCELLENT, QualityLevel.GOOD] else '🟡' if metrics.quality_grade == QualityLevel.AVERAGE else '🔴'} |

## 💡 Recommandations

{chr(10).join(f"- {rec}" for rec in self._generate_recommendations(metrics))}

---
*Rapport généré automatiquement par docGen AI*
"""
    
    def _generate_html_report(self, file_path: Union[str, Path], metrics: CodeMetrics) -> str:
        """Génère un rapport au format HTML."""
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Rapport d'Analyse - {Path(file_path).name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .metric {{ margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }}
        .good {{ border-left: 4px solid #27ae60; }}
        .warning {{ border-left: 4px solid #f39c12; }}
        .critical {{ border-left: 4px solid #e74c3c; }}
    </style>
</head>
<body>
    <h1>Rapport d'Analyse - {Path(file_path).name}</h1>
    
    <div class="metric {'good' if metrics.quality_grade in [QualityLevel.EXCELLENT, QualityLevel.GOOD] else 'warning' if metrics.quality_grade == QualityLevel.AVERAGE else 'critical'}">
        <h3>Note de Qualité: {metrics.quality_grade.value}</h3>
        <p>Complexité: {metrics.complexity:.2f}</p>
        <p>Couverture: {metrics.documentation_coverage:.1f}%</p>
        <p>Lignes: {metrics.lines_of_code}</p>
    </div>
    
    <h3>Recommandations:</h3>
    <ul>
        {chr(10).join(f"<li>{rec}</li>" for rec in self._generate_recommendations(metrics))}
    </ul>
</body>
</html>"""

async def main():
    """Fonction principale de démonstration."""
    print("🚀 Démonstration de docGen AI")
    print("=" * 50)
    
    # Création de l'analyseur
    config = {
        "max_complexity": 8,
        "min_coverage": 85.0,
        "enable_cache": True,
        "ai_enhancement": True
    }
    
    analyzer = DocumentationAnalyzer(config)
    
    # Analyse du fichier courant
    current_file = Path(__file__)
    print(f"📖 Analyse du fichier: {current_file.name}")
    
    try:
        # Analyse basique
        metrics = analyzer.analyze_file(current_file)
        print(f"✅ Analyse terminée!")
        print(f"   Complexité: {metrics.complexity:.2f}")
        print(f"   Couverture: {metrics.documentation_coverage:.1f}%")
        print(f"   Note: {metrics.quality_grade.value}")
        
        # Génération de rapports
        print("\n📊 Génération de rapports...")
        
        # Rapport Markdown
        markdown_report = analyzer.generate_report(current_file, "markdown")
        with open("demo_report.md", "w", encoding="utf-8") as f:
            f.write(markdown_report)
        print("   ✅ Rapport Markdown généré: demo_report.md")
        
        # Rapport HTML
        html_report = analyzer.generate_report(current_file, "html")
        with open("demo_report.html", "w", encoding="utf-8") as f:
            f.write(html_report)
        print("   ✅ Rapport HTML généré: demo_report.html")
        
        # Rapport JSON
        json_report = analyzer.generate_report(current_file, "json")
        with open("demo_report.json", "w", encoding="utf-8") as f:
            f.write(json_report)
        print("   ✅ Rapport JSON généré: demo_report.json")
        
        # Amélioration IA
        print("\n🤖 Amélioration avec IA...")
        ai_suggestions = await analyzer.enhance_with_ai(current_file)
        print(f"   ✅ Suggestions IA générées: {len(ai_suggestions.get('improvements', []))} améliorations")
        
        print("\n🎉 Démonstration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        logger.exception("Erreur détaillée:")

if __name__ == "__main__":
    asyncio.run(main())
