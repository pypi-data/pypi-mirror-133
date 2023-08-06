import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appromath",
    version="0.0.1",
    author="Ibrahima BAH, Kévin HENTZ, Alexandre RAMDOO, Henri MACEDO GONCALVES",
    author_email="henri.macedo-goncalves@etu.unistra.fr",
    description="Projet d'analyse: Sujet 31",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henrimacedo/appromath.git",
    project_urls={
        "Bug Tracker": "https://github.com/henrimacedo/appromath.git/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)