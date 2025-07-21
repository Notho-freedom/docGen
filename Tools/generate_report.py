#!/usr/bin/env python3
"""
Script de génération de rapports pour docGen AI.

Ce script génère des rapports de documentation et les place dans le dossier Log.
"""

import sys
import os
import asyncio
from pathlib import Path
from datetime import datetime
import json

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

def ensure_log_directory():
    """S'assure que le dossier Log existe."""
    log_dir = Path("Log")
    if not log_dir.exists():
        log_dir.mkdir()
        print_status("📁 Dossier Log créé", "INFO")
    return log_dir

def generate_basic_report(file_path, output_format="markdown"):
    """Génère un rapport basique."""
    try:
        from docgen import extract_doc_info
        
        print_status(f"📝 Génération du rapport basique pour {file_path}...", "INFO")
        
        # Extraction
        doc_info = extract_doc_info(file_path)
        
        # Génération du rapport
        if output_format == "markdown":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_markdown(doc_info)
            extension = "md"
        elif output_format == "html":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_html(doc_info)
            extension = "html"
        elif output_format == "json":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_json(doc_info, indent=2)
            extension = "json"
        else:
            raise ValueError(f"Format non supporté: {output_format}")
        
        # Sauvegarde dans Log
        log_dir = ensure_log_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Path(file_path).stem}_basic_{timestamp}.{extension}"
        output_path = log_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_status(f"✅ Rapport basique généré: {output_path}", "SUCCESS")
        return str(output_path)
        
    except Exception as e:
        print_status(f"❌ Erreur génération rapport basique: {e}", "ERROR")
        return None

async def generate_enhanced_report(file_path, output_format="markdown"):
    """Génère un rapport enrichi par IA."""
    try:
        from docgen import extract_doc_info_enhanced
        
        print_status(f"🤖 Génération du rapport enrichi pour {file_path}...", "INFO")
        
        # Extraction enrichie
        doc_info = await extract_doc_info_enhanced(file_path)
        
        # Génération du rapport
        if output_format == "markdown":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_markdown(doc_info)
            extension = "md"
        elif output_format == "html":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_html(doc_info)
            extension = "html"
        elif output_format == "json":
            from docgen import DocumentationFormatter
            formatter = DocumentationFormatter()
            content = formatter.format_json(doc_info, indent=2)
            extension = "json"
        else:
            raise ValueError(f"Format non supporté: {output_format}")
        
        # Sauvegarde dans Log
        log_dir = ensure_log_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{Path(file_path).stem}_enhanced_{timestamp}.{extension}"
        output_path = log_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_status(f"✅ Rapport enrichi généré: {output_path}", "SUCCESS")
        return str(output_path)
        
    except Exception as e:
        print_status(f"❌ Erreur génération rapport enrichi: {e}", "ERROR")
        return None

def generate_validation_report():
    """Génère un rapport de validation du projet."""
    try:
        print_status("🔍 Génération du rapport de validation...", "INFO")
        
        # Importer le script de validation
        sys.path.insert(0, str(Path("Tools")))
        from validate_installation import test_imports, test_configuration, test_formatter, test_cli
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": "docGen AI",
            "version": "2.0.0",
            "tests": {}
        }
        
        # Tests synchrones
        tests = [
            ("imports", test_imports),
            ("configuration", test_configuration),
            ("formatter", test_formatter),
            ("cli", test_cli)
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                report["tests"][test_name] = {
                    "status": "passed" if result else "failed",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                report["tests"][test_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        # Test asynchrone
        try:
            from validate_installation import test_enhanced_extraction
            result = asyncio.run(test_enhanced_extraction())
            report["tests"]["enhanced_extraction"] = {
                "status": "passed" if result else "failed",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            report["tests"]["enhanced_extraction"] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # Sauvegarde dans Log
        log_dir = ensure_log_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"validation_report_{timestamp}.json"
        output_path = log_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print_status(f"✅ Rapport de validation généré: {output_path}", "SUCCESS")
        return str(output_path)
        
    except Exception as e:
        print_status(f"❌ Erreur génération rapport validation: {e}", "ERROR")
        return None

def generate_project_analysis():
    """Génère une analyse complète du projet."""
    try:
        print_status("📊 Génération de l'analyse du projet...", "INFO")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "project": "docGen AI",
            "structure": {},
            "files": {},
            "statistics": {}
        }
        
        # Analyse de la structure
        structure_dirs = ["docgen", "tests", "docs", "examples", "templates", "Tools", "Config", "Build"]
        for dir_name in structure_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                analysis["structure"][dir_name] = {
                    "exists": True,
                    "files": len(list(dir_path.rglob("*.py"))) if dir_path.is_dir() else 0,
                    "size": sum(f.stat().st_size for f in dir_path.rglob("*") if f.is_file())
                }
            else:
                analysis["structure"][dir_name] = {
                    "exists": False,
                    "files": 0,
                    "size": 0
                }
        
        # Analyse des fichiers Python
        python_files = list(Path(".").rglob("*.py"))
        analysis["files"]["python_count"] = len(python_files)
        analysis["files"]["python_list"] = [str(f) for f in python_files]
        
        # Statistiques
        total_lines = 0
        total_size = 0
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                total_size += py_file.stat().st_size
            except Exception:
                pass
        
        analysis["statistics"] = {
            "total_python_files": len(python_files),
            "total_lines": total_lines,
            "total_size_bytes": total_size,
            "average_lines_per_file": total_lines / len(python_files) if python_files else 0
        }
        
        # Sauvegarde dans Log
        log_dir = ensure_log_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"project_analysis_{timestamp}.json"
        output_path = log_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print_status(f"✅ Analyse du projet générée: {output_path}", "SUCCESS")
        return str(output_path)
        
    except Exception as e:
        print_status(f"❌ Erreur analyse du projet: {e}", "ERROR")
        return None

def main():
    """Fonction principale."""
    print_status("🚀 Démarrage de la génération de rapports docGen AI", "INFO")
    print_status("=" * 60, "INFO")
    
    # S'assurer que le dossier Log existe
    ensure_log_directory()
    
    # Générer les rapports
    reports = []
    
    # Rapport de validation
    validation_report = generate_validation_report()
    if validation_report:
        reports.append(validation_report)
    
    # Analyse du projet
    analysis_report = generate_project_analysis()
    if analysis_report:
        reports.append(analysis_report)
    
    # Rapports de documentation pour les exemples
    example_files = list(Path("examples").glob("*.py"))
    for example_file in example_files:
        print_status(f"\n📄 Traitement de {example_file}...", "INFO")
        
        # Rapport basique
        basic_report = generate_basic_report(str(example_file), "markdown")
        if basic_report:
            reports.append(basic_report)
        
        # Rapport enrichi
        enhanced_report = asyncio.run(generate_enhanced_report(str(example_file), "markdown"))
        if enhanced_report:
            reports.append(enhanced_report)
    
    # Résumé
    print_status("=" * 60, "INFO")
    print_status(f"📊 Résumé: {len(reports)} rapports générés", "INFO")
    
    for report in reports:
        print_status(f"📄 {report}", "SUCCESS")
    
    print_status("🎉 Génération de rapports terminée !", "SUCCESS")
    print_status("📁 Tous les rapports ont été sauvegardés dans le dossier Log", "INFO")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 