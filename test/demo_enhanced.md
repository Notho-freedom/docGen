# 📚 Documentation - demo.py

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Documentation](https://img.shields.io/badge/Documentation-Générée%20automatiquement-green.svg)
![IA](https://img.shields.io/badge/IA-Groq%20Powered-orange.svg)

**Généré le 21/07/2025 à 01:46**  
**Fichier source :** `examples\demo.py`

</div>

---



## 📋 Table des matières

- [📖 Documentation du module](#-documentation-du-module)
- [📦 Analyse des imports](#-analyse-des-imports)
- [🔧 Fonctions](#-fonctions)
- [🧱 Classes](#-classes)
- [📈 Statistiques détaillées](#-statistiques-détaillées)

## 📖 Documentation du module

### Documentation originale
```
Module de démonstration pour docGen AI.

Ce module illustre les capacités avancées du générateur de documentation
intelligent avec des exemples concrets de fonctions et classes bien documentées.
```


## 📦 Analyse des imports

**Total des imports :** 13

### 🐍 Modules de la bibliothèque standard
```python
import asyncio
import enum.Enum
import functools.wraps
import json
import logging
import pathlib.Path
import typing.Any
import typing.Dict
import typing.List
import typing.Optional
import typing.Union
```

### 📚 Modules tiers
```python
import dataclasses.dataclass
import time
```


## 🔧 Fonctions (14)

### 1. `performance_monitor`

**Complexité :** 🟢 1 | 
**Lignes :** 46-70 | 
**Code :** 21 lignes


```python
def performance_monitor(func):
```

#### 📝 Documentation originale
```
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
```

### 2. `__post_init__`

**Complexité :** 🟡 4 | 
**Lignes :** 39-44 | 
**Code :** 6 lignes


```python
def __post_init__(self):
```

#### 📝 Documentation originale
```
Validation des métriques après initialisation.
```

### 3. `wrapper`

**Complexité :** 🟢 1 | 
**Lignes :** 63-69 | 
**Code :** 6 lignes


```python
def wrapper():
```

#### 🎨 Décorateurs
- `wraps(func)`

### 4. `__init__`

**Complexité :** 🟢 2 | 
**Lignes :** 90-102 | 
**Code :** 11 lignes


```python
def __init__(self, config=None):
```

#### 📝 Documentation originale
```
Initialise l'analyseur de documentation.

Args:
    config: Configuration optionnelle pour l'analyseur
    
Raises:
    ValueError: Si la configuration est invalide
```

### 5. `_validate_config`

**Complexité :** 🟢 3 | 
**Lignes :** 104-109 | 
**Code :** 6 lignes


```python
def _validate_config(self) -> None:
```

#### 📝 Documentation originale
```
Valide la configuration de l'analyseur.
```

### 6. `_get_default_config`

**Complexité :** 🟢 1 | 
**Lignes :** 111-118 | 
**Code :** 8 lignes


```python
def _get_default_config(self) -> Dict[str, Any]:
```

#### 📝 Documentation originale
```
Retourne la configuration par défaut.
```

### 7. `analyze_file`

**Complexité :** 🟡 6 | 
**Lignes :** 121-177 | 
**Code :** 41 lignes


```python
def analyze_file(self, file_path) -> CodeMetrics:
```

#### 📝 Documentation originale
```
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
```

#### 🎨 Décorateurs
- `performance_monitor`

### 8. `_calculate_complexity`

**Complexité :** 🟢 2 | 
**Lignes :** 179-197 | 
**Code :** 14 lignes


```python
def _calculate_complexity(self, content) -> float:
```

#### 📝 Documentation originale
```
Calcule la complexité cyclomatique du code.

Args:
    content: Contenu du fichier Python
    
Returns:
    float: Complexité cyclomatique moyenne
```

### 9. `_calculate_documentation_coverage`

**Complexité :** 🟠 8 | 
**Lignes :** 199-226 | 
**Code :** 23 lignes


```python
def _calculate_documentation_coverage(self, content) -> float:
```

#### 📝 Documentation originale
```
Calcule la couverture de documentation.

Args:
    content: Contenu du fichier Python
    
Returns:
    float: Pourcentage de couverture (0-100)
```

### 10. `_determine_quality_grade`

**Complexité :** 🔴 11 | 
**Lignes :** 228-274 | 
**Code :** 37 lignes


```python
def _determine_quality_grade(self, complexity, coverage) -> QualityLevel:
```

#### 📝 Documentation originale
```
Détermine la note de qualité basée sur les métriques.

Args:
    complexity: Complexité cyclomatique
    coverage: Couverture de documentation
    
Returns:
    QualityLevel: Note de qualité déterminée
```

### 11. `generate_report`

**Complexité :** 🟢 3 | 
**Lignes :** 314-343 | 
**Code :** 25 lignes


```python
def generate_report(self, file_path, format='markdown') -> str:
```

#### 📝 Documentation originale
```
Génère un rapport détaillé d'analyse.

Args:
    file_path: Chemin vers le fichier analysé
    format: Format du rapport ("markdown", "html", "json")
    
Returns:
    str: Rapport généré dans le format spécifié
```

### 12. `_generate_recommendations`

**Complexité :** 🟡 4 | 
**Lignes :** 345-358 | 
**Code :** 10 lignes


```python
def _generate_recommendations(self, metrics) -> List[str]:
```

#### 📝 Documentation originale
```
Génère des recommandations basées sur les métriques.
```

### 13. `_generate_markdown_report`

**Complexité :** 🟢 1 | 
**Lignes :** 360-379 | 
**Code :** 13 lignes


```python
def _generate_markdown_report(self, file_path, metrics) -> str:
```

#### 📝 Documentation originale
```
Génère un rapport au format Markdown.
```

### 14. `_generate_html_report`

**Complexité :** 🟢 1 | 
**Lignes :** 381-410 | 
**Code :** 28 lignes


```python
def _generate_html_report(self, file_path, metrics) -> str:
```

#### 📝 Documentation originale
```
Génère un rapport au format HTML.
```


## 🧱 Classes (3)

### 1. `QualityLevel`

**Lignes :** 23-29 | 
**Méthodes :** 0 | 
**Variables :** 5


#### 🏗️ Héritage
```python
class QualityLevel(Enum):
```

#### 📝 Documentation originale
```
Niveaux de qualité pour l'évaluation du code.
```

#### 📊 Variables de classe
- `EXCELLENT` = `'A'`
- `GOOD` = `'B'`
- `AVERAGE` = `'C'`
- `POOR` = `'D'`
- `CRITICAL` = `'E'`

### 2. `CodeMetrics`

**Lignes :** 32-44 | 
**Méthodes :** 1 | 
**Variables :** 0


#### 📝 Documentation originale
```
Métriques de qualité du code.
```

#### 🔧 Méthodes
- `__post_init__(self)`

### 3. `DocumentationAnalyzer`

**Lignes :** 72-410 | 
**Méthodes :** 11 | 
**Variables :** 0


#### 📝 Documentation originale
```
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
```

#### 🔧 Méthodes
- `__init__(self, config)`
- `_validate_config(self)`
- `_get_default_config(self)`
- `analyze_file(self, file_path)`
- `_calculate_complexity(self, content)`
- `_calculate_documentation_coverage(self, content)`
- `_determine_quality_grade(self, complexity, coverage)`
- `generate_report(self, file_path, format)`
- `_generate_recommendations(self, metrics)`
- `_generate_markdown_report(self, file_path, metrics)`
- `_generate_html_report(self, file_path, metrics)`


## 📈 Statistiques détaillées

### 🔧 Statistiques des fonctions
- **Total :** 14
- **Documentées :** 13 (92.9%)
- **Arguments moyens :** 1.9
- **Complexité moyenne :** 3.4

### 🧱 Statistiques des classes
- **Total :** 3
- **Documentées :** 3 (100.0%)
- **Méthodes totales :** 12
- **Variables de classe :** 5

### 📄 Statistiques du fichier
- **Lignes totales :** 473
- **Lignes de code :** 0
- **Lignes de commentaires :** 0



---

<div align="center">

**📚 Documentation générée automatiquement avec [docGen](https://github.com/votre-repo/docGen)**

*Propulsé par Groq AI 🤖*

---

</div>
