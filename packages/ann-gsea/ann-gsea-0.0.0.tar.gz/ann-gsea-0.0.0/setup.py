from setuptools import setup
import re
import os
import sys


setup(
    name="ann-gsea",
    version="0.0.0",
    python_requires=">3.6.0",
    author="Michael E. Vinyard - Harvard University - Massachussetts General Hospital - Broad Institute of MIT and Harvard",
    author_email="mvinyard@broadinstitute.org",
    url="",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="ann-gsea - integrate GSEA molecular signatures with AnnData",
    packages=[
        "ann-gsea",
    ],
    install_requires=[
        "anndata>=0.7.8",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
