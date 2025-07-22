import os
from datetime import datetime
from typing import Dict, Any, List
import json

class DocumentationFormatter:
    def __init__(self):
        self.template_dir = "templates"
        self.ensure_template_dir()
        
    def ensure_template_dir(self):
        """Assure que le répertoire des templates existe."""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
            
    def format_markdown(self, doc_info: Dict[str, Any]) -> str:
        """Formate la documentation en Markdown enrichi."""
        md = []
        
        # En-tête avec métadonnées
        md.append(self._generate_header(doc_info))
        
        # Table des matières
        md.append(self._generate_toc(doc_info))
        
        # Résumé exécutif
        if "quality_analysis" in doc_info:
            md.append(self._generate_executive_summary(doc_info))
        
        # Documentation du module
        if doc_info.get("module_doc") or doc_info.get("enhanced_module_doc"):
            md.append(self._generate_module_documentation(doc_info))
        
        # Analyse des imports
        if doc_info.get("imports"):
            md.append(self._generate_imports_analysis(doc_info))
        
        # Fonctions
        if doc_info.get("functions"):
            md.append(self._generate_functions_documentation(doc_info))
        
        # Classes
        if doc_info.get("classes"):
            md.append(self._generate_classes_documentation(doc_info))
        
        # Analyse de qualité
        if "quality_analysis" in doc_info:
            md.append(self._generate_quality_analysis(doc_info))
        
        # Suggestions d'amélioration
        if "suggestions" in doc_info:
            md.append(self._generate_improvement_suggestions(doc_info))
        
        # Statistiques détaillées
        md.append(self._generate_detailed_statistics(doc_info))
        
        # Pied de page
        md.append(self._generate_footer(doc_info))
        
        return "\n\n".join(md)
    
    def format_html(self, doc_info: dict) -> str:
        """Formate la documentation en HTML (utilise le template de cli.py)."""
        from .cli import generate_html
        return generate_html(doc_info)

    def format_json(self, doc_info: dict, indent: int = 2) -> str:
        """Formate la documentation en JSON."""
        import json
        return json.dumps(doc_info, indent=indent, ensure_ascii=False)
    
    def _generate_header(self, doc_info: Dict[str, Any]) -> str:
        """Génère l'en-tête de la documentation."""
        file_name = os.path.basename(doc_info.get("file_path", "unknown"))
        current_time = datetime.now().strftime("%d/%m/%Y à %H:%M")
        
        return f"""# 📚 Documentation - {file_name}

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Documentation](https://img.shields.io/badge/Documentation-Générée%20automatiquement-green.svg)
![IA](https://img.shields.io/badge/IA-Groq%20Powered-orange.svg)

**Généré le {current_time}**  
**Fichier source :** `{doc_info.get("file_path", "unknown")}`

</div>

---

"""
    
    def _generate_toc(self, doc_info: Dict[str, Any]) -> str:
        """Génère la table des matières."""
        toc = ["## 📋 Table des matières\n"]
        
        if doc_info.get("module_doc") or doc_info.get("enhanced_module_doc"):
            toc.append("- [📖 Documentation du module](#-documentation-du-module)")
        
        if doc_info.get("imports"):
            toc.append("- [📦 Analyse des imports](#-analyse-des-imports)")
        
        if doc_info.get("functions"):
            toc.append("- [🔧 Fonctions](#-fonctions)")
        
        if doc_info.get("classes"):
            toc.append("- [🧱 Classes](#-classes)")
        
        if "quality_analysis" in doc_info:
            toc.append("- [📊 Analyse de qualité](#-analyse-de-qualité)")
        
        if "suggestions" in doc_info:
            toc.append("- [💡 Suggestions d'amélioration](#-suggestions-damélioration)")
        
        toc.append("- [📈 Statistiques détaillées](#-statistiques-détaillées)")
        
        return "\n".join(toc)
    
    def _generate_executive_summary(self, doc_info: Dict[str, Any]) -> str:
        """Génère un résumé exécutif."""
        quality = doc_info.get("quality_analysis", {})
        grade = quality.get("quality_grade", "N/A")
        coverage = quality.get("documentation_coverage", 0)
        complexity = quality.get("complexity_score", 0)
        
        grade_emoji = {
            "A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴", "E": "⚫"
        }.get(grade, "❓")
        
        return f"""## 🎯 Résumé exécutif

<div align="center">

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **Note de qualité** | {grade_emoji} {grade} | {self._get_quality_status(grade)} |
| **Couverture doc** | {coverage:.1f}% | {self._get_coverage_status(coverage)} |
| **Complexité moy.** | {complexity:.1f} | {self._get_complexity_status(complexity)} |
| **Fonctions** | {len(doc_info.get('functions', []))} | 📊 |
| **Classes** | {len(doc_info.get('classes', []))} | 📊 |

</div>

"""
    
    def _generate_module_documentation(self, doc_info: Dict[str, Any]) -> str:
        """Génère la documentation du module."""
        md = ["## 📖 Documentation du module\n"]
        
        # Documentation originale
        if doc_info.get("module_doc"):
            md.append("### Documentation originale")
            md.append(f"```\n{doc_info['module_doc']}\n```\n")
        
        # Documentation enrichie
        if doc_info.get("enhanced_module_doc"):
            md.append("### 📝 Documentation enrichie par IA")
            md.append(f"{doc_info['enhanced_module_doc']}\n")
        
        return "\n".join(md)
    
    def _generate_imports_analysis(self, doc_info: Dict[str, Any]) -> str:
        """Génère l'analyse des imports."""
        imports = doc_info.get("imports", [])
        
        # Catégoriser les imports
        stdlib_imports = []
        third_party_imports = []
        
        for imp in imports:
            if self._is_stdlib_import(imp):
                stdlib_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        md = ["## 📦 Analyse des imports\n"]
        md.append(f"**Total des imports :** {len(imports)}\n")
        
        if stdlib_imports:
            md.append("### 🐍 Modules de la bibliothèque standard")
            md.append("```python")
            for imp in sorted(set(stdlib_imports)):
                md.append(f"import {imp}")
            md.append("```\n")
        
        if third_party_imports:
            md.append("### 📚 Modules tiers")
            md.append("```python")
            for imp in sorted(set(third_party_imports)):
                md.append(f"import {imp}")
            md.append("```\n")
        
        return "\n".join(md)
    
    def _generate_functions_documentation(self, doc_info: Dict[str, Any]) -> str:
        """Génère la documentation des fonctions."""
        functions = doc_info.get("functions", [])
        md = [f"## 🔧 Fonctions ({len(functions)})\n"]
        
        for i, func in enumerate(functions, 1):
            md.append(self._format_function(func, i))
        
        return "\n".join(md)
    
    def _format_function(self, func: Dict[str, Any], index: int) -> str:
        """Formate une fonction individuelle."""
        md = [f"### {index}. `{func['name']}`\n"]
        
        # Métadonnées
        complexity_emoji = self._get_complexity_emoji(func.get("complexity", 0))
        md.append(f"**Complexité :** {complexity_emoji} {func.get('complexity', 0)} | ")
        md.append(f"**Lignes :** {func.get('line_start', 0)}-{func.get('line_end', 0)} | ")
        md.append(f"**Code :** {func.get('code_lines', 0)} lignes\n\n")
        
        # Signature
        signature = self._generate_function_signature(func)
        md.append(f"```python\n{signature}\n```\n")
        
        # Documentation originale
        if func.get("doc"):
            md.append("#### 📝 Documentation originale")
            md.append(f"```\n{func['doc']}\n```\n")
        
        # Documentation enrichie
        if func.get("enhanced_doc"):
            md.append("#### 🤖 Documentation enrichie par IA")
            md.append(f"{func['enhanced_doc']}\n")
        
        # Exemples
        if func.get("examples"):
            md.append("#### 💡 Exemples d'utilisation")
            md.append(f"{func['examples']}\n")
        
        # Conseils d'usage
        if func.get("usage_tips"):
            md.append("#### 💭 Conseils d'utilisation")
            md.append(f"{func['usage_tips']}\n")
        
        # Décorateurs
        if func.get("decorators"):
            md.append("#### 🎨 Décorateurs")
            for decorator in func["decorators"]:
                md.append(f"- `{decorator}`")
            md.append("")
        
        return "\n".join(md)
    
    def _generate_classes_documentation(self, doc_info: Dict[str, Any]) -> str:
        """Génère la documentation des classes."""
        classes = doc_info.get("classes", [])
        md = [f"## 🧱 Classes ({len(classes)})\n"]
        
        for i, cls in enumerate(classes, 1):
            md.append(self._format_class(cls, i))
        
        return "\n".join(md)
    
    def _format_class(self, cls: Dict[str, Any], index: int) -> str:
        """Formate une classe individuelle."""
        md = [f"### {index}. `{cls['name']}`\n"]
        
        # Métadonnées
        md.append(f"**Lignes :** {cls.get('line_start', 0)}-{cls.get('line_end', 0)} | ")
        md.append(f"**Méthodes :** {len(cls.get('methods', []))} | ")
        md.append(f"**Variables :** {len(cls.get('class_variables', []))}\n\n")
        
        # Héritage
        if cls.get("bases"):
            md.append("#### 🏗️ Héritage")
            md.append(f"```python\nclass {cls['name']}({', '.join(cls['bases'])}):\n```\n")
        
        # Documentation originale
        if cls.get("doc"):
            md.append("#### 📝 Documentation originale")
            md.append(f"```\n{cls['doc']}\n```\n")
        
        # Documentation enrichie
        if cls.get("enhanced_doc"):
            md.append("#### 🤖 Documentation enrichie par IA")
            md.append(f"{cls['enhanced_doc']}\n")
        
        # Variables de classe
        if cls.get("class_variables"):
            md.append("#### 📊 Variables de classe")
            for var in cls["class_variables"]:
                value = var.get("value", "Non définie")
                md.append(f"- `{var['name']}` = `{value}`")
            md.append("")
        
        # Méthodes
        if cls.get("methods"):
            md.append("#### 🔧 Méthodes")
            for method in cls["methods"]:
                md.append(f"- `{method['name']}({', '.join(method.get('args', []))})`")
            md.append("")
        
        # Patterns de conception
        if cls.get("design_patterns"):
            md.append("#### 🎯 Patterns de conception")
            md.append(f"{cls['design_patterns']}\n")
        
        # Exemples d'utilisation
        if cls.get("usage_examples"):
            md.append("#### 💡 Exemples d'utilisation")
            md.append(f"{cls['usage_examples']}\n")
        
        return "\n".join(md)
    
    def _generate_quality_analysis(self, doc_info: Dict[str, Any]) -> str:
        """Génère l'analyse de qualité."""
        quality = doc_info.get("quality_analysis", {})
        md = ["## 📊 Analyse de qualité\n"]
        
        # Métriques principales
        grade = quality.get("quality_grade", "N/A")
        coverage = quality.get("documentation_coverage", 0)
        complexity = quality.get("complexity_score", 0)
        high_complexity = quality.get("high_complexity_count", 0)
        
        md.append("### 🎯 Métriques principales")
        md.append(f"| Métrique | Valeur | Statut |")
        md.append(f"|----------|--------|--------|")
        md.append(f"| **Note globale** | {self._get_grade_emoji(grade)} {grade} | {self._get_quality_status(grade)} |")
        md.append(f"| **Couverture doc** | {coverage:.1f}% | {self._get_coverage_status(coverage)} |")
        md.append(f"| **Complexité moy.** | {complexity:.1f} | {self._get_complexity_status(complexity)} |")
        md.append(f"| **Fonctions complexes** | {high_complexity} | {self._get_high_complexity_status(high_complexity)} |")
        md.append("")
        
        # Recommandations
        if quality.get("recommendations"):
            md.append("### 💡 Recommandations")
            md.append(f"{quality['recommendations']}\n")
        
        return "\n".join(md)
    
    def _generate_improvement_suggestions(self, doc_info: Dict[str, Any]) -> str:
        """Génère les suggestions d'amélioration."""
        suggestions = doc_info.get("suggestions", {})
        md = ["## 💡 Suggestions d'amélioration\n"]
        
        if isinstance(suggestions, dict) and suggestions.get("suggestions"):
            md.append(suggestions["suggestions"])
        elif isinstance(suggestions, str):
            md.append(suggestions)
        
        # Éléments manquants
        if isinstance(suggestions, dict):
            if suggestions.get("missing_docs"):
                md.append("\n### 📝 Documentation manquante")
                md.append("Les éléments suivants n'ont pas de documentation :")
                for item in suggestions["missing_docs"]:
                    md.append(f"- `{item}`")
                md.append("")
            
            if suggestions.get("complexity_issues"):
                md.append("\n### ⚠️ Fonctions trop complexes")
                md.append("Ces fonctions ont une complexité cyclomatique élevée :")
                for func in suggestions["complexity_issues"]:
                    md.append(f"- `{func}`")
                md.append("")
        
        return "\n".join(md)
    
    def _generate_detailed_statistics(self, doc_info: Dict[str, Any]) -> str:
        """Génère les statistiques détaillées."""
        md = ["## 📈 Statistiques détaillées\n"]
        
        functions = doc_info.get("functions", [])
        classes = doc_info.get("classes", [])
        
        # Statistiques des fonctions
        if functions:
            md.append("### 🔧 Statistiques des fonctions")
            total_args = sum(len(f.get("args", [])) for f in functions)
            avg_args = total_args / len(functions) if functions else 0
            documented_funcs = len([f for f in functions if f.get("doc")])
            
            md.append(f"- **Total :** {len(functions)}")
            md.append(f"- **Documentées :** {documented_funcs} ({documented_funcs/len(functions)*100:.1f}%)")
            md.append(f"- **Arguments moyens :** {avg_args:.1f}")
            md.append(f"- **Complexité moyenne :** {sum(f.get('complexity', 0) for f in functions)/len(functions):.1f}")
            md.append("")
        
        # Statistiques des classes
        if classes:
            md.append("### 🧱 Statistiques des classes")
            total_methods = sum(len(c.get("methods", [])) for c in classes)
            total_vars = sum(len(c.get("class_variables", [])) for c in classes)
            documented_classes = len([c for c in classes if c.get("doc")])
            
            md.append(f"- **Total :** {len(classes)}")
            md.append(f"- **Documentées :** {documented_classes} ({documented_classes/len(classes)*100:.1f}%)")
            md.append(f"- **Méthodes totales :** {total_methods}")
            md.append(f"- **Variables de classe :** {total_vars}")
            md.append("")
        
        # Statistiques du fichier
        stats = doc_info.get("file_stats", {})
        if stats:
            md.append("### 📄 Statistiques du fichier")
            md.append(f"- **Lignes totales :** {stats.get('total_lines', 0)}")
            md.append(f"- **Lignes de code :** {stats.get('code_lines', 0)}")
            md.append(f"- **Lignes de commentaires :** {stats.get('comment_lines', 0)}")
            md.append("")
        
        return "\n".join(md)
    
    def _generate_footer(self, doc_info: Dict[str, Any]) -> str:
        """Génère le pied de page."""
        return f"""
---

<div align="center">

**📚 Documentation générée automatiquement avec [docGen](https://github.com/votre-repo/docGen)**

*Propulsé par Groq AI 🤖*

---

</div>
"""
    
    def _generate_function_signature(self, func: Dict[str, Any]) -> str:
        """Génère la signature d'une fonction."""
        args = func.get("args", [])
        defaults = func.get("defaults", [])
        returns = func.get("returns")
        
        # Construire la signature
        signature_parts = []
        for i, arg in enumerate(args):
            if i >= len(args) - len(defaults):
                default_idx = i - (len(args) - len(defaults))
                signature_parts.append(f"{arg}={defaults[default_idx]}")
            else:
                signature_parts.append(arg)
        
        signature = f"def {func['name']}({', '.join(signature_parts)})"
        if returns:
            signature += f" -> {returns}"
        signature += ":"
        
        return signature
    
    def _is_stdlib_import(self, module_name: str) -> bool:
        """Détermine si un module fait partie de la bibliothèque standard."""
        stdlib_modules = {
            'os', 'sys', 're', 'json', 'datetime', 'typing', 'collections',
            'pathlib', 'ast', 'logging', 'asyncio', 'argparse', 'setuptools',
            'pydantic', 'dotenv', 'enum', 'abc', 'itertools', 'functools'
        }
        return module_name.split('.')[0] in stdlib_modules
    
    def _get_grade_emoji(self, grade: str) -> str:
        """Retourne l'emoji correspondant à une note."""
        return {"A": "🟢", "B": "🟡", "C": "🟠", "D": "🔴", "E": "⚫"}.get(grade, "❓")
    
    def _get_complexity_emoji(self, complexity: int) -> str:
        """Retourne l'emoji correspondant à la complexité."""
        if complexity <= 3:
            return "🟢"
        elif complexity <= 7:
            return "🟡"
        elif complexity <= 10:
            return "🟠"
        else:
            return "🔴"
    
    def _get_quality_status(self, grade: str) -> str:
        """Retourne le statut de qualité."""
        return {
            "A": "Excellent", "B": "Bon", "C": "Moyen", 
            "D": "À améliorer", "E": "Critique"
        }.get(grade, "Inconnu")
    
    def _get_coverage_status(self, coverage: float) -> str:
        """Retourne le statut de couverture."""
        if coverage >= 90:
            return "🟢 Excellent"
        elif coverage >= 70:
            return "🟡 Bon"
        elif coverage >= 50:
            return "🟠 Moyen"
        else:
            return "🔴 Insuffisant"
    
    def _get_complexity_status(self, complexity: float) -> str:
        """Retourne le statut de complexité."""
        if complexity <= 5:
            return "🟢 Faible"
        elif complexity <= 10:
            return "🟡 Modérée"
        else:
            return "🔴 Élevée"
    
    def _get_high_complexity_status(self, count: int) -> str:
        """Retourne le statut des fonctions complexes."""
        if count == 0:
            return "🟢 Aucune"
        elif count <= 2:
            return "🟡 Acceptable"
        else:
            return "🔴 À refactoriser"

# Fonction de compatibilité
def format_markdown(doc_info: Dict[str, Any]) -> str:
    """Fonction de compatibilité avec l'API existante."""
    formatter = DocumentationFormatter()
    return formatter.format_markdown(doc_info)

def format_html(doc_info: dict) -> str:
    """Fonction de compatibilité pour format_html."""
    formatter = DocumentationFormatter()
    return formatter.format_html(doc_info)

def format_json(doc_info: dict, indent: int = 2) -> str:
    """Fonction de compatibilité pour format_json."""
    formatter = DocumentationFormatter()
    return formatter.format_json(doc_info, indent=indent)
