"""
Setup the plugin
"""
from setuptools import setup, find_packages

setup(
    version="1.0.0",
    python_requires='>=3.6',
    install_requires=[
        'mkdocs==1.2.3',
    ],
    packages=find_packages(exclude=['*.tests']),
    package_data={'canicve': ['templates/*.template']},
    entry_points={
        'mkdocs.plugins': [
            'canicve = canicve.plugin:CanICVEPlugin'
        ]
    }
)
