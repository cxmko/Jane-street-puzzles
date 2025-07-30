from setuptools import setup, find_packages

setup(
    name="hall-of-mirrors",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
    ],
    author="Cameron Mouangue",
    author_email="cam.mouangue@example.com",
    description="A package for solving Hall of Mirrors puzzles",
    keywords="puzzle, ray-tracing, mirrors",
    python_requires=">=3.6",
)
