#!/usr/bin/env python3
"""
Script de validation pour docGen AI.

Ce script teste tous les aspects de l'installation et de la structure du projet
pour s'assurer que tout fonctionne correctement.
"""

import sys
import os
import asyncio
from pathlib import Path

def print_status(message, status="INFO"):
    """Affiche un message avec un statut coloré."""
    colors = {
        "INFO": "\033[94m",    # Bleu
        "SUCCESS": "\033[92m", # Vert
        "WARNING": "\033[93m", # Jaune
        "ERROR": "\033[91m",   # Rouge
        "RESET": "\033[0m"     # Reset
    }
    print(f"{colors.get(status, '')}[{status}]{colors['RESET']} {message}")

def test_imports():
    """Teste les imports des modules principaux."""
    print_status("🔍 Test des imports...", "INFO")
    
    try:
        import docgen
        print_status("✅ Package docgen importé", "SUCCESS")
    except ImportError as e:
        print_status(f"❌ Erreur import docgen: {e}", "ERROR")
        return False
    
    try:
        from docgen import DocGenerator, DocumentationFormatter
        print_status("✅ Classes principales importées", "SUCCESS")
    except ImportError as e:
        print_status(f"❌ Erreur import classes: {e}", "ERROR")
        return False
    
    try:
        from docgen.providers import GroqClient, Memory
        print_status("✅ Providers importés", "SUCCESS")
    except ImportError as e:
        print_status(f"❌ Erreur import providers: {e}", "ERROR")
        return False
    
    return True

