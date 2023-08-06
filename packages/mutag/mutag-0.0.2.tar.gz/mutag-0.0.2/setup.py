import setuptools
from importlib.machinery import SourceFileLoader


version = SourceFileLoader("mutag.version", "mutag/version.py").load_module()

with open("requirements.txt", "r") as fp:
    required = fp.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="mutag",
    version=version.__version__,
    author="Panagiotis Vardanis",
    author_email="panagiotisvardanis@gmail.com",
    description="Automatic tagging of music excerpts with SOTA models in TensorFlow 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/pvardanis/mutag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    project_urls={
        "Source": "https://https://github.com/pvardanis/mutag",
        "Tracker": "https://https://github.com/pvardanis/mutag/issues",
    },
    python_requires=">=3.7",
    install_requires=required,
    extras_require={"testing": ["pytest", "coverage", "pytest-mock", "pylint", "mypy"]},
)
