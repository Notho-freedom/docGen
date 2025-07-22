# 🚀 docGen AI - Générateur de Documentation Python Intelligent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Documentation](https://img.shields.io/badge/Documentation-Générée%20automatiquement-green.svg)
![IA](https://img.shields.io/badge/IA-Groq%20Powered-orange.svg)
![Version](https://img.shields.io/badge/Version-2.0.0-purple.svg)

**Générateur de documentation Python intelligent avec enrichissement IA**

*Propulsé par Groq AI 🤖 | Développé par Genesis Company*

</div>

---

## 📋 Vue d'ensemble

**docGen AI** est un générateur de documentation Python avancé qui utilise l'IA Groq pour créer une documentation riche et détaillée. Il analyse automatiquement votre code Python et génère une documentation structurée avec métriques de qualité, suggestions d'amélioration et exemples d'utilisation.

## 🏗️ Structure du Projet

```
docGen/
├── 📦 docgen/                    # Package principal
│   ├── __init__.py              # Point d'entrée
│   ├── docgen.py                # Moteur d'extraction et enrichissement
│   ├── formatter.py             # Générateur de formats (MD/HTML/JSON)
│   ├── cli.py                   # Interface ligne de commande
│   ├── config.py                # Configuration Pydantic
│   └── providers/               # Services externes
│       ├── __init__.py          # Exports des providers
│       ├── groq_client.py       # Client Groq AI
│       └── memory.py            # Gestion mémoire conversations
├── 🧪 tests/                    # Tests unitaires
│   ├── __init__.py
│   └── test_docgen.py           # Tests complets
├── 📚 docs/                     # Documentation complète
│   ├── README.md                # Documentation principale
│   ├── API.md                   # Guide d'API
│   ├── CONTRIBUTING.md          # Guide de contribution
│   ├── CHANGELOG.md             # Historique des versions
│   ├── STRUCTURE.md             # Structure détaillée
│   └── INSTALLATION_GUIDE.md    # Guide d'installation
├── 📝 examples/                 # Exemples d'utilisation
│   └── demo.py                  # Fichier de démonstration
├── 🎨 templates/                # Templates de sortie
│   ├── markdown.j2              # Template Markdown Jinja2
│   └── html.j2                  # Template HTML avec CSS
├── 🔧 Tools/                    # Outils de développement
│   ├── validate_installation.py # Script de validation
│   └── generate_report.py       # Générateur de rapports
├── ⚙️ Config/                   # Configuration
│   ├── setup.py                 # Configuration setuptools
│   ├── pyproject.toml           # Configuration moderne PEP 621
│   ├── MANIFEST.in              # Fichiers à inclure
│   ├── requirements.txt         # Dépendances principales
│   ├── requirements-dev.txt     # Dépendances développement
│   └── env.example              # Variables d'environnement
├── 📦 Build/                    # Distribution
│   ├── dist/                    # Packages buildés
│   └── docgen_ai.egg-info/      # Métadonnées
├── 📊 Log/                      # Rapports générés
│   └── *.md, *.json             # Rapports de documentation
└── 📖 README.md                 # Ce fichier
```

## 🚀 Installation Rapide

### Prérequis
- **Python 3.8+**
- **Clé API Groq** (optionnelle, pour l'enrichissement IA)

### Installation
```bash
# 1. Cloner le projet
git clone https://github.com/Notho-freedom/docGen.git
cd docGen

# 2. Installation en mode développement
pip install -e Config/

# 3. Configuration (optionnelle)
cp Config/env.example .env
# Éditer .env avec votre clé API Groq

# 4. Validation
python Tools/validate_installation.py
```

## 🎯 Utilisation

### Interface CLI
```bash
# Documentation basique
docgen examples/demo.py

# Documentation enrichie par IA
docgen examples/demo.py --enhanced

# Format HTML
docgen examples/demo.py --format html

# Sortie personnalisée
docgen examples/demo.py -o ma_documentation.md --verbose
```

### Utilisation Programmatique
```python
import asyncio
from docgen import DocGenerator, DocumentationFormatter

# Extraction basique
generator = DocGenerator()
doc_info = generator.extract_doc_info("mon_fichier.py")

# Extraction enrichie
doc_info = await generator.extract_doc_info_enhanced("mon_fichier.py")

# Formatage
formatter = DocumentationFormatter()
markdown = formatter.format_markdown(doc_info)
html = formatter.format_html(doc_info)
json_output = formatter.format_json(doc_info)
```

## 🔧 Outils de Développement

### Validation de l'Installation
```bash
python Tools/validate_installation.py
```

### Génération de Rapports
```bash
python Tools/generate_report.py
```
*Les rapports sont automatiquement sauvegardés dans le dossier `Log/`*

### Tests
```bash
# Tests complets
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest tests/ --cov=docgen --cov-report=html
```

## 📊 Fonctionnalités

### 🔍 Extraction Intelligente
- **Analyse AST** : Extraction complète des fonctions, classes et docstrings
- **Calcul de complexité** : Métriques cyclomatiques automatiques
- **Analyse des imports** : Distinction entre bibliothèques standard et tierces
- **Statistiques détaillées** : Métriques de qualité du code

### 🤖 Enrichissement IA
- **Intégration Groq** : API asynchrone avec retry automatique
- **Mémoire conversationnelle** : Contexte persistant pour l'IA
- **Fallback intelligent** : Fonctionnement sans IA si nécessaire
- **Enrichissement automatique** : Exemples, suggestions, patterns

### 📄 Formats de Sortie
- **Markdown riche** : Documentation structurée avec badges et emojis
- **HTML interactif** : Interface web stylée et responsive
- **JSON structuré** : Données pour intégration avec d'autres outils
- **Templates personnalisables** : Extensibilité complète

## 📚 Documentation

### Guides Disponibles
- **[Guide d'Installation](docs/INSTALLATION_GUIDE.md)** : Instructions détaillées
- **[Guide d'API](docs/API.md)** : Utilisation programmatique
- **[Guide de Contribution](docs/CONTRIBUTING.md)** : Standards de développement
- **[Changelog](docs/CHANGELOG.md)** : Historique des versions
- **[Structure](docs/STRUCTURE.md)** : Organisation détaillée du projet

### Exemples
- **[Demo](examples/demo.py)** : Fichier de démonstration complet
- **[Templates](templates/)** : Templates Markdown et HTML personnalisables

## 🔧 Configuration

### Variables d'Environnement
```env
# API Groq (obligatoire pour l'IA)
GROQ_API_KEY=votre_clé_api_groq
GROQ_MODEL=llama3-70b-8192
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=1000

# Configuration documentation
DOC_LANGUAGE=fr
DEFAULT_FORMAT=markdown
ENABLE_AI_ENHANCEMENT=true
```

### Configuration Python
```python
from docgen.config import config

# Modification des paramètres
config.groq_models = ["llama3-70b-8192", "mixtral-8x7b-32768"]
config.groq_temperature = 0.5
config.groq_max_tokens = 2000
```

## 🧪 Tests et Validation

### Validation Automatique
```bash
python Tools/validate_installation.py
```

**Tests inclus :**
- ✅ Structure du projet
- ✅ Imports des modules
- ✅ Configuration
- ✅ Extraction basique
- ✅ Formateur
- ✅ Interface CLI
- ✅ Extraction enrichie

### Tests Unitaires
```bash
python -m pytest tests/ -v
```

## 📊 Métriques de Qualité

### Complexité Cyclomatique
- 🟢 **1-5** : Simple
- 🟡 **6-10** : Modérée
- 🔴 **11+** : Complexe

### Couverture de Documentation
- **Fonctions documentées** : Pourcentage des fonctions avec docstrings
- **Classes documentées** : Pourcentage des classes avec docstrings
- **Moyenne des docstrings** : Longueur moyenne des descriptions

## 🚀 Performance

### Métriques
- **Temps d'analyse** : < 1 seconde pour un fichier de 500 lignes
- **Mémoire** : < 50MB pour l'analyse d'un projet moyen
- **API Groq** : Gestion d'erreurs et retry automatique
- **Cache** : Optimisation des appels répétés

## 🤝 Contribution

### Développement
1. **Fork** le projet
2. **Clone** votre fork
3. **Installation** : `pip install -e Config/`
4. **Tests** : `python Tools/validate_installation.py`
5. **Commit** avec des messages clairs
6. **Pull Request** avec description détaillée

### Standards
- **Black** : Formatage automatique
- **Flake8** : Linting
- **MyPy** : Vérification des types
- **Pytest** : Tests unitaires
- **Coverage** : Couverture de code

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

### Documentation
- **Guide d'installation** : `docs/INSTALLATION_GUIDE.md`
- **Structure du projet** : `docs/STRUCTURE.md`
- **Exemples** : Dossier `examples/`

### Issues
- **Bugs** : Créer une issue avec reproduction
- **Feature requests** : Décrire le cas d'usage
- **Questions** : Utiliser les discussions GitHub

### Contact
- **Email** : contact@genesis-company.net
- **GitHub** : Issues et discussions

---

<div align="center">

**🎉 docGen AI - Documentation intelligente pour Python**

*Propulsé par Groq AI 🤖 | Développé par Genesis Company*

[![GitHub stars](https://img.shields.io/github/stars/Notho-freedom/docGen?style=social)](https://github.com/Notho-freedom/docGen)
[![GitHub forks](https://img.shields.io/github/forks/Notho-freedom/docGen?style=social)](https://github.com/Notho-freedom/docGen)

</div> 