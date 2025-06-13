from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="knowledge-graph-builder",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to build knowledge graphs from research topics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/knowledge-graph-builder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.32.0",
        "requests>=2.31.0",
        "google-search-results>=2.4.2",
        "wikipedia>=1.4.0",
        "python-dotenv>=1.0.0",
        "graphviz>=0.20.1",
        "openai>=1.12.0",
        "typing-extensions>=4.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.0",
            "flake8>=7.0.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",  # For static type checking
            "pre-commit>=3.6.0",  # For git hooks
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
            "sphinx-autodoc-typehints>=2.0.0",
        ],
        "test": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "pytest-asyncio>=0.23.0",
        ],
    },
) 