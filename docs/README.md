# 📚 Documentation docGen AI

## 🎯 Vue d'ensemble

**docGen AI** est un générateur de documentation Python intelligent qui utilise l'IA Groq pour créer une documentation riche et détaillée.

## 🚀 Fonctionnalités Principales

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

## 🛠️ Architecture

### Composants Principaux

#### 📦 Package `docgen`
- `docgen.py` : Moteur principal d'extraction et d'enrichissement
- `formatter.py` : Générateur de formats de sortie
- `cli.py` : Interface en ligne de commande
- `config.py` : Configuration et gestion des paramètres

#### 🔌 Providers
- `groq_client.py` : Client pour l'API Groq
- `memory.py` : Gestion de la mémoire des conversations

### Flux de Traitement

1. **Analyse du fichier** → Extraction AST
2. **Calcul des métriques** → Complexité, statistiques
3. **Enrichissement IA** → Amélioration du contenu (optionnel)
4. **Formatage** → Génération du format de sortie
5. **Sauvegarde** → Écriture du fichier final

## 📊 Métriques de Qualité

### Complexité Cyclomatique
- 🟢 **1-5** : Simple
- 🟡 **6-10** : Modérée
- 🔴 **11+** : Complexe

### Couverture de Documentation
- **Fonctions documentées** : Pourcentage des fonctions avec docstrings
- **Classes documentées** : Pourcentage des classes avec docstrings
- **Moyenne des docstrings** : Longueur moyenne des descriptions

### Analyse des Imports
- **Bibliothèques standard** : Modules Python intégrés
- **Bibliothèques tierces** : Packages externes
- **Imports relatifs** : Imports internes au projet

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

# Analyse qualité
MAX_COMPLEXITY=10
MIN_DOC_COVERAGE=80.0
ENABLE_CACHE=true
```

### Configuration Python
```python
from docgen.config import config

# Modification des paramètres
config.groq_models = ["llama3-70b-8192", "mixtral-8x7b-32768"]
config.groq_temperature = 0.5
config.groq_max_tokens = 2000
```

## 🎯 Cas d'Usage

### Développement Local
```bash
# Documentation basique
docgen mon_fichier.py

# Documentation enrichie
docgen mon_fichier.py --enhanced

# Format HTML
docgen mon_fichier.py --format html
```

### Intégration CI/CD
```yaml
# GitHub Actions
- name: Generate Documentation
  run: |
    pip install docgen-ai
    docgen src/ --enhanced -o docs/
    git add docs/
    git commit -m "Update documentation"
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
```

## 🧪 Tests et Validation

### Tests Unitaires
```bash
# Tests complets
python -m pytest tests/ -v

# Tests avec couverture
python -m pytest tests/ --cov=docgen --cov-report=html

# Validation complète
python validate_installation.py
```

### Tests d'Intégration
- **Extraction basique** : Vérification de l'analyse AST
- **Enrichissement IA** : Test des appels API Groq
- **Formatage** : Validation des formats de sortie
- **CLI** : Test de l'interface utilisateur

## 🚀 Performance

### Métriques de Performance
- **Temps d'analyse** : < 1 seconde pour un fichier de 500 lignes
- **Mémoire** : < 50MB pour l'analyse d'un projet moyen
- **API Groq** : Gestion d'erreurs et retry automatique
- **Cache** : Optimisation des appels répétés

### Optimisations
- **Analyse AST optimisée** : Parsing efficace
- **Appels API asynchrones** : Non-bloquant
- **Cache intelligent** : Évite les appels redondants
- **Gestion d'erreurs** : Fallback robuste

## 🔮 Évolutions Futures

### Fonctionnalités Planifiées
- [ ] **Support Jupyter Notebooks** : Analyse des .ipynb
- [ ] **Génération UML** : Diagrammes automatiques
- [ ] **Interface web** : Dashboard interactif
- [ ] **Multi-langues** : Support international
- [ ] **Intégration IDE** : Plugins pour VS Code, PyCharm

### Améliorations Techniques
- [ ] **Cache distribué** : Redis/Memcached
- [ ] **Templates avancés** : Personnalisation complète
- [ ] **Métriques avancées** : Analyse de qualité approfondie
- [ ] **API REST** : Service web

## 🤝 Contribution

### Développement
1. **Fork** le projet
2. **Clone** votre fork
3. **Installation** : `pip install -e ".[dev]"`
4. **Tests** : `python -m pytest tests/ -v`
5. **Commit** avec des messages clairs
6. **Pull Request** avec description détaillée

### Standards de Code
- **Black** : Formatage automatique
- **Flake8** : Linting
- **MyPy** : Vérification des types
- **Pytest** : Tests unitaires
- **Coverage** : Couverture de code

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

### Documentation
- **Guide d'installation** : `INSTALLATION_GUIDE.md`
- **Structure du projet** : `STRUCTURE.md`
- **Exemples** : Dossier `examples/`

### Issues
- **Bugs** : Créer une issue avec reproduction
- **Feature requests** : Décrire le cas d'usage
- **Questions** : Utiliser les discussions GitHub

---

<div align="center">

**🎉 docGen AI - Documentation intelligente pour Python**

*Propulsé par Groq AI 🤖 | Développé par Genesis Company*

</div> 