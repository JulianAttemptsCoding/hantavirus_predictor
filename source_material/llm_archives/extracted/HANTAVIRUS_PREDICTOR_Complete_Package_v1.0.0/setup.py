from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hantavirus-predictor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@university.edu",
    description="Physics-Informed Foundation Model for Hantavirus Spillover Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/hantavirus-predictor",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest", "black", "flake8", "mypy", "isort"],
        "docs": ["jupyter", "quarto", "sphinx"],
    },
    entry_points={
        "console_scripts": [
            "hanta-train=scripts.train:main",
            "hanta-eval=scripts.evaluate:main",
            "hanta-deploy=scripts.deploy:main",
        ],
    },
)
