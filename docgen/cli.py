import argparse
import asyncio
import logging
import sys
from pathlib import Path
from .docgen import extract_doc_info, extract_doc_info_enhanced, DocGenerator
from .formatter import format_markdown, DocumentationFormatter

def setup_logging(verbose: bool = False):
    """Configure le système de logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_file_path(file_path: str) -> Path:
    """Valide le chemin du fichier."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    if not path.suffix == '.py':
        raise ValueError(f"Le fichier {file_path} n'est pas un fichier Python (.py)")
    return path

async def generate_documentation(
    file_path: Path,
    output_path: Path,
    enhanced: bool = False,
    format_type: str = "markdown",
    verbose: bool = False
) -> None:
    """Génère la documentation pour un fichier Python."""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"📖 Analyse du fichier : {file_path}")
        
        if enhanced:
            logger.info("🤖 Génération de documentation enrichie avec IA...")
            doc_info = await extract_doc_info_enhanced(str(file_path))
        else:
            logger.info("📝 Génération de documentation basique...")
            doc_info = extract_doc_info(str(file_path))
        
        logger.info(f"✅ Analyse terminée - {len(doc_info.get('functions', []))} fonctions, {len(doc_info.get('classes', []))} classes")
        
        # Génération du contenu selon le format
        if format_type == "markdown":
            content = format_markdown(doc_info)
        elif format_type == "json":
            import json
            content = json.dumps(doc_info, indent=2, ensure_ascii=False)
        elif format_type == "html":
            content = generate_html(doc_info)
        else:
            raise ValueError(f"Format non supporté : {format_type}")
        
        # Écriture du fichier de sortie
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"✅ Documentation générée : {output_path}")
        
        # Affichage des statistiques
        if enhanced and "quality_analysis" in doc_info:
            quality = doc_info["quality_analysis"]
            print(f"\n📊 Statistiques de qualité :")
            print(f"   Note : {quality.get('quality_grade', 'N/A')}")
            print(f"   Couverture doc : {quality.get('documentation_coverage', 0):.1f}%")
            print(f"   Complexité moyenne : {quality.get('complexity_score', 0):.1f}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération : {e}")
        raise