def test_configuration():
    """Teste la configuration."""
    print_status("⚙️ Test de la configuration...", "INFO")
    
    try:
        from docgen.config import config
        print_status(f"✅ Configuration chargée - Modèle: {config.groq_models[0] if config.groq_models else 'Non configuré'}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"❌ Erreur configuration: {e}", "ERROR")
        return False

def test_basic_extraction():
    """Teste l'extraction basique."""
    print_status("📝 Test d'extraction basique...", "INFO")
    
    try:
        from docgen import extract_doc_info
        
        # Créer un fichier de test temporaire
        test_file = "test_validation.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write('''
"""
Fichier de test pour validation.
"""

def test_function():
    """Fonction de test."""
    return "test"

class TestClass:
    """Classe de test."""
    
    def __init__(self):
        """Initialisation."""
        pass
''')
        
        # Tester l'extraction
        doc_info = extract_doc_info(test_file)
        
        if doc_info and "functions" in doc_info and "classes" in doc_info:
            print_status(f"✅ Extraction réussie - {len(doc_info['functions'])} fonctions, {len(doc_info['classes'])} classes", "SUCCESS")
            
            # Nettoyer
            os.remove(test_file)
            return True
        else:
            print_status("❌ Extraction échouée - données invalides", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Erreur extraction: {e}", "ERROR")
        return False

async def test_enhanced_extraction():
    """Teste l'extraction enrichie."""
    print_status("🤖 Test d'extraction enrichie...", "INFO")
    
    try:
        from docgen import extract_doc_info_enhanced
        
        # Créer un fichier de test temporaire
        test_file = "test_enhanced.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write('''
"""
Fichier de test pour validation enrichie.
"""

def enhanced_function():
    """Fonction avec documentation enrichie."""
    return "enhanced"
''')
        
        # Tester l'extraction enrichie
        doc_info = await extract_doc_info_enhanced(test_file)
        
        if doc_info and "functions" in doc_info:
            print_status(f"✅ Extraction enrichie réussie - {len(doc_info['functions'])} fonctions", "SUCCESS")
            
            # Nettoyer
            os.remove(test_file)
            return True
        else:
            print_status("❌ Extraction enrichie échouée", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Erreur extraction enrichie: {e}", "ERROR")
        return False

def test_formatter():
    """Teste le formateur."""
    print_status("🎨 Test du formateur...", "INFO")
    
    try:
        from docgen import DocumentationFormatter
        
        formatter = DocumentationFormatter()
        
        # Données de test
        test_data = {
            "module_name": "test_module",
            "module_doc": "Module de test",
            "functions": [
                {
                    "name": "test_func",
                    "doc": "Fonction de test",
                    "complexity": 1,
                    "lines": (1, 5)
                }
            ],
            "classes": [],
            "imports": {"standard": [], "third_party": []},
            "stats": {"total_lines": 10, "code_lines": 5}
        }
        
        # Tester le formatage
        markdown = formatter.format_markdown(test_data)
        
        if markdown and len(markdown) > 100:
            print_status("✅ Formatage Markdown réussi", "SUCCESS")
            return True
        else:
            print_status("❌ Formatage échoué", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"❌ Erreur formateur: {e}", "ERROR")
        return False

def test_cli():
    """Teste l'interface CLI."""
    print_status("💻 Test de l'interface CLI...", "INFO")
    
    try:
        from docgen.cli import main
        import sys
        from io import StringIO
        
        # Capturer la sortie
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Simuler l'appel avec --help
        sys.argv = ["docgen", "--help"]
        
        try:
            main()
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if "usage:" in output or "Générateur de documentation" in output:
                print_status("✅ CLI fonctionne correctement", "SUCCESS")
                return True
            else:
                print_status("❌ CLI ne fonctionne pas", "ERROR")
                return False
                
        except SystemExit:
            # --help provoque un SystemExit, c'est normal
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if "usage:" in output or "Générateur de documentation" in output:
                print_status("✅ CLI fonctionne correctement", "SUCCESS")
                return True
            else:
                print_status("❌ CLI ne fonctionne pas", "ERROR")
                return False
            
    except Exception as e:
        print_status(f"❌ Erreur CLI: {e}", "ERROR")
        return False

def test_project_structure():
    """Teste la structure du projet."""
    print_status("📁 Test de la structure du projet...", "INFO")
    
    required_files = [
        "docgen/__init__.py",
        "docgen/docgen.py",
        "docgen/formatter.py",
        "docgen/cli.py",
        "docgen/config.py",
        "docgen/providers/__init__.py",
        "docgen/providers/groq_client.py",
        "docgen/providers/memory.py",
        "tests/__init__.py",
        "tests/test_docgen.py",
        "Config/setup.py",
        "Config/pyproject.toml",
        "Config/requirements.txt",
        "Config/requirements-dev.txt",
        "docs/README.md",
        "docs/STRUCTURE.md",
        "Config/env.example"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if not missing_files:
        print_status("✅ Structure du projet complète", "SUCCESS")
        return True
    else:
        print_status(f"❌ Fichiers manquants: {missing_files}", "ERROR")
        return False

def main():
    """Fonction principale de validation."""
    print_status("🚀 Démarrage de la validation docGen AI", "INFO")
    print_status("=" * 50, "INFO")
    
    tests = [
        ("Structure du projet", test_project_structure),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Extraction basique", test_basic_extraction),
        ("Formateur", test_formatter),
        ("Interface CLI", test_cli),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print_status(f"\n🔍 Test: {test_name}", "INFO")
        try:
            if test_func():
                passed += 1
            else:
                print_status(f"❌ Test '{test_name}' échoué", "ERROR")
        except Exception as e:
            print_status(f"❌ Erreur dans le test '{test_name}': {e}", "ERROR")
    
    # Test asynchrone séparé
    print_status(f"\n🔍 Test: Extraction enrichie", "INFO")
    try:
        if asyncio.run(test_enhanced_extraction()):
            passed += 1
        else:
            print_status("❌ Test 'Extraction enrichie' échoué", "ERROR")
    except Exception as e:
        print_status(f"❌ Erreur dans le test 'Extraction enrichie': {e}", "ERROR")
    
    total += 1
    
    print_status("=" * 50, "INFO")
    print_status(f"📊 Résultats: {passed}/{total} tests réussis", "INFO")
    
    if passed == total:
        print_status("🎉 Tous les tests sont passés ! Installation validée.", "SUCCESS")
        return 0
    else:
        print_status("⚠️ Certains tests ont échoué. Vérifiez l'installation.", "WARNING")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 