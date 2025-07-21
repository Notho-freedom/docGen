import ast
import asyncio
import logging
from typing import Dict, List, Optional, Any
try:
    from .providers.groq_client import GroqClient
    from .config import config
except ImportError:
    # Fallback pour les tests sans dépendances complètes
    GroqClient = None
    config = None

class DocGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if GroqClient is not None:
            self.groq_client = GroqClient(self.logger)
        else:
            self.groq_client = None
        
    def extract_doc_info(self, file_path: str) -> Dict[str, Any]:
        """Extrait les informations de documentation d'un fichier Python."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content, filename=file_path)

        doc_info = {
            "file_path": file_path,
            "functions": [],
            "classes": [],
            "module_doc": ast.get_docstring(tree),
            "imports": [],
            "file_stats": {
                "total_lines": len(content.split('\n')),
                "code_lines": 0,
                "comment_lines": 0
            }
        }

        # Extraction des imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    doc_info["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    doc_info["imports"].append(f"{module}.{alias.name}")

        # Extraction des fonctions et classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, content)
                doc_info["functions"].append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, content)
                doc_info["classes"].append(class_info)

        return doc_info

    def _extract_function_info(self, node: ast.FunctionDef, content: str) -> Dict[str, Any]:
        """Extrait les informations détaillées d'une fonction."""
        # Obtenir le code source de la fonction
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
        
        # Compter les lignes de code et commentaires
        lines = content.split('\n')[start_line-1:end_line]
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        
        return {
            "name": node.name,
            "doc": ast.get_docstring(node),
            "args": [arg.arg for arg in node.args.args],
            "defaults": [ast.unparse(default) for default in node.args.defaults],
            "returns": ast.unparse(node.returns) if node.returns else None,
            "decorators": [ast.unparse(decorator) for decorator in node.decorator_list],
            "line_start": start_line,
            "line_end": end_line,
            "complexity": self._calculate_complexity(node),
            "code_lines": code_lines,
            "comment_lines": comment_lines
        }

    def _extract_class_info(self, node: ast.ClassDef, content: str) -> Dict[str, Any]:
        """Extrait les informations détaillées d'une classe."""
        methods = []
        class_vars = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_function_info(item, content)
                methods.append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_vars.append({
                            "name": target.id,
                            "value": ast.unparse(item.value) if item.value else None
                        })

        return {
            "name": node.name,
            "doc": ast.get_docstring(node),
            "bases": [ast.unparse(base) for base in node.bases],
            "methods": methods,
            "class_variables": class_vars,
            "decorators": [ast.unparse(decorator) for decorator in node.decorator_list],
            "line_start": node.lineno,
            "line_end": node.end_lineno if hasattr(node, 'end_lineno') else node.lineno
        }

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calcule la complexité cyclomatique d'un nœud AST."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, 
                                ast.ExceptHandler, ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    async def enrich_documentation(self, doc_info: Dict[str, Any]) -> Dict[str, Any]:
        """Enrichit la documentation avec l'IA Groq."""
        if self.groq_client is None:
            self.logger.warning("Groq client non disponible, enrichissement désactivé")
            return doc_info
            
        try:
            # Enrichir la documentation du module
            if doc_info["module_doc"]:
                enhanced_module_doc = await self._enhance_module_doc(doc_info)
                doc_info["enhanced_module_doc"] = enhanced_module_doc

            # Enrichir chaque fonction
            for func in doc_info["functions"]:
                enhanced_func = await self._enhance_function_doc(func, doc_info)
                func.update(enhanced_func)

            # Enrichir chaque classe
            for cls in doc_info["classes"]:
                enhanced_cls = await self._enhance_class_doc(cls, doc_info)
                cls.update(enhanced_cls)

            # Générer des suggestions d'amélioration
            suggestions = await self._generate_improvement_suggestions(doc_info)
            doc_info["suggestions"] = suggestions

            # Analyser la qualité du code
            quality_analysis = await self._analyze_code_quality(doc_info)
            doc_info["quality_analysis"] = quality_analysis

        except Exception as e:
            self.logger.error(f"Erreur lors de l'enrichissement: {e}")
            
        return doc_info

    async def _enhance_module_doc(self, doc_info: Dict[str, Any]) -> str:
        """Améliore la documentation du module avec Groq."""
        prompt = f"""
        Améliore la documentation suivante d'un module Python. 
        Ajoute des détails sur l'objectif, les fonctionnalités principales, et l'utilisation.
        
        Module: {doc_info['file_path']}
        Documentation actuelle: {doc_info['module_doc']}
        
        Fonctions: {[f['name'] for f in doc_info['functions']]}
        Classes: {[c['name'] for c in doc_info['classes']]}
        
        Génère une documentation claire, complète et professionnelle en français.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=500
        )
        
        return response or doc_info["module_doc"]

    async def _enhance_function_doc(self, func: Dict[str, Any], doc_info: Dict[str, Any]) -> Dict[str, Any]:
        """Améliore la documentation d'une fonction avec Groq."""
        prompt = f"""
        Améliore la documentation de cette fonction Python.
        
        Fonction: {func['name']}
        Arguments: {func['args']}
        Valeurs par défaut: {func['defaults']}
        Type de retour: {func['returns']}
        Documentation actuelle: {func['doc']}
        Complexité: {func['complexity']}
        
        Génère:
        1. Une description claire de la fonction
        2. Des exemples d'utilisation
        3. Des explications sur les paramètres
        4. Des cas d'usage typiques
        
        Réponds en français de manière structurée.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=400
        )
        
        return {
            "enhanced_doc": response or func["doc"],
            "examples": await self._generate_function_examples(func),
            "usage_tips": await self._generate_usage_tips(func)
        }

    async def _enhance_class_doc(self, cls: Dict[str, Any], doc_info: Dict[str, Any]) -> Dict[str, Any]:
        """Améliore la documentation d'une classe avec Groq."""
        prompt = f"""
        Améliore la documentation de cette classe Python.
        
        Classe: {cls['name']}
        Héritage: {cls['bases']}
        Méthodes: {[m['name'] for m in cls['methods']]}
        Variables de classe: {[v['name'] for v in cls['class_variables']]}
        Documentation actuelle: {cls['doc']}
        
        Génère:
        1. Une description claire de la classe
        2. Le rôle de chaque méthode
        3. Des exemples d'utilisation
        4. Des patterns de conception utilisés
        
        Réponds en français de manière structurée.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=500
        )
        
        return {
            "enhanced_doc": response or cls["doc"],
            "design_patterns": await self._identify_design_patterns(cls),
            "usage_examples": await self._generate_class_examples(cls)
        }

    async def _generate_function_examples(self, func: Dict[str, Any]) -> str:
        """Génère des exemples d'utilisation pour une fonction."""
        prompt = f"""
        Génère des exemples d'utilisation pratiques pour cette fonction Python:
        
        Nom: {func['name']}
        Arguments: {func['args']}
        Valeurs par défaut: {func['defaults']}
        Type de retour: {func['returns']}
        
        Crée 2-3 exemples concrets et utiles en français.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.4,
            max_tokens=300
        )
        
        return response or "Aucun exemple généré."

    async def _generate_usage_tips(self, func: Dict[str, Any]) -> str:
        """Génère des conseils d'utilisation pour une fonction."""
        prompt = f"""
        Génère des conseils d'utilisation pour cette fonction:
        
        Fonction: {func['name']}
        Complexité: {func['complexity']}
        Arguments: {func['args']}
        
        Donne des conseils sur:
        - Quand utiliser cette fonction
        - Les bonnes pratiques
        - Les pièges à éviter
        
        Réponds en français.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=200
        )
        
        return response or "Aucun conseil généré."

    async def _identify_design_patterns(self, cls: Dict[str, Any]) -> str:
        """Identifie les patterns de conception utilisés dans une classe."""
        prompt = f"""
        Identifie les patterns de conception utilisés dans cette classe:
        
        Classe: {cls['name']}
        Méthodes: {[m['name'] for m in cls['methods']]}
        Variables: {[v['name'] for v in cls['class_variables']]}
        Héritage: {cls['bases']}
        
        Analyse et explique les patterns détectés en français.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.2,
            max_tokens=250
        )
        
        return response or "Aucun pattern identifié."

    async def _generate_class_examples(self, cls: Dict[str, Any]) -> str:
        """Génère des exemples d'utilisation pour une classe."""
        prompt = f"""
        Génère des exemples d'utilisation pour cette classe:
        
        Classe: {cls['name']}
        Méthodes: {[m['name'] for m in cls['methods']]}
        
        Crée des exemples montrant:
        - L'instanciation
        - L'utilisation des méthodes principales
        - Des cas d'usage typiques
        
        Réponds en français avec du code Python.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.4,
            max_tokens=400
        )
        
        return response or "Aucun exemple généré."

    async def _generate_improvement_suggestions(self, doc_info: Dict[str, Any]) -> Dict[str, Any]:
        """Génère des suggestions d'amélioration pour le code."""
        prompt = f"""
        Analyse ce code Python et génère des suggestions d'amélioration:
        
        Fichier: {doc_info['file_path']}
        Fonctions: {len(doc_info['functions'])}
        Classes: {len(doc_info['classes'])}
        
        Fonctions sans docstring: {[f['name'] for f in doc_info['functions'] if not f['doc']]}
        Classes sans docstring: {[c['name'] for c in doc_info['classes'] if not c['doc']]}
        
        Suggère des améliorations pour:
        - La documentation manquante
        - La qualité du code
        - Les bonnes pratiques
        - La lisibilité
        
        Réponds en français de manière structurée.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=400
        )
        
        return {
            "suggestions": response or "Aucune suggestion générée.",
            "missing_docs": [f['name'] for f in doc_info['functions'] if not f['doc']] + 
                          [c['name'] for c in doc_info['classes'] if not c['doc']],
            "complexity_issues": [f['name'] for f in doc_info['functions'] if f['complexity'] > 10]
        }

    async def _analyze_code_quality(self, doc_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse la qualité du code."""
        total_functions = len(doc_info['functions'])
        documented_functions = len([f for f in doc_info['functions'] if f['doc']])
        high_complexity_functions = len([f for f in doc_info['functions'] if f['complexity'] > 10])
        
        return {
            "documentation_coverage": (documented_functions / total_functions * 100) if total_functions > 0 else 0,
            "complexity_score": sum(f['complexity'] for f in doc_info['functions']) / total_functions if total_functions > 0 else 0,
            "high_complexity_count": high_complexity_functions,
            "quality_grade": self._calculate_quality_grade(doc_info),
            "recommendations": await self._generate_quality_recommendations(doc_info)
        }

    def _calculate_quality_grade(self, doc_info: Dict[str, Any]) -> str:
        """Calcule une note de qualité pour le code."""
        score = 0
        total_functions = len(doc_info['functions'])
        
        if total_functions == 0:
            return "A"
            
        # Documentation
        documented = len([f for f in doc_info['functions'] if f['doc']])
        score += (documented / total_functions) * 40
        
        # Complexité
        avg_complexity = sum(f['complexity'] for f in doc_info['functions']) / total_functions
        if avg_complexity < 5:
            score += 30
        elif avg_complexity < 10:
            score += 20
        else:
            score += 10
            
        # Structure
        if doc_info['module_doc']:
            score += 15
        if doc_info['classes']:
            score += 15
            
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "E"

    async def _generate_quality_recommendations(self, doc_info: Dict[str, Any]) -> str:
        """Génère des recommandations pour améliorer la qualité."""
        prompt = f"""
        Génère des recommandations spécifiques pour améliorer la qualité de ce code:
        
        Fichier: {doc_info['file_path']}
        Note de qualité: {self._calculate_quality_grade(doc_info)}
        
        Analyse et propose des améliorations concrètes et prioritaires.
        """
        
        response = await self.groq_client.async_chat_completion(
            model=config.groq_models[0],
            user_message=prompt,
            temperature=0.3,
            max_tokens=300
        )
        
        return response or "Aucune recommandation générée."

# Fonction de compatibilité pour l'API existante
def extract_doc_info(file_path: str) -> Dict[str, Any]:
    """Fonction de compatibilité avec l'API existante."""
    generator = DocGenerator()
    return generator.extract_doc_info(file_path)

async def extract_doc_info_enhanced(file_path: str) -> Dict[str, Any]:
    """Version enrichie avec IA de l'extraction de documentation."""
    generator = DocGenerator()
    doc_info = generator.extract_doc_info(file_path)
    return await generator.enrich_documentation(doc_info)