def generate_html(doc_info: dict) -> str:
    """Génère une version HTML de la documentation."""
    # Template HTML simple mais élégant
    html_template = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - {file_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin: 2px; }}
        .badge-success {{ background: #27ae60; color: white; }}
        .badge-warning {{ background: #f39c12; color: white; }}
        .badge-danger {{ background: #e74c3c; color: white; }}
        .badge-info {{ background: #3498db; color: white; }}
        .function, .class {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
        .signature {{ background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 5px; font-family: 'Courier New', monospace; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; font-size: 14px; }}
        pre {{ background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        code {{ background: #f1f2f6; padding: 2px 4px; border-radius: 3px; }}
        .toc {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .toc ul {{ list-style-type: none; padding-left: 0; }}
        .toc li {{ margin: 5px 0; }}
        .toc a {{ text-decoration: none; color: #3498db; }}
        .toc a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Documentation - {file_name}</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{function_count}</div>
                <div class="stat-label">Fonctions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{class_count}</div>
                <div class="stat-label">Classes</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{doc_coverage:.1f}%</div>
                <div class="stat-label">Couverture doc</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{quality_grade}</div>
                <div class="stat-label">Note qualité</div>
            </div>
        </div>
        
        {content}
    </div>
</body>
</html>
"""
    
    # Préparer les données pour le template
    file_name = Path(doc_info.get("file_path", "unknown")).name
    function_count = len(doc_info.get("functions", []))
    class_count = len(doc_info.get("classes", []))
    
    quality = doc_info.get("quality_analysis", {})
    doc_coverage = quality.get("documentation_coverage", 0)
    quality_grade = quality.get("quality_grade", "N/A")
    
    # Générer le contenu HTML
    content_parts = []
    
    # Module documentation
    if doc_info.get("module_doc") or doc_info.get("enhanced_module_doc"):
        content_parts.append("<h2>📖 Documentation du module</h2>")
        if doc_info.get("enhanced_module_doc"):
            content_parts.append(f"<p>{doc_info['enhanced_module_doc']}</p>")
        elif doc_info.get("module_doc"):
            content_parts.append(f"<pre>{doc_info['module_doc']}</pre>")
    
    # Functions
    if doc_info.get("functions"):
        content_parts.append("<h2>🔧 Fonctions</h2>")
        for func in doc_info["functions"]:
            content_parts.append(f"""
            <div class="function">
                <h3>{func['name']}</h3>
                <div class="signature">{func.get('signature', f"def {func['name']}()")}</div>
                {f"<p><strong>Complexité :</strong> {func.get('complexity', 0)}</p>" if func.get('complexity') else ""}
                {f"<p><strong>Documentation :</strong> {func.get('enhanced_doc', func.get('doc', 'Aucune'))}</p>" if func.get('enhanced_doc') or func.get('doc') else ""}
                {f"<p><strong>Exemples :</strong> {func.get('examples', '')}</p>" if func.get('examples') else ""}
            </div>
            """)
    
    # Classes
    if doc_info.get("classes"):
        content_parts.append("<h2>🧱 Classes</h2>")
        for cls in doc_info["classes"]:
            content_parts.append(f"""
            <div class="class">
                <h3>{cls['name']}</h3>
                {f"<p><strong>Héritage :</strong> {', '.join(cls.get('bases', []))}</p>" if cls.get('bases') else ""}
                {f"<p><strong>Documentation :</strong> {cls.get('enhanced_doc', cls.get('doc', 'Aucune'))}</p>" if cls.get('enhanced_doc') or cls.get('doc') else ""}
                {f"<p><strong>Méthodes :</strong> {len(cls.get('methods', []))}</p>" if cls.get('methods') else ""}
            </div>
            """)
    
    content = "\n".join(content_parts)
    
    return html_template.format(
        file_name=file_name,
        function_count=function_count,
        class_count=class_count,
        doc_coverage=doc_coverage,
        quality_grade=quality_grade,
        content=content
    )

def main():
    """Point d'entrée principal du CLI."""
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de documentation Python intelligent avec IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python cli.py mon_fichier.py                    # Documentation basique
  python cli.py mon_fichier.py --enhanced         # Documentation enrichie par IA
  python cli.py mon_fichier.py --format html      # Sortie HTML
  python cli.py mon_fichier.py --format json      # Sortie JSON
  python cli.py mon_fichier.py --verbose          # Mode verbeux
        """
    )
    
    parser.add_argument(
        "fichier",
        help="Chemin du fichier Python à documenter"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Fichier de sortie (défaut: DOC.md)",
        default="DOC.md"
    )
    
    parser.add_argument(
        "--enhanced",
        action="store_true",
        help="Active l'enrichissement par IA (nécessite une clé API Groq)"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "json"],
        default="markdown",
        help="Format de sortie (défaut: markdown)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mode verbeux avec plus de détails"
    )
    
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Désactive l'IA même si --enhanced est spécifié"
    )
    
    args = parser.parse_args()
    
    # Configuration du logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Validation du fichier d'entrée
        file_path = validate_file_path(args.fichier)
        
        # Détermination du fichier de sortie
        output_path = Path(args.output)
        if args.format != "markdown" and output_path.suffix == ".md":
            # Changer l'extension selon le format
            output_path = output_path.with_suffix(f".{args.format}")
        
        # Vérification de l'API Groq si nécessaire
        if args.enhanced and not args.no_ai:
            try:
                from .config import config
                if not config.groq_api_key:
                    logger.warning("⚠️  Clé API Groq non trouvée. Utilisation du mode basique.")
                    args.enhanced = False
            except ImportError:
                logger.warning("⚠️  Configuration Groq non trouvée. Utilisation du mode basique.")
                args.enhanced = False
        
        # Génération de la documentation
        asyncio.run(generate_documentation(
            file_path=file_path,
            output_path=output_path,
            enhanced=args.enhanced,
            format_type=args.format,
            verbose=args.verbose
        ))
        
        print(f"\n🎉 Documentation générée avec succès !")
        print(f"📁 Fichier : {output_path}")
        print(f"🤖 IA : {'Activée' if args.enhanced else 'Désactivée'}")
        print(f"📄 Format : {args.format.upper()}")
        
    except FileNotFoundError as e:
        logger.error(f"❌ Fichier non trouvé : {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"❌ Erreur de validation : {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⏹️  Génération interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur inattendue : {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
