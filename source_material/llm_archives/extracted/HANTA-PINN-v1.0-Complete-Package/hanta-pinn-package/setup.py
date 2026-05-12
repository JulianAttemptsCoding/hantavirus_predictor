from setuptools import setup, find_packages

setup(
    name="hanta-pinn",
    version="1.0.0",
    description="Physics-Informed Neural Network for Hantavirus Prediction",
    author="HANTA-PINN Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "torch>=2.2",
        "numpy",
        "scipy",
        "pandas",
        "scikit-learn",
    ],
)
