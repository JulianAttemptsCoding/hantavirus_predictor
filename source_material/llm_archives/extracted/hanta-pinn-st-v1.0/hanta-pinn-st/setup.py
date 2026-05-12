from setuptools import setup, find_packages

setup(
    name="hanta-pinn-st",
    version="1.0.0",
    description="Physics-Informed Spatiotemporal Predictor for Hantavirus Risk",
    author="HANTA Research Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.3.0",
        "pytorch-geometric>=2.5.0",
        "torchdiffeq>=0.2.3",
        "numpy>=1.26.0",
        "scipy>=1.13.0",
        "pandas>=2.2.0",
        "scikit-learn>=1.5.0",
        "matplotlib>=3.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.2.0",
            "pytest-cov>=5.0.0",
            "black>=24.4.0",
            "flake8>=7.0.0",
            "mypy>=1.10.0",
        ]
    }
)
