# 🚀 docGen AI - Générateur de Documentation Python Intelligent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://pypi.org/project/docgen-ai/)
[![AI Powered](https://img.shields.io/badge/AI-Groq%20Powered-purple.svg)](https://groq.com/)

**docGen AI** est un générateur de documentation Python révolutionnaire qui utilise l'intelligence artificielle (Groq) pour créer une documentation riche, intelligente et professionnelle automatiquement.

## ✨ Fonctionnalités Principales

### 🤖 Enrichissement par IA
- **Documentation intelligente** : Génération automatique de descriptions détaillées
- **Exemples d'utilisation** : Création d'exemples concrets et pratiques
- **Conseils d'usage** : Suggestions de bonnes pratiques et pièges à éviter
- **Analyse de qualité** : Évaluation automatique de la qualité du code
- **Suggestions d'amélioration** : Recommandations pour optimiser le code

### 📊 Analyse Avancée
- **Complexité cyclomatique** : Calcul automatique de la complexité des fonctions
- **Couverture de documentation** : Statistiques détaillées sur la documentation
- **Analyse des imports** : Catégorisation des dépendances
- **Patterns de conception** : Identification automatique des patterns utilisés
- **Métriques de qualité** : Notes et recommandations personnalisées

### 🎨 Formats de Sortie Multiples
- **Markdown enrichi** : Documentation moderne avec emojis et badges
- **HTML interactif** : Interface web élégante et responsive
- **JSON structuré** : Données brutes pour intégration avec d'autres outils
- **Rapports détaillés** : Statistiques et analyses complètes

## 🚀 Installation

### Installation via pip
```bash
pip install docgen-ai
```

### Installation depuis les sources
```bash
git clone https://github.com/votre-repo/docGen.git
cd docGen
pip install -e .
```

### Configuration de l'API Groq
1. Créez un compte sur [Groq](https://groq.com/)
2. Obtenez votre clé API
3. Créez un fichier `.env` à la racine du projet :
```env
GROQ_API_KEY=votre_clé_api_groq
```

## 📖 Utilisation

### Utilisation Basique
```bash
# Documentation basique (sans IA)
docgen mon_fichier.py

# Documentation enrichie par IA
docgen mon_fichier.py --enhanced

# Spécifier le fichier de sortie
docgen mon_fichier.py -o documentation.md
```

### Formats de Sortie
```bash
# Markdown (par défaut)
docgen mon_fichier.py --format markdown

# HTML interactif
docgen mon_fichier.py --format html

# JSON structuré
docgen mon_fichier.py --format json
```

### Options Avancées
```bash
# Mode verbeux avec plus de détails
docgen mon_fichier.py --verbose

# Désactiver l'IA même si --enhanced est spécifié
docgen mon_fichier.py --enhanced --no-ai

# Afficher l'aide complète
docgen --help
```

## 📊 Exemple de Sortie

### Résumé Exécutif
```
🎯 Résumé exécutif

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Note de qualité** | 🟢 A | Excellent |
| **Couverture doc** | 85.7% | 🟡 Bon |
| **Complexité moy.** | 3.2 | 🟢 Faible |
| **Fonctions** | 7 | 📊 |
| **Classes** | 2 | 📊 |
```

### Documentation Enrichie
```markdown
## 🔧 Fonctions (7)

### 1. `extract_doc_info`

**Complexité :** 🟢 2 | **Lignes :** 15-45 | **Code :** 25 lignes

```python
def extract_doc_info(file_path: str) -> Dict[str, Any]:
```

#### 📝 Documentation originale
```
Extrait les informations de documentation d'un fichier Python.
```

#### 🤖 Documentation enrichie par IA
Cette fonction analyse un fichier Python et extrait automatiquement toutes les informations de documentation disponibles. Elle utilise l'analyse syntaxique (AST) pour identifier les fonctions, classes, docstrings et métadonnées importantes.

**Cas d'usage typiques :**
- Génération automatique de documentation
- Analyse de la qualité du code
- Audit de la couverture de documentation

#### 💡 Exemples d'utilisation
```python
# Analyse d'un fichier simple
doc_info = extract_doc_info("mon_module.py")

# Accès aux informations extraites
print(f"Fonctions trouvées : {len(doc_info['functions'])}")
print(f"Classes trouvées : {len(doc_info['classes'])}")
```

#### 💭 Conseils d'utilisation
- Utilisez cette fonction pour automatiser la génération de documentation
- Idéal pour les projets avec de nombreux fichiers Python
- Combine bien avec les outils de CI/CD pour maintenir la documentation à jour
```

## 🏗️ Architecture

### Structure du Projet
```
docGen/
├── docgen.py          # Moteur principal d'extraction et d'enrichissement
├── formatter.py       # Générateur de formats de sortie
├── cli.py            # Interface en ligne de commande
├── config.py         # Configuration et gestion des paramètres
├── providers/
│   ├── groq_client.py # Client Groq pour l'IA
│   └── memory.py     # Gestion de la mémoire des conversations
├── templates/        # Templates pour les formats de sortie
└── examples/         # Exemples d'utilisation
```

### Composants Principaux

#### `DocGenerator`
- **Extraction** : Analyse AST des fichiers Python
- **Enrichissement** : Utilisation de Groq pour améliorer la documentation
- **Analyse** : Calcul de métriques de qualité

#### `DocumentationFormatter`
- **Markdown** : Génération de documentation riche
- **HTML** : Interface web interactive
- **JSON** : Données structurées

#### `GroqClient`
- **IA** : Intégration avec l'API Groq
- **Mémoire** : Gestion du contexte des conversations
- **Optimisation** : Paramètres adaptatifs

## 🔧 Configuration Avancée

### Variables d'Environnement
```env
# Obligatoire pour l'IA
GROQ_API_KEY=votre_clé_api_groq

# Optionnel - Paramètres Groq
GROQ_MODEL=llama3-70b-8192
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=1000
```

### Configuration Personnalisée
```python
from config import Config

# Personnaliser les paramètres
config = Config(
    groq_temperature=0.5,
    groq_max_tokens=2000,
    groq_models=["llama3-70b-8192", "mixtral-8x7b-32768"]
)
```

## 🧪 Tests

### Exécution des Tests
```bash
# Installation des dépendances de développement
pip install -e ".[dev]"

# Exécution des tests
pytest

# Tests avec couverture
pytest --cov=docgen

# Tests asynchrones
pytest --asyncio-mode=auto
```

### Exemples d'Utilisation
```python
import asyncio
from docgen import DocGenerator

# Création d'un générateur
generator = DocGenerator()

# Extraction basique
doc_info = generator.extract_doc_info("mon_fichier.py")

# Enrichissement avec IA
enhanced_doc = await generator.enrich_documentation(doc_info)
```

## 📈 Métriques et Qualité

### Indicateurs de Qualité
- **Note globale** : A (Excellent) à E (Critique)
- **Couverture de documentation** : Pourcentage de fonctions/classes documentées
- **Complexité moyenne** : Complexité cyclomatique moyenne
- **Fonctions complexes** : Nombre de fonctions nécessitant une refactorisation

### Recommandations Automatiques
- Documentation manquante
- Fonctions trop complexes
- Bonnes pratiques
- Optimisations possibles

## 🤝 Contribution

### Comment Contribuer
1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité
3. **Commitez** vos changements
4. **Poussez** vers la branche
5. **Ouvrez** une Pull Request

### Standards de Code
```bash
# Formatage automatique
black .

# Vérification du style
flake8 .

# Vérification des types
mypy .
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Groq** pour l'API d'intelligence artificielle
- **Python AST** pour l'analyse syntaxique
- **Pydantic** pour la validation des données
- **La communauté Python** pour les outils et bibliothèques

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/votre-repo/docGen/issues)
- **Documentation** : [Wiki](https://github.com/votre-repo/docGen/wiki)
- **Discussions** : [GitHub Discussions](https://github.com/votre-repo/docGen/discussions)

---

<div align="center">

**Propulsé par Groq AI 🤖**

*Fait avec ❤️ pour la communauté Python*

</div> 