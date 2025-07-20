from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docgen-ai",
    version="2.0.0",
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="🚀 Générateur de documentation Python intelligent avec IA Groq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/votre-repo/docGen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "groq>=0.4.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "ast-comments>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docgen=cli:main",
            "docgen-ai=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "templates": ["*.j2", "*.html", "*.md"],
    },
    keywords="documentation generator python ai groq markdown html",
    project_urls={
        "Bug Reports": "https://github.com/votre-repo/docGen/issues",
        "Source": "https://github.com/votre-repo/docGen",
        "Documentation": "https://github.com/votre-repo/docGen#readme",
    },
)
