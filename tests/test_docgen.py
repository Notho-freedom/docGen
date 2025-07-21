#!/usr/bin/env python3
"""
Tests pour docGen AI.

Ce fichier contient des tests simples pour valider le fonctionnement
du système de génération de documentation.
"""

import asyncio
import tempfile
import os
from pathlib import Path
from docgen import DocGenerator, extract_doc_info
from formatter import DocumentationFormatter

def test_basic_extraction():
    """Test de l'extraction basique de documentation."""
    print("🧪 Test d'extraction basique...")
    
    # Créer un fichier Python temporaire pour le test
    test_code = '''
"""
Module de test pour docGen AI.
"""

def simple_function():
    """Fonction simple pour les tests."""
    return "Hello World"

class TestClass:
    """Classe de test."""
    
    def __init__(self):
        """Initialise la classe de test."""
        self.value = 42
    
    def get_value(self):
        """Retourne la valeur."""
        return self.value
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Test de l'extraction
        doc_info = extract_doc_info(temp_file)
        
        # Vérifications
        assert doc_info['module_doc'] is not None
        assert len(doc_info['functions']) == 1
        assert len(doc_info['classes']) == 1
        assert doc_info['functions'][0]['name'] == 'simple_function'
        assert doc_info['classes'][0]['name'] == 'TestClass'
        
        print("✅ Test d'extraction basique réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Test d'extraction basique échoué: {e}")
        return False
    finally:
        # Nettoyage
        os.unlink(temp_file)

def test_formatter():
    """Test du formateur de documentation."""
    print("🧪 Test du formateur...")
    
    # Données de test
    test_doc_info = {
        "file_path": "test.py",
        "module_doc": "Module de test",
        "functions": [
            {
                "name": "test_func",
                "doc": "Fonction de test",
                "args": ["param1", "param2"],
                "complexity": 3,
                "line_start": 10,
                "line_end": 15,
                "code_lines": 5
            }
        ],
        "classes": [
            {
                "name": "TestClass",
                "doc": "Classe de test",
                "methods": [],
                "line_start": 20,
                "line_end": 25
            }
        ],
        "imports": ["os", "sys"],
        "file_stats": {
            "total_lines": 50,
            "code_lines": 30,
            "comment_lines": 10
        }
    }
    
    try:
        # Test du formateur
        formatter = DocumentationFormatter()
        markdown_output = formatter.format_markdown(test_doc_info)
        
        # Vérifications
        assert "# 📚 Documentation - test.py" in markdown_output
        assert "## 🔧 Fonctions (1)" in markdown_output
        assert "## 🧱 Classes (1)" in markdown_output
        assert "test_func" in markdown_output
        assert "TestClass" in markdown_output
        
        print("✅ Test du formateur réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Test du formateur échoué: {e}")
        return False

async def test_enhanced_extraction():
    """Test de l'extraction enrichie (sans IA)."""
    print("🧪 Test d'extraction enrichie...")
    
    # Créer un fichier Python temporaire pour le test
    test_code = '''
"""
Module de test avancé.
"""

def complex_function(param1: str, param2: int = 42) -> str:
    """
    Fonction complexe avec types et valeurs par défaut.
    
    Args:
        param1: Premier paramètre
        param2: Deuxième paramètre avec valeur par défaut
        
    Returns:
        Chaîne de caractères résultante
    """
    if param2 > 50:
        return f"Grande valeur: {param1}"
    else:
        return f"Petite valeur: {param1}"

class AdvancedClass:
    """Classe avancée avec héritage."""
    
    class_var = "Variable de classe"
    
    def __init__(self, name: str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Test de l'extraction enrichie
        generator = DocGenerator()
        doc_info = generator.extract_doc_info(temp_file)
        
        # Vérifications avancées
        assert doc_info['module_doc'] is not None
        assert len(doc_info['functions']) == 1
        assert len(doc_info['classes']) == 1
        
        func = doc_info['functions'][0]
        assert func['name'] == 'complex_function'
        assert 'param1' in func['args']
        assert 'param2' in func['args']
        assert func['complexity'] > 0
        assert func['line_start'] > 0
        assert func['line_end'] > func['line_start']
        
        cls = doc_info['classes'][0]
        assert cls['name'] == 'AdvancedClass'
        assert len(cls['methods']) == 2  # __init__ et get_name
        assert len(cls['class_variables']) == 1
        
        print("✅ Test d'extraction enrichie réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Test d'extraction enrichie échoué: {e}")
        return False
    finally:
        # Nettoyage
        os.unlink(temp_file)

def test_cli_help():
    """Test de l'aide du CLI."""
    print("🧪 Test de l'aide CLI...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["python", "cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Vérifications
        assert result.returncode == 0
        assert "Générateur de documentation Python intelligent" in result.stdout
        assert "--enhanced" in result.stdout
        assert "--format" in result.stdout
        
        print("✅ Test de l'aide CLI réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Test de l'aide CLI échoué: {e}")
        return False

async def main():
    """Fonction principale des tests."""
    print("🚀 Lancement des tests docGen AI")
    print("=" * 50)
    
    tests = [
        test_basic_extraction,
        test_formatter,
        test_enhanced_extraction,
        test_cli_help
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if asyncio.iscoroutinefunction(test):
                result = await test()
            else:
                result = test()
            
            if result:
                passed += 1
                
        except Exception as e:
            print(f"❌ Test {test.__name__} a levé une exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés!")
        return True
    else:
        print("⚠️  Certains tests ont échoué.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 